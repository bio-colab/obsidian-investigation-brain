#!/usr/bin/env python3
"""Smoke tests for Benchmark v1 scorer using fixtures."""

from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from score_vault import score  # noqa: E402
import run_benchmark  # noqa: E402


class ScorerSmoke(unittest.TestCase):
    def test_good_beats_bad(self):
        good = score(
            vault=ROOT / "fixtures" / "sample_vault_good",
            gt_path=ROOT / "fixtures" / "sample_vault_good" / "ground_truth.yaml",
            case_id="FIXTURE-GOOD",
            call_audit=False,
        )
        bad = score(
            vault=ROOT / "fixtures" / "sample_vault_bad",
            gt_path=ROOT / "fixtures" / "sample_vault_bad" / "ground_truth.yaml",
            case_id="FIXTURE-BAD",
            call_audit=False,
        )
        self.assertGreater(good["case_score"], bad["case_score"])
        self.assertGreaterEqual(good["case_score"], 0.45)
        self.assertLessEqual(bad["case_score"], 0.55)

    def test_false_inference_penalizes_bad(self):
        bad = score(
            vault=ROOT / "fixtures" / "sample_vault_bad",
            gt_path=ROOT / "fixtures" / "sample_vault_bad" / "ground_truth.yaml",
            call_audit=False,
        )
        self.assertLess(bad["metrics"]["false_inference_rate"]["score"], 1.0)

    def test_missing_vaults_fail_by_default(self):
        run_id = "test-missing-vaults"
        output = ROOT / "results" / "runs" / run_id
        with tempfile.TemporaryDirectory() as td:
            cases_dir = Path(td) / "cases" / "CASE-TEST-MISSING"
            cases_dir.mkdir(parents=True)
            (cases_dir / "ground_truth.yaml").write_text("case_id: CASE-TEST-MISSING\n", encoding="utf-8")
            vaults_root = Path(td) / "vaults"
            try:
                with patch.object(
                    sys,
                    "argv",
                    [
                        "run_benchmark.py",
                        "--run-id",
                        run_id,
                        "--vaults-root",
                        str(vaults_root),
                        "--cases-dir",
                        str(Path(td) / "cases"),
                    ],
                ):
                    self.assertEqual(run_benchmark.main(), 2)
            finally:
                shutil.rmtree(output, ignore_errors=True)

    def test_good_has_counter_score(self):
        good = score(
            vault=ROOT / "fixtures" / "sample_vault_good",
            gt_path=ROOT / "fixtures" / "sample_vault_good" / "ground_truth.yaml",
            call_audit=False,
        )
        self.assertGreaterEqual(good["metrics"]["counter_hypothesis_quality"]["score"], 0.5)


if __name__ == "__main__":
    unittest.main()
