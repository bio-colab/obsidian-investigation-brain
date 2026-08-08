#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validate case packs (case.yaml + ground_truth.yaml + source_packet)."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.io_utils import benchmark_root, load_yaml

CASE_ID_RE = re.compile(r"^CASE-[A-Z0-9-]+$")


def validate_one(case_dir: Path, strict: bool = True) -> list[str]:
    errors: list[str] = []
    case_yaml = case_dir / "case.yaml"
    gt_path = case_dir / "ground_truth.yaml"
    brief = case_dir / "source_packet" / "BRIEF.md"

    if not case_yaml.is_file():
        errors.append("missing case.yaml")
        return errors
    if not gt_path.is_file():
        errors.append("missing ground_truth.yaml")
        return errors

    try:
        case = load_yaml(case_yaml)
    except Exception as e:
        errors.append(f"case.yaml parse error: {e}")
        return errors
    try:
        gt = load_yaml(gt_path)
    except Exception as e:
        errors.append(f"ground_truth.yaml parse error: {e}")
        return errors

    cid = case.get("case_id")
    if not cid or not CASE_ID_RE.match(str(cid)):
        errors.append(f"invalid case_id: {cid!r}")
    if gt.get("case_id") and gt.get("case_id") != cid:
        errors.append(f"case_id mismatch case.yaml={cid} gt={gt.get('case_id')}")

    for field in ("title", "difficulty", "case_status", "scope", "phases"):
        if field not in case:
            errors.append(f"case.yaml missing {field}")

    scope = case.get("scope") or {}
    if not scope.get("in_scope") or not scope.get("out_of_scope"):
        errors.append("scope.in_scope and scope.out_of_scope required")

    if not case.get("phases"):
        errors.append("phases must be non-empty")

    diff = case.get("difficulty")
    if diff is not None and (not isinstance(diff, int) or diff < 1 or diff > 5):
        errors.append(f"difficulty must be 1..5, got {diff}")

    if "truth_status" not in gt:
        errors.append("ground_truth missing truth_status")
    if not gt.get("evidence"):
        errors.append("ground_truth.evidence empty")
    if not gt.get("hypotheses"):
        errors.append("ground_truth.hypotheses empty")

    # id uniqueness
    for key in ("evidence", "hypotheses", "timeline_events", "contradictions", "missing_evidence"):
        ids = [x.get("id") for x in (gt.get(key) or []) if isinstance(x, dict)]
        if len(ids) != len(set(ids)):
            errors.append(f"duplicate ids in {key}")

    # primary should have counter theme or counter hyp in GT
    primaries = [h for h in (gt.get("hypotheses") or []) if h.get("kind") == "primary"]
    counters = [h for h in (gt.get("hypotheses") or []) if h.get("kind") == "counter"]
    if primaries and not counters and not any(p.get("expected_counter_themes") for p in primaries):
        errors.append("primary hypotheses without GT counter or expected_counter_themes")

    if not brief.is_file():
        errors.append("missing source_packet/BRIEF.md")

    prompts_dir = case_dir / "prompts"
    if strict:
        for name in ("scaffold.md", "manage.md", "audit.md", "report.md"):
            if not (prompts_dir / name).is_file():
                errors.append(f"missing prompts/{name}")

    # soft: evidence source_kind consistency flags
    for e in gt.get("evidence") or []:
        if e.get("source_kind") in ("public-archive", "archival", "official-archive", "declassified"):
            if e.get("must_have_coc") and not e.get("must_have_provenance"):
                errors.append(f"evidence {e.get('id')}: archival should use must_have_provenance not only CoC")

    return errors


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("case_dir", nargs="?", help="Single case directory")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--cases-dir", default=None)
    ap.add_argument("--relaxed", action="store_true", help="Do not require all prompt files")
    args = ap.parse_args()

    root = benchmark_root()
    cases_dir = Path(args.cases_dir) if args.cases_dir else root / "cases"
    strict = not args.relaxed

    targets: list[Path] = []
    if args.all:
        targets = sorted([p for p in cases_dir.iterdir() if p.is_dir() and p.name.startswith("CASE-")])
    elif args.case_dir:
        targets = [Path(args.case_dir)]
    else:
        print("Usage: validate_case.py <case_dir> | --all", file=sys.stderr)
        return 2

    n_err = 0
    for t in targets:
        errs = validate_one(t, strict=strict)
        if errs:
            n_err += 1
            print(f"FAIL {t.name}")
            for e in errs:
                print(f"  - {e}")
        else:
            print(f"OK   {t.name}")

    print(f"\n{len(targets) - n_err}/{len(targets)} valid")
    return 1 if n_err else 0


if __name__ == "__main__":
    raise SystemExit(main())
