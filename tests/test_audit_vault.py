from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from audit_vault import audit_vault  # noqa: E402


CRITICAL = (
    "00-Scaffold/AGENTS.md",
    "00-Scaffold/Case-Scope.md",
    "00-Scaffold/Investigation-Plan.md",
    "00-Scaffold/Coverage-Ledger.md",
    "00-Scaffold/Review-Queue.md",
)


def make_base(root: Path) -> None:
    for rel in CRITICAL:
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"# {path.stem}\n", encoding="utf-8")
    (root / "01-Evidence").mkdir(parents=True, exist_ok=True)


def test_audit_flags_verified_evidence_without_coc(tmp_path: Path) -> None:
    make_base(tmp_path)
    (tmp_path / "01-Evidence" / "EV-001.md").write_text(
        """---
type: digital-evidence
status: verified
created: 2026-01-01
updated: 2026-01-01
evidence-id: EV-001
---
Verified claim without a custody record.
""",
        encoding="utf-8",
    )
    result = audit_vault(tmp_path)
    codes = {issue["code"] for issue in result["issues"]}
    assert "EVIDENCE_NO_COC" in codes


def test_audit_accepts_unverified_evidence_with_valid_coc(tmp_path: Path) -> None:
    make_base(tmp_path)
    (tmp_path / "01-Evidence" / "EV-002.md").write_text(
        """---
type: digital-evidence
status: unverified
created: 2026-01-01
updated: 2026-01-01
evidence-id: EV-002
chain-of-custody: "[[COC-002]]"
---
Unverified training note.
""",
        encoding="utf-8",
    )
    (tmp_path / "01-Evidence" / "COC-002.md").write_text(
        """---
type: chain-of-custody
status: draft
created: 2026-01-01
updated: 2026-01-01
evidence-ref: "[[EV-002]]"
---
Custody record for the training note.
""",
        encoding="utf-8",
    )
    result = audit_vault(tmp_path)
    codes = {issue["code"] for issue in result["issues"]}
    assert "EVIDENCE_NO_COC" not in codes
    assert result["evidence_count"] == 1
