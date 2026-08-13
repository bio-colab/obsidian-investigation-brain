#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validate Obsidian native formats used by an investigation vault.

The validator is deliberately syntax/graph focused. It does not decide whether
an investigation claim is true; that remains the job of audit_vault.py and a
human gate.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None  # type: ignore

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
WIKILINK_RE = re.compile(r"!?\[\[([^\]]+?)(?:\|[^\]]+)?\]\]")
ALLOWED_NODE_TYPES = {"text", "file", "link", "group"}
ALLOWED_SIDES = {"top", "right", "bottom", "left"}
ALLOWED_ENDS = {"none", "arrow"}


def issue(issues: list[dict[str, Any]], severity: str, code: str, path: str, message: str) -> None:
    issues.append({"severity": severity, "code": code, "path": path, "message": message})


def parse_yaml(text: str) -> Any:
    if yaml is None:
        raise RuntimeError("PyYAML is required: pip install PyYAML")
    return yaml.safe_load(text)


def known_note_names(root: Path) -> set[str]:
    names: set[str] = set()
    for path in root.rglob("*.md"):
        if any(part.startswith(".") for part in path.parts):
            continue
        rel = path.relative_to(root).with_suffix("").as_posix()
        names.update({path.stem, rel, rel.rsplit("/", 1)[-1]})
    return names


def resolve_target(target: str, known: set[str]) -> bool:
    target = target.strip().split("#", 1)[0].split("|", 1)[0].strip()
    if not target:
        return True
    return target in known or target.replace("\\", "/") in known or target.rsplit("/", 1)[-1] in known


def validate_markdown(root: Path, path: Path, known: set[str], issues: list[dict[str, Any]]) -> None:
    rel = path.relative_to(root).as_posix()
    text = path.read_text(encoding="utf-8", errors="replace")
    match = FRONTMATTER_RE.match(text)
    if not match:
        issue(issues, "warning", "MD_NO_FRONTMATTER", rel, "Markdown note has no YAML frontmatter")
    else:
        try:
            data = parse_yaml(match.group(1))
            if data is not None and not isinstance(data, dict):
                issue(issues, "error", "MD_FRONTMATTER_NOT_MAPPING", rel, "frontmatter must parse to a mapping")
        except Exception as exc:
            issue(issues, "error", "MD_INVALID_FRONTMATTER", rel, f"invalid YAML frontmatter: {exc}")
    body = text[match.end():] if match else text
    for link_match in WIKILINK_RE.finditer(body):
        target = link_match.group(1)
        if not resolve_target(target, known):
            issue(issues, "warning", "MD_BROKEN_WIKILINK", rel, f"wikilink target not found: {target}")


def validate_canvas(root: Path, path: Path, issues: list[dict[str, Any]]) -> None:
    rel = path.relative_to(root).as_posix()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        issue(issues, "error", "CANVAS_INVALID_JSON", rel, str(exc))
        return
    if not isinstance(data, dict):
        issue(issues, "error", "CANVAS_NOT_OBJECT", rel, "canvas root must be an object")
        return
    nodes = data.get("nodes", [])
    edges = data.get("edges", [])
    if not isinstance(nodes, list) or not isinstance(edges, list):
        issue(issues, "error", "CANVAS_ARRAYS_REQUIRED", rel, "nodes and edges must be arrays")
        return
    ids: list[str] = []
    node_ids: set[str] = set()
    for index, node in enumerate(nodes):
        if not isinstance(node, dict):
            issue(issues, "error", "CANVAS_NODE_NOT_OBJECT", rel, f"nodes[{index}] must be an object")
            continue
        node_id = node.get("id")
        if not isinstance(node_id, str) or not node_id:
            issue(issues, "error", "CANVAS_NODE_ID_MISSING", rel, f"nodes[{index}] has no id")
        else:
            ids.append(node_id)
            node_ids.add(node_id)
        node_type = node.get("type")
        if node_type not in ALLOWED_NODE_TYPES:
            issue(issues, "error", "CANVAS_NODE_TYPE_INVALID", rel, f"nodes[{index}] has invalid type {node_type!r}")
        for field in ("x", "y", "width", "height"):
            if not isinstance(node.get(field), (int, float)):
                issue(issues, "error", "CANVAS_NODE_GEOMETRY_MISSING", rel, f"nodes[{index}] missing numeric {field}")
        if node_type == "text" and not isinstance(node.get("text"), str):
            issue(issues, "error", "CANVAS_TEXT_MISSING", rel, f"nodes[{index}] text node has no text")
        if node_type == "file" and not isinstance(node.get("file"), str):
            issue(issues, "error", "CANVAS_FILE_MISSING", rel, f"nodes[{index}] file node has no file")
        if node_type == "link" and not isinstance(node.get("url"), str):
            issue(issues, "error", "CANVAS_URL_MISSING", rel, f"nodes[{index}] link node has no url")
    for index, edge in enumerate(edges):
        if not isinstance(edge, dict):
            issue(issues, "error", "CANVAS_EDGE_NOT_OBJECT", rel, f"edges[{index}] must be an object")
            continue
        edge_id = edge.get("id")
        if not isinstance(edge_id, str) or not edge_id:
            issue(issues, "error", "CANVAS_EDGE_ID_MISSING", rel, f"edges[{index}] has no id")
        else:
            ids.append(edge_id)
        for endpoint in ("fromNode", "toNode"):
            if edge.get(endpoint) not in node_ids:
                issue(issues, "error", "CANVAS_DANGLING_EDGE", rel, f"edges[{index}] {endpoint} does not reference a node")
        for side in ("fromSide", "toSide"):
            if side in edge and edge[side] not in ALLOWED_SIDES:
                issue(issues, "error", "CANVAS_SIDE_INVALID", rel, f"edges[{index}] invalid {side}")
        for end in ("fromEnd", "toEnd"):
            if end in edge and edge[end] not in ALLOWED_ENDS:
                issue(issues, "error", "CANVAS_END_INVALID", rel, f"edges[{index}] invalid {end}")
    duplicates = [key for key, count in Counter(ids).items() if count > 1]
    for duplicate in duplicates:
        issue(issues, "error", "CANVAS_DUPLICATE_ID", rel, f"duplicate node/edge id: {duplicate}")


def formula_refs(value: Any) -> set[str]:
    if isinstance(value, str):
        return set(re.findall(r"formula\.([A-Za-z0-9_-]+)", value))
    if isinstance(value, list):
        result: set[str] = set()
        for item in value:
            result.update(formula_refs(item))
        return result
    if isinstance(value, dict):
        result = set()
        for item in value.values():
            result.update(formula_refs(item))
        return result
    return set()


def validate_base(root: Path, path: Path, issues: list[dict[str, Any]]) -> None:
    rel = path.relative_to(root).as_posix()
    try:
        data = parse_yaml(path.read_text(encoding="utf-8"))
    except Exception as exc:
        issue(issues, "error", "BASE_INVALID_YAML", rel, str(exc))
        return
    if not isinstance(data, dict):
        issue(issues, "error", "BASE_NOT_MAPPING", rel, "base root must be a mapping")
        return
    formulas = data.get("formulas") or {}
    if formulas and not isinstance(formulas, dict):
        issue(issues, "error", "BASE_FORMULAS_NOT_MAPPING", rel, "formulas must be a mapping")
        formulas = {}
    refs = formula_refs(data.get("properties")) | formula_refs(data.get("views")) | formula_refs(data.get("summaries"))
    for ref in sorted(refs):
        if ref not in formulas:
            issue(issues, "error", "BASE_UNDEFINED_FORMULA", rel, f"formula.{ref} is referenced but not defined")
    views = data.get("views")
    if views is not None and not isinstance(views, list):
        issue(issues, "error", "BASE_VIEWS_NOT_LIST", rel, "views must be a list")
    if isinstance(views, list):
        for index, view in enumerate(views):
            if not isinstance(view, dict):
                issue(issues, "error", "BASE_VIEW_NOT_OBJECT", rel, f"views[{index}] must be an object")
                continue
            if view.get("type") not in {"table", "cards", "list", "map"}:
                issue(issues, "error", "BASE_VIEW_TYPE_INVALID", rel, f"views[{index}] has invalid type")


def validate(root: Path) -> dict[str, Any]:
    issues: list[dict[str, Any]] = []
    if not root.is_dir():
        raise FileNotFoundError(root)
    known = known_note_names(root)
    for path in sorted(root.rglob("*.md")):
        if any(part.startswith(".") for part in path.relative_to(root).parts):
            continue
        validate_markdown(root, path, known, issues)
    for path in sorted(root.rglob("*.canvas")):
        if any(part.startswith(".") for part in path.relative_to(root).parts):
            continue
        validate_canvas(root, path, issues)
    for path in sorted(root.rglob("*.base")):
        if any(part.startswith(".") for part in path.relative_to(root).parts):
            continue
        validate_base(root, path, issues)
    counts = Counter(item["severity"] for item in issues)
    return {
        "vault": str(root),
        "files": {
            "markdown": len(list(root.rglob("*.md"))),
            "canvas": len(list(root.rglob("*.canvas"))),
            "base": len(list(root.rglob("*.base"))),
        },
        "issues": issues,
        "score": {"errors": counts.get("error", 0), "warnings": counts.get("warning", 0), "total": len(issues)},
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Obsidian native formats")
    parser.add_argument("vault", help="vault root")
    parser.add_argument("--json", help="write JSON result")
    parser.add_argument("--strict", action="store_true", help="fail on warnings as well as errors")
    args = parser.parse_args()
    try:
        result = validate(Path(args.vault))
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    if args.json:
        Path(args.json).write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    errors = result["score"]["errors"]
    warnings = result["score"]["warnings"]
    return 1 if errors or (args.strict and warnings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
