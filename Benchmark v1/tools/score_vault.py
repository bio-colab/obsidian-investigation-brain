#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Score one investigation vault against a case ground_truth.yaml."""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

# allow running as script
sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.io_utils import benchmark_root, dump_json, load_yaml, write_text
from lib.metrics import (
    score_conclusion_calibration,
    score_confirmation_bias,
    score_contradictions,
    score_counter_quality,
    score_evidence_coverage,
    score_false_inference,
    score_hypothesis_coverage,
    score_missing_evidence,
    score_readiness_gate,
    score_report_traceability,
    score_source_provenance,
    score_timeline,
    weighted_case_score,
)
from lib.skill_audit import run_skill_audit
from lib.vault_parse import load_vault


def render_md(result: dict) -> str:
    lines = [
        f"# Benchmark score - `{result.get('case_id')}`",
        "",
        f"- **Case score:** {result['case_score']:.3f}",
        f"- **Vault:** `{result.get('vault_path')}`",
        f"- **Scored at:** {result.get('scored_at')}",
        "",
        "## Metrics",
        "",
        "| Metric | ID | Score |",
        "|--------|----|------:|",
    ]
    for key, m in result.get("metrics", {}).items():
        lines.append(f"| {key} | {m.get('id')} | {m.get('score', 0):.3f} |")
    lines.append("")
    if result.get("hard_fails"):
        lines.append("## Hard fails")
        lines.append("")
        for hf in result["hard_fails"]:
            lines.append(f"- **{hf.get('code')}**: {hf.get('msg')}")
        lines.append("")
    audit = result.get("skill_audit") or {}
    if audit:
        score = audit.get("score") or {}
        lines.append("## Skill audit (appendix)")
        lines.append("")
        lines.append(
            f"- critical: {score.get('critical', audit.get('critical', 'n/a'))} · "
            f"major: {score.get('major', 'n/a')} · minor: {score.get('minor', 'n/a')}"
        )
        lines.append("")
    return "\n".join(lines)


def detect_hard_fails(gt: dict, metrics: dict, cfg: dict) -> list[dict]:
    fails = []
    codes = set((cfg.get("scoring") or {}).get("hard_fail_codes") or [])
    if not (cfg.get("scoring") or {}).get("hard_fail_enabled"):
        return fails
    fi = metrics.get("false_inference_rate") or {}
    for hit in fi.get("details") or []:
        if hit.get("type") == "entity" and "FORBIDDEN_ENTITY_INVENTED" in codes:
            fails.append({"code": "FORBIDDEN_ENTITY_INVENTED", "msg": str(hit)})
        if hit.get("type") == "inference" and "FORBIDDEN_EVIDENCE_INVENTED" in codes:
            fails.append({"code": "FORBIDDEN_EVIDENCE_INVENTED", "msg": str(hit)})
    for v in (metrics.get("readiness_gate_violations") or {}).get("details") or []:
        if v.get("code") == "court_file_against_expectation" and "COURT_FILE_WITHOUT_READINESS" in codes:
            fails.append({"code": "COURT_FILE_WITHOUT_READINESS", "msg": v.get("path", "")})
        if v.get("code") == "verified_without_source" and "VERIFIED_WITHOUT_SOURCE" in codes:
            fails.append({"code": "VERIFIED_WITHOUT_SOURCE", "msg": v.get("path", "")})
    return fails


def score(
    vault: Path,
    gt_path: Path,
    case_id: str | None = None,
    config_path: Path | None = None,
    call_audit: bool = True,
    producer: str = "unspecified",
) -> dict:
    root = benchmark_root()
    cfg_path = config_path or (root / "config.yaml")
    cfg = load_yaml(cfg_path) if cfg_path.is_file() else {}
    rubrics = load_yaml(root / "rubrics" / "scoring.yaml")
    gt = load_yaml(gt_path)
    case_id = case_id or gt.get("case_id") or vault.name
    idx = load_vault(vault)

    thr = float((cfg.get("scoring") or {}).get("text_similarity_threshold", 0.55))
    date_tol = int((cfg.get("scoring") or {}).get("date_tolerance_days", 1))
    weights = (cfg.get("scoring") or {}).get("weights") or {}
    vcap = int(((rubrics.get("metrics") or {}).get("readiness_gate_violations") or {}).get("violation_cap", 5))
    matrix = ((rubrics.get("metrics") or {}).get("final_conclusion_calibration") or {}).get("calibration_matrix") or {}

    # Producer-aware hard-fail: agent on by default; baseline off unless scoring.hard_fail_enabled
    run_cfg = cfg.get("run") or {}
    scoring_cfg = dict(cfg.get("scoring") or {})
    if producer == "agent":
        scoring_cfg["hard_fail_enabled"] = bool(
            run_cfg.get("agent_hard_fail_enabled", True) or scoring_cfg.get("hard_fail_enabled")
        )
    elif producer == "baseline":
        scoring_cfg["hard_fail_enabled"] = bool(
            run_cfg.get("baseline_hard_fail_enabled", False) and scoring_cfg.get("hard_fail_enabled", False)
        )
    cfg_eff = {**cfg, "scoring": scoring_cfg}

    skill_audit = None
    if call_audit and (cfg.get("run") or {}).get("call_skill_audit", True):
        audit_rel = (cfg.get("paths") or {}).get("audit_script", "../scripts/audit_vault.py")
        audit_script = (root / audit_rel).resolve()
        skill_audit = run_skill_audit(vault, audit_script)

    metrics = {
        "evidence_coverage": score_evidence_coverage(gt, idx, thr),
        "source_provenance_completeness": score_source_provenance(gt, idx, thr),
        "hypothesis_coverage": score_hypothesis_coverage(gt, idx, thr),
        "counter_hypothesis_quality": score_counter_quality(gt, idx, thr),
        "timeline_reconstruction": score_timeline(gt, idx, thr, date_tol),
        "contradiction_detection": score_contradictions(gt, idx, thr),
        "missing_evidence_detection": score_missing_evidence(gt, idx, thr),
        "false_inference_rate": score_false_inference(gt, idx),
        "confirmation_bias_resistance": score_confirmation_bias(gt, idx, thr),
        "report_traceability": score_report_traceability(gt, idx, thr),
        "readiness_gate_violations": score_readiness_gate(gt, idx, skill_audit, vcap),
        "final_conclusion_calibration": score_conclusion_calibration(gt, idx, thr, matrix),
    }

    case_score = weighted_case_score(metrics, weights)
    hard_fails = detect_hard_fails(gt, metrics, cfg_eff)
    if hard_fails and scoring_cfg.get("hard_fail_enabled"):
        case_score = 0.0

    result = {
        "benchmark_version": "1.0.0",
        "case_id": case_id,
        "producer": producer,
        "hard_fail_enabled": bool(scoring_cfg.get("hard_fail_enabled")),
        "vault_path": str(vault),
        "ground_truth": str(gt_path),
        "scored_at": datetime.now(timezone.utc).isoformat(),
        "case_score": round(case_score, 4),
        "metrics": metrics,
        "hard_fails": hard_fails,
        "skill_audit": {
            "score": (skill_audit or {}).get("score"),
            "issues_count": len((skill_audit or {}).get("issues") or []),
            "critical": sum(1 for i in (skill_audit or {}).get("issues") or [] if i.get("severity") == "critical"),
            "error": (skill_audit or {}).get("error"),
        }
        if skill_audit is not None
        else None,
        "vault_stats": {
            "notes_total": len(idx.notes),
            "by_type_top": sorted(
                ((t, len(ns)) for t, ns in idx.by_type.items()),
                key=lambda x: -x[1],
            )[:15],
        },
    }
    return result


def main() -> int:
    ap = argparse.ArgumentParser(description="Score an investigation vault vs ground truth")
    ap.add_argument("--vault", required=True, help="Path to vault root")
    ap.add_argument("--ground-truth", required=True, help="Path to ground_truth.yaml")
    ap.add_argument("--case-id", default=None)
    ap.add_argument("--config", default=None)
    ap.add_argument("--out", default=None, help="Write JSON result")
    ap.add_argument("--md", default=None, help="Write Markdown report")
    ap.add_argument("--no-audit", action="store_true")
    ap.add_argument(
        "--producer",
        default="unspecified",
        choices=["baseline", "agent", "adversarial", "unspecified"],
        help="Who produced the vault (do not mix baseline with agent when reporting skill quality)",
    )
    args = ap.parse_args()

    result = score(
        vault=Path(args.vault),
        gt_path=Path(args.ground_truth),
        case_id=args.case_id,
        config_path=Path(args.config) if args.config else None,
        call_audit=not args.no_audit,
        producer=args.producer,
    )

    if args.out:
        dump_json(Path(args.out), result)
        print(f"JSON -> {args.out}", file=sys.stderr)
    if args.md:
        write_text(Path(args.md), render_md(result))
        print(f"MD   -> {args.md}", file=sys.stderr)
    if not args.out and not args.md:
        dump_json  # silence linter
        import json

        print(json.dumps(result, ensure_ascii=False, indent=2))

    print(f"case_score={result['case_score']:.4f} case_id={result['case_id']}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
