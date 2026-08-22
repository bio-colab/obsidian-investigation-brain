"""Typed, validated contracts for the Investigation Swarm wrapper MVP."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
import json
import re
from urllib.parse import urlparse


AGENT_ID_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9_.-]{1,63}$")
CASE_ID_RE = re.compile(r"^[A-Z0-9][A-Z0-9_.-]{2,63}$")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def require_text(value: Any, name: str) -> str:
    text = str(value or "").strip()
    if not text:
        raise ValueError(f"{name} is required")
    return text


@dataclass(frozen=True)
class AgentSpec:
    agent_id: str
    role: str
    task: str
    bot_id: str | None = None
    jurisdiction: str | None = None
    enabled: bool = True

    @classmethod
    def from_mapping(cls, raw: dict[str, Any]) -> "AgentSpec":
        agent_id = require_text(raw.get("agent_id") or raw.get("id"), "agent_id")
        if not AGENT_ID_RE.fullmatch(agent_id):
            raise ValueError(f"invalid agent_id: {agent_id}")
        return cls(
            agent_id=agent_id,
            role=require_text(raw.get("role"), f"{agent_id}.role"),
            task=require_text(raw.get("task"), f"{agent_id}.task"),
            bot_id=str(raw["bot_id"]).strip() if raw.get("bot_id") else None,
            jurisdiction=str(raw["jurisdiction"]).strip() if raw.get("jurisdiction") else None,
            enabled=bool(raw.get("enabled", True)),
        )


@dataclass(frozen=True)
class TeamManifest:
    case_id: str
    team_id: str
    title: str
    source_root: str
    agents: tuple[AgentSpec, ...]
    mode: str = "dry-run"
    openmaus_url: str = "http://127.0.0.1:8799"
    max_workers: int = 4
    timeout_seconds: int = 180
    max_claims_per_agent: int = 20

    @classmethod
    def from_mapping(cls, raw: dict[str, Any]) -> "TeamManifest":
        case_id = require_text(raw.get("case_id"), "case_id")
        team_id = require_text(raw.get("team_id"), "team_id")
        if not CASE_ID_RE.fullmatch(case_id):
            raise ValueError(f"invalid case_id: {case_id}")
        if not AGENT_ID_RE.fullmatch(team_id):
            raise ValueError(f"invalid team_id: {team_id}")
        if raw.get("require_human_gate") is False:
            raise ValueError("Human Gate is mandatory and cannot be disabled")
        agents = tuple(AgentSpec.from_mapping(item) for item in raw.get("agents", []))
        if not agents:
            raise ValueError("agents must contain at least one agent")
        ids = [agent.agent_id for agent in agents]
        if len(ids) != len(set(ids)):
            raise ValueError("agent_id values must be unique")
        mode = str(raw.get("mode", "dry-run"))
        if mode not in {"dry-run", "openmausbot"}:
            raise ValueError("mode must be dry-run or openmausbot")
        openmaus_url = str(raw.get("openmaus_url", "http://127.0.0.1:8799")).rstrip("/")
        parsed_url = urlparse(openmaus_url)
        if mode == "openmausbot" and (parsed_url.scheme not in {"http", "https"} or parsed_url.hostname not in {"127.0.0.1", "localhost", "::1"}):
            raise ValueError("openmaus_url must target loopback in openmausbot mode")
        workers = int(raw.get("max_workers", min(4, len(agents))))
        timeout = int(raw.get("timeout_seconds", 180))
        claim_cap = int(raw.get("max_claims_per_agent", 20))
        if not 1 <= workers <= 8:
            raise ValueError("max_workers must be between 1 and 8")
        if not 10 <= timeout <= 1800:
            raise ValueError("timeout_seconds must be between 10 and 1800")
        if not 1 <= claim_cap <= 100:
            raise ValueError("max_claims_per_agent must be between 1 and 100")
        return cls(
            case_id=case_id,
            team_id=team_id,
            title=require_text(raw.get("title") or team_id, "title"),
            source_root=require_text(raw.get("source_root") or "01-Evidence", "source_root"),
            agents=agents,
            mode=mode,
            openmaus_url=openmaus_url,
            max_workers=workers,
            timeout_seconds=timeout,
            max_claims_per_agent=claim_cap,
        )


@dataclass(frozen=True)
class Claim:
    claim_id: str
    text: str
    supporting_refs: tuple[str, ...] = ()
    counter_refs: tuple[str, ...] = ()
    confidence: str = "unknown"
    limitations: tuple[str, ...] = ()

    @classmethod
    def from_mapping(cls, raw: dict[str, Any], index: int) -> "Claim":
        claim_id = require_text(raw.get("claim_id") or raw.get("id") or f"CLAIM-{index:03d}", "claim_id")
        text = require_text(raw.get("text") or raw.get("claim"), f"{claim_id}.text")
        confidence = str(raw.get("confidence", "unknown"))
        if confidence not in {"unknown", "low", "medium", "high"}:
            raise ValueError(f"invalid confidence for {claim_id}")
        return cls(
            claim_id=claim_id,
            text=text,
            supporting_refs=tuple(str(x) for x in (raw.get("supporting_refs") or raw.get("supporting-notes") or [])),
            counter_refs=tuple(str(x) for x in (raw.get("counter_refs") or raw.get("counter-hypotheses") or [])),
            confidence=confidence,
            limitations=tuple(str(x) for x in (raw.get("limitations") or [])),
        )


@dataclass(frozen=True)
class Proposal:
    proposal_id: str
    case_id: str
    team_id: str
    agent_id: str
    role: str
    run_id: str
    status: str
    summary: str
    claims: tuple[Claim, ...] = ()
    known_gaps: tuple[str, ...] = ()
    jurisdiction: str | None = None
    raw_text: str = ""
    parse_status: str = "structured"
    source_hash: str = ""
    created_at: str = field(default_factory=utc_now)

    @classmethod
    def from_reply(
        cls,
        *,
        agent: AgentSpec,
        manifest: TeamManifest,
        run_id: str,
        raw_text: str,
        source_hash: str,
    ) -> "Proposal":
        payload: dict[str, Any] | None = None
        candidates = [raw_text.strip()]
        if "```" in raw_text:
            candidates.extend(part.strip() for part in raw_text.split("```") if part.strip())
        for candidate in candidates:
            try:
                decoded = json.loads(candidate.removeprefix("json").strip())
            except json.JSONDecodeError:
                continue
            if isinstance(decoded, dict):
                payload = decoded
                break
        if payload is None:
            return cls(
                proposal_id=f"PROP-{agent.agent_id}-{run_id}",
                case_id=manifest.case_id,
                team_id=manifest.team_id,
                agent_id=agent.agent_id,
                role=agent.role,
                run_id=run_id,
                status="unstructured",
                summary=raw_text.strip()[:2000] or "agent returned no text",
                raw_text=raw_text[-12000:],
                parse_status="unstructured",
                jurisdiction=agent.jurisdiction,
                source_hash=source_hash,
            )
        claims_raw = payload.get("claims") or []
        if not isinstance(claims_raw, list):
            raise ValueError("proposal claims must be a list")
        claims = tuple(Claim.from_mapping(item, i + 1) for i, item in enumerate(claims_raw[: manifest.max_claims_per_agent]))
        return cls(
            proposal_id=str(payload.get("proposal_id") or f"PROP-{agent.agent_id}-{run_id}"),
            case_id=manifest.case_id,
            team_id=manifest.team_id,
            agent_id=agent.agent_id,
            role=agent.role,
            run_id=run_id,
            status="draft",
            summary=str(payload.get("summary") or "").strip()[:2000],
            claims=claims,
            known_gaps=tuple(str(x) for x in (payload.get("known_gaps") or payload.get("known-gaps") or [])),
            jurisdiction=str(payload.get("jurisdiction") or agent.jurisdiction or "").strip() or None,
            raw_text=raw_text[-12000:],
            parse_status="structured",
            source_hash=source_hash,
        )


@dataclass(frozen=True)
class Conflict:
    conflict_id: str
    claim_id: str
    proposal_ids: tuple[str, ...]
    descriptions: tuple[str, ...]
    status: str = "open"


@dataclass(frozen=True)
class Gate:
    gate_id: str
    case_id: str
    team_id: str
    run_id: str
    status: str = "pending-human-review"
    reason: str = "Consensus draft requires human review"
    reviewer: str = ""
    decision: str = ""
    decided_at: str = ""
