#!/usr/bin/env python3
"""CLI entrypoint for the Investigation Swarm wrapper MVP."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from models import TeamManifest
from orchestrator import load_manifest, run_team


def validate(args: argparse.Namespace) -> int:
    manifest = load_manifest(Path(args.manifest).resolve())
    print(json.dumps({
        "case_id": manifest.case_id,
        "team_id": manifest.team_id,
        "mode": manifest.mode,
        "agents": [agent.agent_id for agent in manifest.agents if agent.enabled],
        "source_root": manifest.source_root,
    }, ensure_ascii=False, indent=2))
    return 0


def run(args: argparse.Namespace) -> int:
    manifest = load_manifest(Path(args.manifest).resolve())
    if args.mode:
        raw = {
            "case_id": manifest.case_id,
            "team_id": manifest.team_id,
            "title": manifest.title,
            "source_root": manifest.source_root,
            "agents": [
                {
                    "agent_id": agent.agent_id,
                    "role": agent.role,
                    "task": agent.task,
                    "bot_id": agent.bot_id,
                    "jurisdiction": agent.jurisdiction,
                    "enabled": agent.enabled,
                }
                for agent in manifest.agents
            ],
            "mode": args.mode,
            "openmaus_url": manifest.openmaus_url,
            "max_workers": manifest.max_workers,
            "timeout_seconds": manifest.timeout_seconds,
            "max_claims_per_agent": manifest.max_claims_per_agent,
        }
        manifest = TeamManifest.from_mapping(raw)
    result = run_team(manifest, Path(args.vault_root).resolve(), run_id=args.run_id)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not result["failures"] else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a bounded Investigation Swarm wrapper")
    sub = parser.add_subparsers(dest="command", required=True)
    p_validate = sub.add_parser("validate")
    p_validate.add_argument("--manifest", required=True)
    p_validate.set_defaults(func=validate)
    p_run = sub.add_parser("run")
    p_run.add_argument("--manifest", required=True)
    p_run.add_argument("--vault-root", required=True)
    p_run.add_argument("--run-id")
    p_run.add_argument("--mode", choices=("dry-run", "openmausbot"))
    p_run.set_defaults(func=run)
    args = parser.parse_args()
    try:
        return int(args.func(args))
    except (ValueError, OSError, RuntimeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
