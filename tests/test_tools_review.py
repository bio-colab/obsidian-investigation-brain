from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

_spec = importlib.util.spec_from_file_location("tools_review", ROOT / "scripts" / "tools-review.py")
tools_review = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(tools_review)


def _seed_case(tmp_path: Path) -> Path:
    active = tmp_path / "08-Tooling" / "Active"
    active.mkdir(parents=True)
    (active / "tool.py").write_text("print('x')\n", encoding="utf-8")
    audits = tmp_path / "08-Tooling" / "Audits"
    audits.mkdir(parents=True)
    entrypoint = "08-Tooling/Active/tool.py"
    # AAA sorts first alphabetically but records the older run.
    (audits / "AAA.json").write_text(
        json.dumps({"entrypoint": entrypoint, "exit_code": 1, "started_at": "2026-01-01T00:00:00+00:00"}),
        encoding="utf-8",
    )
    (audits / "ZZZ.json").write_text(
        json.dumps({"entrypoint": entrypoint, "exit_code": 0, "started_at": "2026-02-01T00:00:00+00:00"}),
        encoding="utf-8",
    )
    return tmp_path


def test_review_picks_latest_audit_by_timestamp(tmp_path: Path) -> None:
    root = _seed_case(tmp_path)
    result = tools_review.review(root)
    assert result["suggestions"], "expected at least one suggestion"
    suggestion = next(s for s in result["suggestions"] if s["path"] == "08-Tooling/Active/tool.py")
    assert suggestion["action"] == "review-for-promotion"


def test_early_return_includes_generated_at(tmp_path: Path) -> None:
    result = tools_review.review(tmp_path)
    assert result.get("generated_at")


def test_decision_markdown_is_sanitized(tmp_path: Path) -> None:
    active = tmp_path / "08-Tooling" / "Active"
    active.mkdir(parents=True)
    tool = active / "tool.py"
    tool.write_text("print('x')\n", encoding="utf-8")
    tools_review.apply_move(tmp_path, ["08-Tooling/Active/tool.py"], "Archive", "bad | row\nnew line")
    log = (tmp_path / "case-logs" / "decisions.md").read_text(encoding="utf-8")
    table_rows = [line for line in log.splitlines() if line.startswith("|")]
    assert len(table_rows) == 1
    assert "\\|" in table_rows[0]
