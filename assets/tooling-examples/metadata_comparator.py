#!/usr/bin/env python3
"""Example case-scoped tool: compare document metadata to reference dates.

This example is intentionally deterministic and only reads JSON input and
writes JSON output. In a real case it belongs under 08-Tooling/Active/.
"""
from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path


def parse_day(value: str) -> date:
    return date.fromisoformat(value)


def compare(records: list[dict]) -> list[dict]:
    output: list[dict] = []
    for record in records:
        observed = record.get("recorded_at")
        referenced = record.get("reference_date")
        row = {"id": record.get("id"), "recorded_at": observed, "reference_date": referenced}
        try:
            delta = (parse_day(str(observed)) - parse_day(str(referenced))).days
            row["delta_days"] = delta
            row["flag"] = "review" if abs(delta) > int(record.get("tolerance_days", 1)) else "within-tolerance"
        except (TypeError, ValueError):
            row["delta_days"] = None
            row["flag"] = "invalid-date"
        output.append(row)
    return output


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    records = json.loads(args.input.read_text(encoding="utf-8"))
    if not isinstance(records, list):
        raise SystemExit("input must be a JSON list")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(compare(records), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
