#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Safe case-scoped self-tooling manager.

The default execution mode is fail-closed: without Docker, Podman, or
bubblewrap the command is recorded as skipped rather than run on the host.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None  # type: ignore

try:
    from case_memory import append_event as append_memory_event, write_snapshot as write_memory_snapshot
except ImportError:  # pragma: no cover
    append_memory_event = None  # type: ignore
    write_memory_snapshot = None  # type: ignore

WRITE_PREFIXES = ("08-Tooling", "05-Analysis", "02b-Exploration", "case-logs")
RUN_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,63}$")
DEFAULT_RUNTIME = "python3"
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    if path.is_file():
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        return f"sha256:{digest.hexdigest()}"
    if path.is_dir():
        for child in sorted(p for p in path.rglob("*") if p.is_file()):
            digest.update(child.relative_to(path).as_posix().encode())
            digest.update(sha256_path(child).encode())
        return f"sha256:{digest.hexdigest()}"
    return "sha256:missing"


def inside(root: Path, candidate: Path) -> bool:
    try:
        candidate.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def relative(root: Path, path: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def safe_case_path(case_root: Path, raw: str, *, label: str) -> Path:
    value = str(raw).replace("\\", "/")
    normalized = value.rstrip("/")
    if value.startswith("/") or any(part in {"", ".", ".."} for part in normalized.split("/")):
        raise ValueError(f"{label} contains unsafe path segments: {raw}")
    path = (case_root / value).resolve()
    if not inside(case_root, path):
        raise ValueError(f"{label} escapes case root: {raw}")
    return path


def append_event(case_root: Path, event: str, **payload: Any) -> None:
    if append_memory_event is not None:
        append_memory_event(
            case_root,
            event,
            tool_event=event.startswith("tool."),
            **payload,
        )
        return
    # Compatibility fallback for a copied standalone case_tooling.py.
    log_dir = case_root / "case-logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    row = {"ts": now(), "event": event, **payload}
    with (log_dir / "tool-runs.jsonl").open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def load_manifest(path: Path) -> dict[str, Any]:
    if yaml is None:
        raise RuntimeError("PyYAML is required: pip install PyYAML")
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".md":
        match = FRONTMATTER_RE.match(text)
        if not match:
            raise ValueError("Markdown manifest must start with YAML frontmatter")
        text = match.group(1)
    data = yaml.safe_load(text) or {}
    if not isinstance(data, dict):
        raise ValueError("manifest root must be a mapping")
    return data


def _validate_entrypoint(case_root: Path, entrypoint: Any, errors: list[str]) -> None:
    if not entrypoint:
        return
    try:
        entry = safe_case_path(case_root, str(entrypoint), label="entrypoint")
    except ValueError as exc:
        errors.append(str(exc))
    else:
        if not entry.is_file():
            errors.append(f"entrypoint does not exist: {entrypoint}")


def _validate_writes(case_root: Path, writes: Any, errors: list[str]) -> None:
    if not isinstance(writes, list):
        errors.append("writes-to must be a list")
        return
    for item in writes:
        try:
            target = safe_case_path(case_root, str(item), label="writes-to")
            text = relative(case_root, target)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        if not any(text == prefix or text.startswith(prefix + "/") for prefix in WRITE_PREFIXES):
            errors.append(f"writes-to outside allowed prefixes: {item}")


def validate_manifest(case_root: Path, path: Path) -> list[str]:
    errors: list[str] = []
    try:
        data = load_manifest(path)
    except Exception as exc:
        return [f"manifest parse error: {exc}"]
    for field in ("tool-id", "version", "entrypoint"):
        if not data.get(field):
            errors.append(f"missing {field}")
    _validate_entrypoint(case_root, data.get("entrypoint"), errors)
    network = str(data.get("network", "denied")).lower()
    if network not in {"denied", "none"}:
        errors.append("network must be denied/none")
    _validate_writes(case_root, data.get("writes-to") or data.get("writes_to") or [], errors)
    return errors


def init_case(case_root: Path, session_id: str) -> None:
    for path in ("08-Tooling/Active", "08-Tooling/Library", "08-Tooling/Archive", "08-Tooling/Manifests", "08-Tooling/Audits", "08-Tooling/Fixtures", "08-Tooling/Runs", "case-logs"):
        (case_root / path).mkdir(parents=True, exist_ok=True)
    session_log = case_root / "case-logs" / "session.jsonl"
    if not session_log.exists():
        session_log.write_text("", encoding="utf-8")
    decisions = case_root / "case-logs" / "decisions.md"
    if not decisions.exists():
        decisions.write_text(
            "---\n"
            "type: case-log\n"
            "status: draft\n"
            "created: " + now()[:10] + "\n"
            "updated: " + now()[:10] + "\n"
            "tags: [log, decisions]\n"
            "---\n\n"
            f"# Case Decisions — {session_id}\n\n| time | decision | reason | references |\n|---|---|---|---|\n",
            encoding="utf-8",
        )
    append_event(case_root, "session.init", session_id=session_id, case_root_path=str(case_root.resolve()))
    if write_memory_snapshot is not None:
        write_memory_snapshot(case_root)
    print(f"initialized tooling workspace: {case_root}")


def choose_backend(requested: str) -> str:
    if requested != "auto":
        return requested
    for name in ("docker", "podman", "bwrap"):
        if shutil.which(name):
            return name
    return "none"


def build_command(case_root: Path, manifest_path: Path, manifest: dict[str, Any], backend: str, tool_args: list[str]) -> tuple[list[str], Path]:
    entrypoint = safe_case_path(case_root, str(manifest["entrypoint"]), label="entrypoint")
    runtime = str(manifest.get("runtime") or DEFAULT_RUNTIME)
    writes = manifest.get("writes-to") or manifest.get("writes_to") or []
    if not isinstance(writes, list):
        writes = [writes]
    write_targets = []
    for raw in writes:
        target = safe_case_path(case_root, str(raw), label="writes-to")
        target.mkdir(parents=True, exist_ok=True)
        write_targets.append((target, "/workspace/" + relative(case_root, target)))
    raw_command = manifest.get("command")
    if raw_command:
        if not isinstance(raw_command, list) or not all(isinstance(x, str) for x in raw_command):
            raise ValueError("manifest command must be a list of strings")
        base = [x.replace("{entrypoint}", "/workspace/" + relative(case_root, entrypoint)) for x in raw_command]
    else:
        base = [runtime, "/workspace/" + relative(case_root, entrypoint)]
    base += tool_args
    if backend in {"docker", "podman"}:
        image = str(manifest.get("image") or "python:3.12-slim")
        command = [backend, "run", "--rm", "--network", "none", "--read-only", "-v", f"{case_root.resolve()}:/workspace:ro"]
        for host_path, container_path in write_targets:
            command += ["-v", f"{host_path}:{container_path}:rw"]
        return [*command, "-w", "/workspace", image, *base], entrypoint
    if backend == "bwrap":
        command = ["bwrap", "--die-with-parent", "--unshare-net", "--ro-bind", str(case_root.resolve()), "/workspace"]
        for host_path, container_path in write_targets:
            command += ["--bind", str(host_path), container_path]
        return [*command, "--chdir", "/workspace", *base], entrypoint
    return base, entrypoint


def _hash_inputs(case_root: Path, inputs: Any) -> list[dict[str, str]]:
    paths = []
    for raw in inputs or []:
        path = safe_case_path(case_root, str(raw), label="input")
        paths.append({"path": relative(case_root, path), "hash": sha256_path(path)})
    return paths


def _run_process(command: list[str], case_root: Path, timeout: int) -> dict[str, Any]:
    try:
        completed = subprocess.run(command, cwd=case_root, capture_output=True, text=True, timeout=timeout, check=False)
        return {"exit_code": completed.returncode, "stdout": completed.stdout[-4000:], "stderr": completed.stderr[-4000:]}
    except subprocess.TimeoutExpired as exc:
        return {"exit_code": 124, "stdout": str(exc.stdout or "")[-4000:], "stderr": "timeout"}
    except OSError as exc:
        return {"exit_code": 126, "stderr": str(exc)}


def run_tool(args: argparse.Namespace) -> int:
    case_root = Path(args.case_root).resolve()
    manifest_path = Path(args.manifest)
    if not manifest_path.is_absolute():
        manifest_path = case_root / manifest_path
    manifest_path = manifest_path.resolve()
    if not inside(case_root, manifest_path):
        print("ERROR: manifest must be inside case root", file=sys.stderr)
        return 2
    errors = validate_manifest(case_root, manifest_path)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 2
    manifest = load_manifest(manifest_path)
    run_id = args.run_id or f"RUN-{int(time.time())}"
    if not RUN_ID_RE.fullmatch(run_id):
        print("ERROR: run-id must be a safe identifier (letters, numbers, . _ -)", file=sys.stderr)
        return 2
    backend = choose_backend(args.backend)
    if backend == "host" and not args.allow_host:
        print("ERROR: host execution requires --allow-host", file=sys.stderr)
        return 2
    if backend == "none":
        append_event(case_root, "tool.run.skipped", tool_id=manifest["tool-id"], reason="no sandbox backend available")
        print("SKIPPED: no Docker, Podman, or bubblewrap backend available; fail-closed")
        return 3
    try:
        output_dir = safe_case_path(case_root, str(args.output_dir or "08-Tooling/Runs"), label="output directory")
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    output_dir.mkdir(parents=True, exist_ok=True)
    command, entrypoint = build_command(case_root, manifest_path, manifest, backend, args.tool_arg or [])
    try:
        input_paths = _hash_inputs(case_root, manifest.get("inputs"))
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    output_before = sha256_path(output_dir)
    record = {
        "run_id": run_id,
        "tool_id": manifest["tool-id"],
        "tool_version": manifest.get("version"),
        "backend": backend,
        "network": "denied" if backend != "host" else "unspecified",
        "command_digest": hashlib.sha256("\0".join(command).encode()).hexdigest(),
        "entrypoint": relative(case_root, entrypoint),
        "inputs": input_paths,
        "output_dir": relative(case_root, output_dir),
        "started_at": now(),
    }
    append_event(case_root, "tool.run.start", **record)
    record.update(_run_process(command, case_root, args.timeout))
    record.update({"finished_at": now(), "output_hash_before": output_before, "output_hash_after": sha256_path(output_dir)})
    append_event(case_root, "tool.run.finish", **record)
    audit_path = case_root / "08-Tooling" / "Audits" / f"{run_id}.json"
    audit_path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: record[k] for k in ("run_id", "tool_id", "backend", "exit_code", "entrypoint", "output_dir")}, ensure_ascii=False, indent=2))
    return int(record["exit_code"])


def main() -> int:
    parser = argparse.ArgumentParser(description="Manage case-scoped self-tooling")
    sub = parser.add_subparsers(dest="command", required=True)
    p_init = sub.add_parser("init")
    p_init.add_argument("case_root")
    p_init.add_argument("--session-id", default="SESSION-000")
    p_init.set_defaults(func=lambda a: (init_case(Path(a.case_root).resolve(), a.session_id) or 0))
    p_validate = sub.add_parser("validate")
    p_validate.add_argument("case_root")
    p_validate.add_argument("manifest")
    def validate_cmd(a: argparse.Namespace) -> int:
        case_root = Path(a.case_root).resolve()
        manifest = Path(a.manifest)
        if not manifest.is_absolute():
            manifest = case_root / manifest
        errors = validate_manifest(case_root, manifest.resolve())
        if errors:
            print("\n".join(errors), file=sys.stderr)
            return 1
        print("manifest valid")
        return 0
    p_validate.set_defaults(func=validate_cmd)
    p_run = sub.add_parser("run")
    p_run.add_argument("case_root")
    p_run.add_argument("--manifest", required=True)
    p_run.add_argument("--backend", choices=("auto", "docker", "podman", "bwrap", "host"), default="auto")
    p_run.add_argument("--allow-host", action="store_true")
    p_run.add_argument("--run-id")
    p_run.add_argument("--output-dir", default="08-Tooling/Runs")
    p_run.add_argument("--timeout", type=int, default=300)
    p_run.add_argument("--tool-arg", action="append", default=[], help="argument passed to the tool; repeat as needed")
    p_run.set_defaults(func=run_tool)
    args = parser.parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
