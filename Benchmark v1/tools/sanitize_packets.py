#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Remove agent-leaked designer hints from source_packet/BRIEF.md
and write designer_notes.md next to ground_truth (not agent-visible).

B-P0-2 from REFORM_PLAN_FROM_BENCHMARK.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.io_utils import benchmark_root, load_yaml, write_text  # noqa: E402

TRUTH_SECTION_RE = re.compile(
    r"\n##\s*Suggested conclusion discipline\s*\n.*?(?=\n##\s|\Z)",
    re.IGNORECASE | re.DOTALL,
)
TRUTH_LINE_RE = re.compile(
    r"^.*Truth band for designers.*$",
    re.IGNORECASE | re.MULTILINE,
)


def sanitize_brief(text: str) -> tuple[str, bool]:
    original = text
    text = TRUTH_SECTION_RE.sub("\n", text)
    text = TRUTH_LINE_RE.sub("", text)
    # collapse 3+ newlines
    text = re.sub(r"\n{3,}", "\n\n", text).rstrip() + "\n"
    return text, text != original


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases-dir", default=None)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    root = benchmark_root()
    cases_dir = Path(args.cases_dir) if args.cases_dir else root / "cases"
    n_brief = 0
    n_notes = 0

    for case_dir in sorted(cases_dir.glob("CASE-*")):
        if not case_dir.is_dir():
            continue
        brief_path = case_dir / "source_packet" / "BRIEF.md"
        gt_path = case_dir / "ground_truth.yaml"
        truth = None
        if gt_path.is_file():
            try:
                gt = load_yaml(gt_path)
                truth = gt.get("truth_status")
            except Exception:
                truth = None

        designer = case_dir / "designer_notes.md"
        if truth and not designer.is_file():
            body = f"""# Designer notes — {case_dir.name}

**Not agent-visible.** Do not copy into source_packet.

- truth_status: `{truth}`
- Use only for authoring ground_truth and adjudication.
"""
            if not args.dry_run:
                write_text(designer, body)
            n_notes += 1
            print(f"notes {case_dir.name}")

        if not brief_path.is_file():
            continue
        text = brief_path.read_text(encoding="utf-8", errors="replace")
        new_text, changed = sanitize_brief(text)
        if changed:
            n_brief += 1
            print(f"brief {case_dir.name}")
            if not args.dry_run:
                brief_path.write_text(new_text, encoding="utf-8")

    print(f"\nSanitized briefs: {n_brief}; designer_notes written: {n_notes}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
