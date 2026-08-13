#!/usr/bin/env python3
"""Validate Investigation Swarm MVP outputs without promoting anything."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sys
from typing import Any


FRONTMATTER = re.compile(r"\A---\n(?P<body>.*?)\n---\n", re.DOTALL)
ALLOWED_SEGMENT = "08-Tooling/Swarm"


def inside(root: Path, path: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def parse_frontmatter(path: Path) -> dict[str, Any]:
    match = FRONTMATTER.match(path.read_text(encoding="utf-8"))
    if not match:
        raise ValueError(f"missing frontmatter: {path}")
    values: dict[str, Any] = {}
    for line in match.group("body").splitlines():
        if not line.strip() or ":" not in line:
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip('"')
    return values


def validate(case_root: Path, team_id: str, run_id: str) -> dict[str, Any]:
    root = case_root.resolve()
    run_root = (root / ALLOWED_SEGMENT / team_id / "runs" / run_id).resolve()
    errors: list[str] = []
    warnings: list[str] = []
    if not inside(root, run_root):
        errors.append("run path escapes case root")
    if not run_root.exists():
        errors.append(f"run does not exist: {run_root}")
        return {"valid": False, "errors": errors, "warnings": warnings}
    run_json = run_root / "run.json"
    try:
        run_data = json.loads(run_json.read_text(encoding="utf-8"))
        if run_data.get("team_id") != team_id or run_data.get("run_id") != run_id:
            errors.append("run.json identity mismatch")
        if not str(run_data.get("source_hash", "")).startswith("sha256:"):
            errors.append("run.json missing source_hash")
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid run.json: {exc}")

    proposals = sorted((run_root / "proposals").glob("*.md")) if (run_root / "proposals").exists() else []
    for proposal in proposals:
        try:
            meta = parse_frontmatter(proposal)
            if meta.get("type") != "agent-proposal":
                errors.append(f"wrong proposal type: {proposal}")
            if meta.get("status") not in {"draft", "unstructured"}:
                errors.append(f"proposal is not draft/unstructured: {proposal}")
            if meta.get("run-id") != run_id:
                errors.append(f"proposal run mismatch: {proposal}")
            if meta.get("parse-status") == "structured" and "## Claims" not in proposal.read_text(encoding="utf-8"):
                errors.append(f"structured proposal has no Claims section: {proposal}")
        except (OSError, ValueError) as exc:
            errors.append(str(exc))
    if not proposals:
        warnings.append("no proposals found")

    for filename in ("conflicts.md", "consensus-draft.md"):
        path = run_root / filename
        if not path.exists():
            errors.append(f"missing {filename}")
        else:
            try:
                meta = parse_frontmatter(path)
                if meta.get("run-id") != run_id:
                    errors.append(f"{filename} run mismatch")
                if filename == "consensus-draft.md" and meta.get("status") != "pending-human-review":
                    errors.append("consensus draft is not pending-human-review")
            except (OSError, ValueError) as exc:
                errors.append(str(exc))

    gates = sorted((run_root / "human-gates").glob("*.md")) if (run_root / "human-gates").exists() else []
    if len(gates) != 1:
        errors.append(f"expected exactly one human gate, found {len(gates)}")
    for gate in gates:
        try:
            meta = parse_frontmatter(gate)
            if meta.get("type") != "human-gate" or meta.get("status") != "pending-human-review":
                errors.append(f"gate is not pending-human-review: {gate}")
        except (OSError, ValueError) as exc:
            errors.append(str(exc))

    session = root / "case-logs" / "session.jsonl"
    event_count = 0
    if session.exists():
        for number, line in enumerate(session.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            event_count += 1
            try:
                event = json.loads(line)
                if event.get("run_id") == run_id and event.get("team_id") != team_id:
                    errors.append(f"session event {number} has wrong team_id")
            except json.JSONDecodeError:
                errors.append(f"invalid JSONL at session.jsonl:{number}")
    else:
        errors.append("missing case-logs/session.jsonl")

    outside = []
    for path in run_root.rglob("*"):
        if path.is_file() and not inside(root / ALLOWED_SEGMENT, path):
            outside.append(str(path))
    if outside:
        errors.append("run contains path outside 08-Tooling/Swarm")

    return {
        "valid": not errors,
        "case_root": str(root),
        "team_id": team_id,
        "run_id": run_id,
        "proposals": len(proposals),
        "session_events": event_count,
        "errors": errors,
        "warnings": warnings,
        "promotion_allowed": False,
        "checked_at": datetime.now(timezone.utc).isoformat(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Investigation Swarm artifacts")
    parser.add_argument("case_root")
    parser.add_argument("--team-id", required=True)
    parser.add_argument("--run-id", required=True)
    args = parser.parse_args()
    try:
        result = validate(Path(args.case_root), args.team_id, args.run_id)
    except Exception as exc:
        print(json.dumps({"valid": False, "errors": [str(exc)], "promotion_allowed": False}, indent=2))
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
