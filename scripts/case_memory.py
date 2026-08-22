#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Append-only external case memory and compact decision-trace snapshots.

This records observable work facts (decisions, observations, uncertainty,
references, and next actions), not hidden chain-of-thought. The JSONL stream is
the durable source; the Markdown snapshot is a compact recovery view.
"""
from __future__ import annotations

import argparse
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


MEMORY_DIR = "case-logs"
SESSION_LOG = "session.jsonl"
TOOL_LOG = "tool-runs.jsonl"
SNAPSHOT = "memory-snapshot.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _append_jsonl(path: Path, row: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def append_event(
    case_root: Path,
    event: str,
    *,
    tool_event: bool = False,
    **payload: Any,
) -> dict[str, Any]:
    """Append one structured event to the durable session stream.

    Tool events are additionally indexed in tool-runs.jsonl for fast review.
    """
    row = {"ts": now(), "event_id": f"EV-{uuid.uuid4().hex[:12]}", "event": event, **payload}
    log_root = case_root / MEMORY_DIR
    _append_jsonl(log_root / SESSION_LOG, row)
    if tool_event:
        _append_jsonl(log_root / TOOL_LOG, row)
    return row


def read_events(case_root: Path) -> tuple[list[dict[str, Any]], int]:
    path = case_root / MEMORY_DIR / SESSION_LOG
    events: list[dict[str, Any]] = []
    invalid = 0
    if not path.exists():
        return events, invalid
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            invalid += 1
            continue
        if isinstance(row, dict):
            events.append(row)
        else:
            invalid += 1
    return events, invalid


def _clean(value: Any, limit: int = 280) -> str:
    if value is None:
        return ""
    text = str(value).replace("\n", " ").strip()
    return text if len(text) <= limit else text[: limit - 1] + "…"


def _refs(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    return [str(value)]


def render_snapshot(case_root: Path, *, last: int = 20) -> str:
    events, invalid = read_events(case_root)
    recent = events[-max(1, last) :]
    lines = [
        "---",
        "type: case-memory-snapshot",
        "status: working",
        f"updated: {now()[:10]}",
        "append-source: case-logs/session.jsonl",
        "---",
        "",
        "# External Decision Memory",
        "",
        "> This is a compact decision trace: observations, decisions, uncertainty, references, and next actions. It is not a dump of hidden chain-of-thought and it is not Evidence.",
        "",
        f"**Events read:** {len(events)} · **Shown:** {len(recent)} · **Invalid lines skipped:** {invalid}",
        "",
        "## Recent events",
        "",
        "| Time | Event | Summary | Decision | Uncertainty | Next action | References |",
        "|---|---|---|---|---|---|---|",
    ]
    for row in recent:
        refs = ", ".join(_refs(row.get("refs") or row.get("references")))
        lines.append(
            "| {ts} | {event} | {summary} | {decision} | {uncertainty} | {next_action} | {refs} |".format(
                ts=_clean(row.get("ts", ""), 25),
                event=_clean(row.get("event", ""), 30),
                summary=_clean(row.get("summary", "")),
                decision=_clean(row.get("decision", "")),
                uncertainty=_clean(row.get("uncertainty", "")),
                next_action=_clean(row.get("next_action", "")),
                refs=_clean(refs, 180),
            )
        )
    if not recent:
        lines.append("| — | — | لا توجد أحداث مسجلة بعد. | — | — | ابدأ بتسجيل قرار أو ملاحظة قابلة للمراجعة. | — |")
    lines += [
        "",
        "## Recovery instructions",
        "",
        "اقرأ هذا snapshot أولاً عند استئناف الجلسة، ثم استخدم `case_memory.py resume` لعرض آخر الأحداث. ارجع إلى `session.jsonl` فقط عند الحاجة إلى تدقيق تفصيلي؛ لا تطبع السجل كاملاً في السياق.",
        "",
    ]
    return "\n".join(lines)


def write_snapshot(case_root: Path, *, last: int = 20) -> Path:
    path = case_root / MEMORY_DIR / SNAPSHOT
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_snapshot(case_root, last=last), encoding="utf-8")
    return path


def add_memory(args: argparse.Namespace) -> int:
    refs = args.ref or []
    row = append_event(
        Path(args.case_root).resolve(),
        f"memory.{args.event_type}",
        summary=args.summary,
        observation=args.observation,
        decision=args.decision,
        uncertainty=args.uncertainty,
        next_action=args.next_action,
        confidence=args.confidence,
        refs=refs,
        tool_id=args.tool_id,
        hypothesis_id=args.hypothesis_id,
        session_id=args.session_id,
    )
    path = write_snapshot(Path(args.case_root).resolve(), last=args.last)
    print(json.dumps({"event_id": row["event_id"], "snapshot": str(path), "event": row["event"]}, ensure_ascii=False, indent=2))
    return 0


def resume_memory(args: argparse.Namespace) -> int:
    root = Path(args.case_root).resolve()
    path = write_snapshot(root, last=args.last)
    print(path.read_text(encoding="utf-8"))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="External case decision memory")
    sub = parser.add_subparsers(dest="command", required=True)
    add = sub.add_parser("add", help="append a structured decision-trace event")
    add.add_argument("case_root")
    add.add_argument("--event-type", default="decision", choices=("observation", "decision", "hypothesis", "tool-note", "review", "handoff"))
    add.add_argument("--summary", required=True)
    add.add_argument("--observation", default="")
    add.add_argument("--decision", default="")
    add.add_argument("--uncertainty", default="")
    add.add_argument("--next-action", default="")
    add.add_argument("--confidence", choices=("low", "medium", "high"), default="medium")
    add.add_argument("--ref", action="append", default=[])
    add.add_argument("--tool-id", default="")
    add.add_argument("--hypothesis-id", default="")
    add.add_argument("--session-id", default="SESSION-000")
    add.add_argument("--last", type=int, default=20)
    add.set_defaults(func=add_memory)
    resume = sub.add_parser("resume", help="render compact recovery memory")
    resume.add_argument("case_root")
    resume.add_argument("--last", type=int, default=20)
    resume.set_defaults(func=resume_memory)
    args = parser.parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
