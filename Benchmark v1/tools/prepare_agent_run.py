#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prepare an agent-visible bundle per case (no ground_truth / designer_notes).

Writes:
  results/runs/<run_id>/<case_id>/agent_input/
    BRIEF.md + packet sources + prompts + INSTRUCTIONS.md
  results/runs/<run_id>/MANIFEST.md
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.io_utils import benchmark_root, write_text  # noqa: E402

INSTRUCTIONS = """# Agent instructions (visible)

You are building an Obsidian investigation vault using **obsidian-investigation-brain**.

## Rules
1. Use **only** files in this `agent_input/` folder plus the skill files provided by the host.
2. Do **not** invent evidence, lab results, wiretap quotes, DNA tables, or names absent from the packet.
3. Modes: Scaffold → Manage → Audit → Report (announce each).
4. Operational evidence → Chain-of-Custody; public-archive → source-provenance.
5. Every Primary hypothesis needs a substantive Counter.
6. Reports need `claim-trace`; Court-File forbidden unless readiness-passed.
7. Organized crime → consider Enterprise-Map. Serial patterns → consider Series-Linkage.
8. Declare gaps in Coverage-Ledger (`gaps:` YAML preferred).

## Deliverable
Write the full vault under the sibling folder `../vault/` (created by you).
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--cases", nargs="+", required=True)
    args = ap.parse_args()

    root = benchmark_root()
    run_root = root / "results" / "runs" / args.run_id
    lines = [f"# Agent run manifest — `{args.run_id}`", "", "Cases prepared:", ""]

    for cid in args.cases:
        case = root / "cases" / cid
        if not case.is_dir():
            print(f"MISSING {cid}", file=sys.stderr)
            return 1
        dest = run_root / cid / "agent_input"
        if dest.exists():
            shutil.rmtree(dest)
        dest.mkdir(parents=True)

        # packet
        packet_src = case / "source_packet"
        if packet_src.is_dir():
            shutil.copytree(packet_src, dest / "source_packet")
        prompts = case / "prompts"
        if prompts.is_dir():
            shutil.copytree(prompts, dest / "prompts")
        write_text(dest / "INSTRUCTIONS.md", INSTRUCTIONS)

        # ensure vault dir exists empty-ish
        (run_root / cid / "vault").mkdir(parents=True, exist_ok=True)
        lines.append(f"- `{cid}` → `results/runs/{args.run_id}/{cid}/agent_input/`")
        print(f"prepared {cid}")

    lines += [
        "",
        "## Next",
        "1. Run agent per case using agent_input only.",
        "2. Write vault to `.../<case_id>/vault/`.",
        "3. Score with `--producer agent`.",
        "",
        "See `docs/AGENT_RUN_PROTOCOL.md`.",
    ]
    write_text(run_root / "MANIFEST.md", "\n".join(lines) + "\n")
    print(f"MANIFEST → {run_root / 'MANIFEST.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
