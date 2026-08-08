#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Create a new case pack from the template."""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.io_utils import benchmark_root, dump_yaml, load_yaml, write_text

CASE_ID_RE = re.compile(r"^CASE-[A-Z0-9-]+$")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--case-id", required=True, help="e.g. CASE-DEMO-001")
    ap.add_argument("--title", required=True)
    ap.add_argument("--difficulty", type=int, default=2)
    ap.add_argument("--status", default="training")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    if not CASE_ID_RE.match(args.case_id):
        print("case-id must match CASE-[A-Z0-9-]+", file=sys.stderr)
        return 2

    root = benchmark_root()
    template = root / "cases" / "_template"
    dest = root / "cases" / args.case_id
    if dest.exists() and not args.force:
        print(f"ERROR: {dest} exists (use --force)", file=sys.stderr)
        return 1
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(template, dest)

    case = load_yaml(dest / "case.yaml")
    case["case_id"] = args.case_id
    case["title"] = args.title
    case["difficulty"] = args.difficulty
    case["case_status"] = args.status
    dump_yaml(dest / "case.yaml", case)

    gt = load_yaml(dest / "ground_truth.yaml")
    gt["case_id"] = args.case_id
    dump_yaml(dest / "ground_truth.yaml", gt)

    readme = f"""# {args.case_id} — {args.title}

Difficulty: D{args.difficulty}

## Agent inputs
- `source_packet/` only

## Scoring
- `ground_truth.yaml` (hidden from agent during generation)
"""
    write_text(dest / "README.md", readme)
    print(f"Created {dest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
