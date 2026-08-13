from __future__ import annotations

import json
import sys
from argparse import Namespace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import case_tooling  # noqa: E402
import validate_obsidian_native  # noqa: E402


def write_valid_vault(root: Path) -> None:
    (root / "00-Scaffold").mkdir(parents=True)
    (root / "00-Scaffold" / "Case-Scope.md").write_text(
        "---\ntype: case-scope\nstatus: verified\ncreated: 2026-01-01\nupdated: 2026-01-01\n---\n# Scope\n",
        encoding="utf-8",
    )
    (root / "00-Scaffold" / "Map.canvas").write_text(
        json.dumps(
            {
                "nodes": [
                    {"id": "a", "type": "file", "x": 0, "y": 0, "width": 300, "height": 200, "file": "00-Scaffold/Case-Scope.md"},
                    {"id": "b", "type": "text", "x": 400, "y": 0, "width": 300, "height": 200, "text": "# Analysis"},
                ],
                "edges": [{"id": "ab", "fromNode": "a", "toNode": "b", "toEnd": "arrow"}],
            }
        ),
        encoding="utf-8",
    )
    (root / "00-Scaffold" / "Index.base").write_text(
        "filters: 'status == \"draft\"'\nformulas:\n  label: 'if(status, status, \"unknown\")'\nviews:\n  - type: table\n    name: \"Drafts\"\n    order:\n      - file.name\n      - formula.label\n",
        encoding="utf-8",
    )


def test_native_validator_accepts_valid_files(tmp_path: Path) -> None:
    write_valid_vault(tmp_path)
    result = validate_obsidian_native.validate(tmp_path)
    assert result["score"]["errors"] == 0


def test_native_validator_rejects_dangling_canvas_edge(tmp_path: Path) -> None:
    write_valid_vault(tmp_path)
    canvas = tmp_path / "00-Scaffold" / "Map.canvas"
    data = json.loads(canvas.read_text(encoding="utf-8"))
    data["edges"][0]["toNode"] = "missing"
    canvas.write_text(json.dumps(data), encoding="utf-8")
    result = validate_obsidian_native.validate(tmp_path)
    assert any(item["code"] == "CANVAS_DANGLING_EDGE" for item in result["issues"])


def test_manifest_rejects_write_escape(tmp_path: Path) -> None:
    (tmp_path / "08-Tooling/Active").mkdir(parents=True)
    entry = tmp_path / "08-Tooling/Active/tool.py"
    entry.write_text("print('ok')\n", encoding="utf-8")
    manifest = tmp_path / "manifest.yaml"
    manifest.write_text(
        "tool-id: TOOL-001\nversion: 0.1.0\nentrypoint: 08-Tooling/Active/tool.py\nnetwork: denied\nwrites-to: [01-Evidence/]\n",
        encoding="utf-8",
    )
    errors = case_tooling.validate_manifest(tmp_path, manifest)
    assert any("outside allowed prefixes" in error for error in errors)


def test_markdown_manifest_is_supported(tmp_path: Path) -> None:
    (tmp_path / "08-Tooling/Active").mkdir(parents=True)
    (tmp_path / "08-Tooling/Active/tool.py").write_text("print('ok')\n", encoding="utf-8")
    manifest = tmp_path / "08-Tooling/Manifests/TOOL-001.md"
    manifest.parent.mkdir(parents=True)
    manifest.write_text(
        "---\ntool-id: TOOL-001\nversion: 0.1.0\nentrypoint: 08-Tooling/Active/tool.py\nnetwork: denied\nwrites-to: [08-Tooling/Runs/]\n---\n# Tool\n",
        encoding="utf-8",
    )
    assert case_tooling.load_manifest(manifest)["tool-id"] == "TOOL-001"
    assert case_tooling.validate_manifest(tmp_path, manifest) == []


def test_executor_is_fail_closed_without_backend(tmp_path: Path) -> None:
    (tmp_path / "08-Tooling/Active").mkdir(parents=True)
    (tmp_path / "08-Tooling/Active/tool.py").write_text("print('must not run')\n", encoding="utf-8")
    manifest = tmp_path / "08-Tooling/manifest.yaml"
    manifest.write_text(
        "tool-id: TOOL-001\nversion: 0.1.0\nentrypoint: 08-Tooling/Active/tool.py\nnetwork: denied\nwrites-to: [08-Tooling/Runs/]\n",
        encoding="utf-8",
    )
    code = case_tooling.run_tool(
        Namespace(
            case_root=str(tmp_path),
            manifest=str(manifest),
            backend="auto",
            allow_host=False,
            run_id="RUN-TEST",
            output_dir="08-Tooling/Runs",
            timeout=10,
            tool_arg=[],
        )
    )
    assert code == 3
    log = tmp_path / "case-logs" / "tool-runs.jsonl"
    assert log.exists()
    assert "tool.run.skipped" in log.read_text(encoding="utf-8")
