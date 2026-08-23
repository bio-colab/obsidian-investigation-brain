from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from audit_vault import audit_vault  # noqa: E402
import case_memory  # noqa: E402


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


def test_audit_accepts_working_memory_snapshot(tmp_path: Path) -> None:
    make_base(tmp_path)
    case_memory.append_event(tmp_path, "session.init", summary="test")
    case_memory.write_snapshot(tmp_path)
    result = audit_vault(tmp_path)
    assert not any(issue["code"] == "INVALID_STATUS" for issue in result["issues"])
    assert result["memory_snapshot_present"] is True


def test_audit_flags_traversal_write_target_despite_prefix(tmp_path: Path) -> None:
    make_base(tmp_path)
    manifests = tmp_path / "08-Tooling" / "Manifests"
    manifests.mkdir(parents=True)
    for target in (
        "08-Tooling/../../99-Attachments/x",
        "01-Evidence/leak",
        "/etc/passwd",
        "C:/Windows/Temp",
    ):
        manifest = manifests / "TOOL-EVIL.md"
        manifest.write_text(
            "---\n"
            "type: tool-manifest\n"
            "status: draft\n"
            f"tool-id: TOOL-EVIL\nversion: 0.1.0\nentrypoint: 08-Tooling/Active/tool.py\nnetwork: denied\nwrites-to: [\"{target}\"]\n"
            "---\n# Tool\n",
            encoding="utf-8",
        )
        result = audit_vault(tmp_path)
        codes = {issue["code"] for issue in result["issues"]}
        assert "TOOL_MANIFEST_WRITE_ESCAPE" in codes, target


def _write_note(root: Path, rel: str, front: str, body: str = "body\n") -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"---\n{front}\n---\n# Note\n\n{body}", encoding="utf-8")


def _write_plan_and_ledger(root: Path, phases: int, ledger_rows: int) -> None:
    plan_items = "\n".join(f"{i}. **Phase {i}** — do things." for i in range(1, phases + 1))
    _write_note(
        root,
        "00-Scaffold/Investigation-Plan.md",
        "type: investigation-plan\nstatus: working\ncreated: 2026-01-01\nupdated: 2026-01-01",
        f"\n{plan_items}\n",
    )
    rows = "\n".join(f"| Phase {i} | evidence rows | covered | none |" for i in range(1, ledger_rows + 1))
    table = "| المرحلة | صفوف الأدلة | تغطية | gaps |\n|---|---|---|---|\n" + (rows + "\n" if rows else "")
    _write_note(
        root,
        "00-Scaffold/Coverage-Ledger.md",
        "type: coverage-ledger\nstatus: working\ncreated: 2026-01-01\nupdated: 2026-01-01",
        f"\n{table}",
    )


def test_audit_measures_empty_coverage_ledger(tmp_path: Path) -> None:
    make_base(tmp_path)
    _write_plan_and_ledger(tmp_path, phases=3, ledger_rows=0)
    result = audit_vault(tmp_path)
    codes = {issue["code"] for issue in result["issues"]}
    assert "COVERAGE_LEDGER_EMPTY" in codes
    info = result["coverage_intelligence"]
    assert info is not None and info["plan_phases"] == 3 and info["coverage_pct"] == 0


def test_audit_flags_partial_and_low_ledger_coverage(tmp_path: Path) -> None:
    make_base(tmp_path)
    _write_plan_and_ledger(tmp_path, phases=3, ledger_rows=2)
    result = audit_vault(tmp_path)
    codes = {issue["code"] for issue in result["issues"]}
    assert "COVERAGE_LEDGER_PARTIAL" in codes
    assert abs(result["coverage_intelligence"]["coverage_pct"] - 67) <= 1
    make_base2 = tmp_path  # reuse fixture for LOW threshold
    _write_plan_and_ledger(make_base2, phases=10, ledger_rows=3)
    result_low = audit_vault(make_base2)
    codes_low = {issue["code"] for issue in result_low["issues"]}
    assert "COVERAGE_LEDGER_LOW" in codes_low


def test_audit_flags_strong_hypothesis_on_unresolved_contradiction(tmp_path: Path) -> None:
    make_base(tmp_path)
    _write_note(
        tmp_path,
        "03-Hypotheses/Primary/H-P1.md",
        (
            "type: hypothesis\nstatus: draft\ncreated: 2026-01-01\nupdated: 2026-01-01\n"
            'hypothesis-kind: primary\nsupport-level: strong\nsupporting-notes: ["[[EV-A]]", "[[EV-B]]"]\n'
            'counter-hypothesis: "[[H-C1]]"'
        ),
    )
    _write_note(
        tmp_path,
        "04-Timeline/Contradictions/CON-X.md",
        (
            "type: contradiction\nstatus: pending-human-review\ncreated: 2026-01-01\nupdated: 2026-01-01\n"
            'between: ["[[EV-A]]", "[[EV-B]]"]'
        ),
    )
    result = audit_vault(tmp_path)
    majors = {(i["code"], i["severity"]) for i in result["issues"]}
    assert ("HYPOTHESIS_STRONG_ON_CONTRADICTION", "major") in majors


def test_audit_skips_rejected_hypotheses_in_contradiction_rule(tmp_path: Path) -> None:
    make_base(tmp_path)
    _write_note(
        tmp_path,
        "03-Hypotheses/Rejected/H-R1.md",
        (
            "type: hypothesis\nstatus: rejected\ncreated: 2026-01-01\nupdated: 2026-01-01\n"
            'hypothesis-kind: rejected\nsupport-level: weak\nsupporting-notes: ["[[EV-A]]"]\n'
            "reject-reason: superseded by DNA evidence"
        ),
    )
    _write_note(
        tmp_path,
        "04-Timeline/Contradictions/CON-X.md",
        (
            "type: contradiction\nstatus: pending-human-review\ncreated: 2026-01-01\nupdated: 2026-01-01\n"
            'between: ["[[EV-A]]", "[[EV-B]]"]'
        ),
    )
    result = audit_vault(tmp_path)
    codes = {issue["code"] for issue in result["issues"]}
    assert not any(c.startswith("HYPOTHESIS_") and c.endswith("_CONTRADICTION") for c in codes)


def test_contradiction_undermines_field_takes_precedence(tmp_path: Path) -> None:
    make_base(tmp_path)
    _write_note(
        tmp_path,
        "03-Hypotheses/Primary/H-P1.md",
        (
            "type: hypothesis\nstatus: draft\ncreated: 2026-01-01\nupdated: 2026-01-01\n"
            'hypothesis-kind: primary\nsupport-level: strong\nsupporting-notes: ["[[EV-A]]", "[[EV-C]]"]\n'
            'counter-hypothesis: "[[H-C1]]"'
        ),
    )
    # The contradiction pits EV-A against EV-B; H-P1 rests on the survivor side.
    _write_note(
        tmp_path,
        "04-Timeline/Contradictions/CON-X.md",
        (
            "type: contradiction\nstatus: pending-human-review\ncreated: 2026-01-01\nupdated: 2026-01-01\n"
            'between: ["[[EV-A]]", "[[EV-B]]"]\nundermines: ["[[EV-B]]"]'
        ),
    )
    result_ok = audit_vault(tmp_path)
    assert not any(
        i["code"] == "HYPOTHESIS_STRONG_ON_CONTRADICTION" and i["path"].endswith("H-P1.md")
        for i in result_ok["issues"]
    )
    # Flip: undermine the very evidence the hypothesis rests on -> must flag.
    note2 = tmp_path / "04-Timeline/Contradictions/CON-X.md"
    note2.write_text(note2.read_text(encoding="utf-8").replace('undermines: ["[[EV-B]]"]', 'undermines: ["[[EV-A]]"]'), encoding="utf-8")
    result_flag = audit_vault(tmp_path)
    assert any(i["code"] == "HYPOTHESIS_STRONG_ON_CONTRADICTION" for i in result_flag["issues"])


def test_audit_conclusive_requires_multiple_supporting_notes(tmp_path: Path) -> None:
    make_base(tmp_path)
    _write_note(
        tmp_path,
        "03-Hypotheses/Alternative/H-A1.md",
        (
            "type: hypothesis\nstatus: draft\ncreated: 2026-01-01\nupdated: 2026-01-01\n"
            'hypothesis-kind: alternative\nsupport-level: conclusive\nsupporting-notes: ["[[EV-ONLY]]"]'
        ),
    )
    result = audit_vault(tmp_path)
    codes = {issue["code"] for issue in result["issues"]}
    assert "CONCLUSIVE_NEEDS_MULTIPLE_SUPPORT" in codes


def test_group_victim_name_rule_fires_on_fabricated_person(tmp_path: Path) -> None:
    make_base(tmp_path)
    _write_note(
        tmp_path,
        "02-Entities/Persons/Groups/GRP-V.md",
        (
            "type: group-entity\nstatus: verified\ncreated: 2026-01-01\nupdated: 2026-01-01\n"
            "role: victims\nnamed-individuals: []"
        ),
    )
    _write_note(
        tmp_path,
        "02-Entities/Persons/Victims/PER-JOHNDOE.md",
        (
            "type: person\nstatus: verified\ncreated: 2026-01-01\nupdated: 2026-01-01\n"
            "role: victim"
        ),
        "\n# John Doe\n",
    )
    result = audit_vault(tmp_path)
    codes = {issue["code"] for issue in result["issues"]}
    assert "GROUP_VICTIM_NAME_WITH_EMPTY_GROUP" in codes
