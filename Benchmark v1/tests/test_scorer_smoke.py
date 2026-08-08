#!/usr/bin/env python3
"""Smoke tests for Benchmark v1 scorer using fixtures."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from score_vault import score  # noqa: E402


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

    def test_good_has_counter_score(self):
        good = score(
            vault=ROOT / "fixtures" / "sample_vault_good",
            gt_path=ROOT / "fixtures" / "sample_vault_good" / "ground_truth.yaml",
            call_audit=False,
        )
        self.assertGreaterEqual(good["metrics"]["counter_hypothesis_quality"]["score"], 0.5)


if __name__ == "__main__":
    unittest.main()
