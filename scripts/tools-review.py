#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Review case tooling without deleting anything automatically."""
from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any] | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else None
    except Exception:
        return None


def review(case_root: Path) -> dict[str, Any]:
    active = case_root / "08-Tooling" / "Active"
    audits = case_root / "08-Tooling" / "Audits"
    library = case_root / "08-Tooling" / "Library"
    archive = case_root / "08-Tooling" / "Archive"
    suggestions: list[dict[str, str]] = []
    if not active.exists():
        return {"case_root": str(case_root), "suggestions": [], "note": "no Active tooling directory"}
    audit_rows = {p.stem: load_json(p) for p in audits.glob("*.json")} if audits.exists() else {}
    for path in sorted(p for p in active.rglob("*") if p.is_file()):
        if path.name.endswith((".pyc", ".tmp")):
            continue
        rel = path.relative_to(case_root).as_posix()
        linked = [row for row in audit_rows.values() if row and row.get("entrypoint") == rel]
        if not linked:
            suggestions.append({"path": rel, "action": "audit", "reason": "no Tool-Audit execution record found"})
            continue
        latest = linked[-1]
        if latest.get("exit_code") == 0:
            suggestions.append({"path": rel, "action": "review-for-promotion", "reason": "latest recorded run exited 0; human review still required"})
        else:
            suggestions.append({"path": rel, "action": "retain-or-archive", "reason": f"latest run exit_code={latest.get('exit_code')}; do not promote automatically"})
    return {"case_root": str(case_root), "generated_at": datetime.now(timezone.utc).isoformat(), "suggestions": suggestions}


def apply_move(case_root: Path, paths: list[str], destination: str, decision: str) -> None:
    target_root = case_root / "08-Tooling" / destination
    target_root.mkdir(parents=True, exist_ok=True)
    active_root = (case_root / "08-Tooling" / "Active").resolve()
    moved: list[str] = []
    for raw in paths:
        src = (case_root / raw).resolve()
        try:
            src.relative_to(active_root)
        except ValueError as exc:
            raise ValueError(f"refusing to move path outside 08-Tooling/Active: {raw}") from exc
        if not src.is_file():
            raise ValueError(f"refusing to move missing path: {raw}")
        dest = target_root / src.name
        if dest.exists():
            dest = target_root / f"{src.stem}-{int(datetime.now().timestamp())}{src.suffix}"
        shutil.move(str(src), str(dest))
        moved.append(dest.relative_to(case_root).as_posix())
    log = case_root / "case-logs" / "decisions.md"
    log.parent.mkdir(parents=True, exist_ok=True)
    with log.open("a", encoding="utf-8") as handle:
        for item in moved:
            handle.write(f"| {datetime.now(timezone.utc).isoformat()} | {decision} | explicit tools-review decision | `{item}` |\n")


def apply_archive(case_root: Path, paths: list[str]) -> None:
    apply_move(case_root, paths, "Archive", "archive tool")


def apply_promote(case_root: Path, paths: list[str]) -> None:
    apply_move(case_root, paths, "Library", "promote tool after human review")


def main() -> int:
    parser = argparse.ArgumentParser(description="Review self-tooling lifecycle")
    parser.add_argument("case_root")
    parser.add_argument("--json")
    parser.add_argument("--archive", nargs="*", default=None, help="explicit paths to archive; never automatic")
    parser.add_argument("--promote", nargs="*", default=None, help="explicit paths to promote after human review; never automatic")
    args = parser.parse_args()
    root = Path(args.case_root).resolve()
    result = review(root)
    if args.archive:
        apply_archive(root, args.archive)
        result["archived"] = args.archive
    if args.promote:
        apply_promote(root, args.promote)
        result["promoted"] = args.promote
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.json:
        Path(args.json).write_text(rendered, encoding="utf-8")
    print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
