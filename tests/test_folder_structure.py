from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_folder_structure_documents_core_zones_and_swarm_namespace() -> None:
    text = (ROOT / "references" / "folder-structure.md").read_text(encoding="utf-8")
    for zone in ("00-Scaffold", "01-Evidence", "03-Hypotheses", "05-Analysis", "08-Tooling", "case-logs"):
        assert zone in text
    assert "Swarm/" in text
    assert "Human Gate" in text
    assert "01-Evidence" in text and "لا يكتب" in text
