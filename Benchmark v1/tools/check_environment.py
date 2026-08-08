#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Check Benchmark v1 + skill environment readiness."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.io_utils import benchmark_root, repo_root


def ok(msg: str) -> None:
    print(f"  OK  {msg}")


def bad(msg: str) -> None:
    print(f" FAIL {msg}")


def main() -> int:
    print("Investigation Benchmark v1 — environment check\n")
    root = benchmark_root()
    repo = repo_root()
    fails = 0

    print("[paths]")
    if (root / "config.yaml").is_file():
        ok(f"config.yaml @ {root}")
    else:
        bad("config.yaml missing")
        fails += 1

    skill_md = repo / "SKILL.md"
    if skill_md.is_file():
        ok(f"skill SKILL.md @ {repo}")
    else:
        bad("skill SKILL.md not found (expected parent of Benchmark v1)")
        fails += 1

    audit = repo / "scripts" / "audit_vault.py"
    if audit.is_file():
        ok("scripts/audit_vault.py")
    else:
        bad("scripts/audit_vault.py missing")
        fails += 1

    print("\n[python packages]")
    for pkg in ("yaml",):
        if importlib.util.find_spec(pkg if pkg != "yaml" else "yaml"):
            # PyYAML imports as yaml
            ok("PyYAML (yaml)")
        else:
            bad("PyYAML missing — pip install pyyaml")
            fails += 1

    print("\n[tools]")
    for t in (
        "score_vault.py",
        "run_benchmark.py",
        "aggregate_results.py",
        "validate_case.py",
        "init_case.py",
        "seed_historical_cases.py",
    ):
        p = root / "tools" / t
        if p.is_file():
            ok(t)
        else:
            bad(f"missing {t}")
            fails += 1

    print("\n[cases]")
    cases = list((root / "cases").glob("CASE-*")) if (root / "cases").is_dir() else []
    ok(f"{len(cases)} case pack(s) found")
    if (root / "cases" / "_template").is_dir():
        ok("cases/_template")
    else:
        bad("cases/_template missing")
        fails += 1

    print("\n[fixtures]")
    for name in ("sample_vault_good", "sample_vault_bad"):
        p = root / "fixtures" / name
        if p.is_dir():
            ok(name)
        else:
            bad(f"fixture missing: {name}")
            fails += 1

    print()
    if fails:
        print(f"RESULT: {fails} failure(s)")
        return 1
    print("RESULT: ready")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
