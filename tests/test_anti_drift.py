from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_anti_drift_defines_evidence_and_human_gate_rules() -> None:
    text = (ROOT / "references" / "anti-drift-rules.md").read_text(encoding="utf-8")
    assert "Evidence" in text
    assert "Human Gate" in text
    assert "الفرضيات المضادة" in text
    assert "Chain-of-Custody" in text or "سلسلة الحفظ" in text
