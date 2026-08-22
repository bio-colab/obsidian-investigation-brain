#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Run Investigation Benchmark v1 over a set of case packs and produced vaults.

Expected vault layout (default):
  {vaults_root}/{case_id}/vault/
or:
  {vaults_root}/{case_id}/

Case packs:
  cases/CASE-*/case.yaml + ground_truth.yaml
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

from lib.io_utils import benchmark_root, dump_json, load_yaml, write_text
from score_vault import render_md, score
import validate_obsidian_native


def discover_cases(cases_dir: Path, pattern: str = "CASE-*") -> list[Path]:
    cases = sorted([p for p in cases_dir.glob(pattern) if p.is_dir() and p.name != "_template"])
    return cases


def resolve_vault(vaults_root: Path, case_id: str) -> Path | None:
    candidates = [
        vaults_root / case_id / "vault",
        vaults_root / case_id,
        vaults_root / f"{case_id}-vault",
    ]
    for c in candidates:
        if c.is_dir() and any(c.rglob("*.md")):
            return c
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description="Run benchmark scoring across cases")
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--vaults-root", required=True, help="Directory containing per-case vaults")
    ap.add_argument("--cases-dir", default=None)
    ap.add_argument("--cases-glob", default="CASE-*")
    ap.add_argument("--only", nargs="*", default=None, help="Optional explicit case_id list")
    ap.add_argument("--config", default=None)
    ap.add_argument("--no-audit", action="store_true")
    ap.add_argument("--no-native-check", action="store_true", help="Do not run Obsidian native-format validation")
    ap.add_argument("--strict-native", action="store_true", help="Treat native-format errors as a case failure")
    ap.add_argument("--skip-missing", action="store_true", help="Skip cases without vaults instead of failing")
    ap.add_argument(
        "--producer",
        default="baseline",
        choices=["baseline", "agent", "adversarial", "unspecified"],
        help="Tag scores with vault producer (baseline ≠ agent skill proof)",
    )
    args = ap.parse_args()

    root = benchmark_root()
    cases_dir = Path(args.cases_dir) if args.cases_dir else root / "cases"
    vaults_root = Path(args.vaults_root)
    out_dir = root / "results" / "runs" / args.run_id
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.only:
        cases = [cases_dir / c for c in args.only]
    else:
        cases = discover_cases(cases_dir, args.cases_glob)
    if not cases:
        print(f"ERROR: no cases under {cases_dir} matching {args.cases_glob}", file=sys.stderr)
        return 2

    results = []
    missing = []
    for case_path in cases:
        case_yaml = case_path / "case.yaml"
        gt_path = case_path / "ground_truth.yaml"
        if not gt_path.is_file():
            print(f"WARN: skip {case_path.name} — no ground_truth.yaml", file=sys.stderr)
            continue
        case_id = case_path.name
        if case_yaml.is_file():
            meta = load_yaml(case_yaml)
            case_id = meta.get("case_id") or case_id

        vault = resolve_vault(vaults_root, case_id) or resolve_vault(vaults_root, case_path.name)
        if not vault:
            missing.append(case_id)
            print(f"MISSING vault for {case_id}", file=sys.stderr)
            continue

        print(f"Scoring {case_id} <- {vault}", file=sys.stderr)
        native_result = None
        native_error = None
        if not args.no_native_check:
            try:
                native_result = validate_obsidian_native.validate(vault)
                native_error = native_result["score"]["errors"] > 0
            except Exception as exc:
                native_error = True
                native_result = {"vault": str(vault), "score": {"errors": 1, "warnings": 0, "total": 1}, "issues": [{"severity": "error", "code": "NATIVE_CHECK_FAILED", "message": str(exc)}]}
        try:
            if args.strict_native and native_error:
                raise ValueError("native-format validation failed in --strict-native mode")
            result = score(
                vault=vault,
                gt_path=gt_path,
                case_id=case_id,
                config_path=Path(args.config) if args.config else None,
                call_audit=not args.no_audit,
                producer=args.producer,
            )
        except Exception as e:
            print(f"ERROR scoring {case_id}: {e}", file=sys.stderr)
            result = {
                "benchmark_version": "1.0.0",
                "case_id": case_id,
                "case_score": 0.0,
                "error": str(e),
                "metrics": {},
            }
        result["run_id"] = args.run_id
        result.setdefault("producer", args.producer)
        if native_result is not None:
            result["native_validation"] = native_result["score"]
        case_out = out_dir / case_id
        case_out.mkdir(parents=True, exist_ok=True)
        if native_result is not None:
            dump_json(case_out / "native-validation.json", native_result)
        dump_json(case_out / "score.json", result)
        write_text(case_out / "score.md", render_md(result))
        results.append(result)

    if missing and not args.skip_missing:
        print(f"ERROR: {len(missing)} vault(s) missing; use --skip-missing for an intentional partial run", file=sys.stderr)
        return 2

    summary = {
        "run_id": args.run_id,
        "producer": args.producer,
        "scored_at": datetime.now(timezone.utc).isoformat(),
        "interpretation_note": (
            "baseline producer scores measure protocol expressibility / regression; "
            "they are not free-form agent skill proof. Compare agent runs separately."
            if args.producer == "baseline"
            else f"producer={args.producer}"
        ),
        "cases_scored": len(results),
        "missing_vaults": missing,
        "native_checked": not args.no_native_check,
        "native_error_cases": [r.get("case_id") for r in results if r.get("native_validation", {}).get("errors", 0) > 0],
        "mean_score": round(sum(r.get("case_score", 0) for r in results) / len(results), 4) if results else 0.0,
        "results": [
            {
                "case_id": r.get("case_id"),
                "case_score": r.get("case_score"),
                "producer": r.get("producer"),
                "error": r.get("error"),
            }
            for r in results
        ],
    }
    dump_json(out_dir / "summary.json", summary)
    lines = [
        f"# Run `{args.run_id}`",
        "",
        f"- Producer: **{args.producer}**",
        f"- Cases scored: **{summary['cases_scored']}**",
        f"- Mean score: **{summary['mean_score']:.3f}**",
        f"- Missing vaults: {len(missing)}",
        f"- Note: {summary['interpretation_note']}",
        "",
        "| Case | Score |",
        "|------|------:|",
    ]
    for r in sorted(results, key=lambda x: x.get("case_id") or ""):
        lines.append(f"| `{r.get('case_id')}` | {r.get('case_score', 0):.3f} |")
    write_text(out_dir / "summary.md", "\n".join(lines))
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if results else 1


if __name__ == "__main__":
    raise SystemExit(main())
