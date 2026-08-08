#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Aggregate per-case score.json files into run-level metrics."""

from __future__ import annotations

import argparse
import csv
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.io_utils import benchmark_root, dump_json, load_json, write_text

METRIC_KEYS = [
    "evidence_coverage",
    "source_provenance_completeness",
    "hypothesis_coverage",
    "counter_hypothesis_quality",
    "timeline_reconstruction",
    "contradiction_detection",
    "missing_evidence_detection",
    "false_inference_rate",
    "confirmation_bias_resistance",
    "report_traceability",
    "readiness_gate_violations",
    "final_conclusion_calibration",
]


def mean(xs: list[float]) -> float:
    return sum(xs) / len(xs) if xs else 0.0


def median(xs: list[float]) -> float:
    if not xs:
        return 0.0
    s = sorted(xs)
    n = len(s)
    mid = n // 2
    if n % 2:
        return s[mid]
    return 0.5 * (s[mid - 1] + s[mid])


def stdev(xs: list[float]) -> float:
    if len(xs) < 2:
        return 0.0
    m = mean(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--results-dir", default=None, help="Default: Benchmark v1/results/runs/<run-id>")
    args = ap.parse_args()

    root = benchmark_root()
    run_dir = Path(args.results_dir) if args.results_dir else root / "results" / "runs" / args.run_id
    if not run_dir.is_dir():
        print(f"ERROR: run dir not found: {run_dir}", file=sys.stderr)
        return 2

    scores = []
    for p in sorted(run_dir.glob("*/score.json")):
        try:
            scores.append(load_json(p))
        except Exception as e:
            print(f"WARN: {p}: {e}", file=sys.stderr)

    if not scores:
        print("ERROR: no score.json found", file=sys.stderr)
        return 1

    case_scores = [float(s.get("case_score") or 0.0) for s in scores]
    per_metric: dict[str, list[float]] = {k: [] for k in METRIC_KEYS}
    for s in scores:
        metrics = s.get("metrics") or {}
        for k in METRIC_KEYS:
            if k in metrics and "score" in metrics[k]:
                per_metric[k].append(float(metrics[k]["score"]))

    producers = sorted({s.get("producer") or "unspecified" for s in scores})
    agg = {
        "run_id": args.run_id,
        "producers": producers,
        "interpretation_note": (
            "If producers include only 'baseline', treat as structural regression — not free-form agent proof."
        ),
        "n_cases": len(scores),
        "case_score": {
            "mean": round(mean(case_scores), 4),
            "median": round(median(case_scores), 4),
            "stdev": round(stdev(case_scores), 4),
            "min": round(min(case_scores), 4),
            "max": round(max(case_scores), 4),
        },
        "metrics_mean": {k: round(mean(vs), 4) for k, vs in per_metric.items()},
        "metrics_stdev": {k: round(stdev(vs), 4) for k, vs in per_metric.items()},
        "leaderboard": sorted(
            [{"case_id": s.get("case_id"), "case_score": s.get("case_score")} for s in scores],
            key=lambda x: (-(x["case_score"] or 0), x["case_id"] or ""),
        ),
        "hard_fail_cases": [
            s.get("case_id") for s in scores if s.get("hard_fails")
        ],
    }

    dump_json(run_dir / "aggregate.json", agg)

    # CSV
    csv_path = run_dir / "aggregate.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["case_id", "case_score"] + METRIC_KEYS)
        for s in sorted(scores, key=lambda x: x.get("case_id") or ""):
            row = [s.get("case_id"), s.get("case_score")]
            metrics = s.get("metrics") or {}
            for k in METRIC_KEYS:
                row.append((metrics.get(k) or {}).get("score"))
            w.writerow(row)

    lines = [
        f"# Aggregate — run `{args.run_id}`",
        "",
        f"- Producers: **{', '.join(agg['producers'])}**",
        f"- N cases: **{agg['n_cases']}**",
        f"- Mean: **{agg['case_score']['mean']:.3f}** · Median: **{agg['case_score']['median']:.3f}** · Stdev: **{agg['case_score']['stdev']:.3f}**",
        f"- Range: {agg['case_score']['min']:.3f} – {agg['case_score']['max']:.3f}",
        f"- Note: {agg['interpretation_note']}",
        "",
        "## Per-metric means",
        "",
        "| Metric | Mean | Stdev |",
        "|--------|-----:|------:|",
    ]
    for k in METRIC_KEYS:
        lines.append(f"| {k} | {agg['metrics_mean'].get(k, 0):.3f} | {agg['metrics_stdev'].get(k, 0):.3f} |")
    lines += ["", "## Leaderboard", ""]
    for i, row in enumerate(agg["leaderboard"], 1):
        lines.append(f"{i}. `{row['case_id']}` — {row['case_score']:.3f}")
    write_text(run_dir / "aggregate.md", "\n".join(lines))

    print(f"Wrote {run_dir / 'aggregate.json'}")
    print(f"Wrote {csv_path}")
    print(f"Wrote {run_dir / 'aggregate.md'}")
    print(f"mean_case_score={agg['case_score']['mean']:.4f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
