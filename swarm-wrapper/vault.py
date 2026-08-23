"""Case-vault projections for the Investigation Swarm wrapper.

All generated artifacts stay under 08-Tooling/Swarm/<team-id>. This module
never writes to 01-Evidence, changes note status, or treats agent text as a
source of truth.
"""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import re
import uuid
from pathlib import Path
from typing import Any, Iterable

from models import Conflict, Gate, Proposal, TeamManifest


ALLOWED_ROOT = "08-Tooling/Swarm"
RUN_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,63}$")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return f"sha256:{digest.hexdigest()}"


def append_event(case_root: Path, event: str, **payload: Any) -> None:
    log_dir = case_root / "case-logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    row = {"ts": utc_now(), "event_id": f"SW-{uuid.uuid4().hex[:12]}", "event": event, **payload}
    with (log_dir / "session.jsonl").open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def _inside(root: Path, path: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def _frontmatter(values: dict[str, Any]) -> str:
    lines = ["---"]
    for key, value in values.items():
        if isinstance(value, list):
            encoded = "[" + ", ".join(json.dumps(item, ensure_ascii=False) for item in value) + "]"
        elif isinstance(value, bool):
            encoded = "true" if value else "false"
        else:
            encoded = json.dumps(value, ensure_ascii=False)
        lines.append(f"{key}: {encoded}")
    return "---\n" + "\n".join(lines) + "\n---\n"


def _cell(value: Any) -> str:
    """Escape untrusted text for a Markdown table cell (pipes, newlines)."""
    text = _line(value)
    return text or "—"


def _line(value: Any) -> str:
    """Escape untrusted text for inline Markdown use without a dash fallback."""
    return str(value).replace("|", "\\|").replace("\r", " ").replace("\n", " ")


def _fenced(text: str) -> tuple[str, str]:
    """Return open/close fence markers long enough to survive embedded backticks."""
    longest = max((len(run) for run in re.findall(r"`{3,}", text)), default=0)
    marker = "`" * max(3, longest + 1)
    return marker, marker


class CaseVault:
    def __init__(self, root: Path, manifest: TeamManifest):
        self.root = root.resolve()
        self.manifest = manifest
        self.team_root = (self.root / ALLOWED_ROOT / manifest.team_id).resolve()
        if not _inside(self.root, self.team_root):
            raise ValueError("team workspace escapes case root")
        self.run_root = self.team_root / "runs"

    def _run_root(self, run_id: str) -> Path:
        if not RUN_ID_RE.fullmatch(run_id):
            raise ValueError("run_id must be a safe identifier (letters, numbers, . _ -)")
        path = (self.run_root / run_id).resolve()
        if not _inside(self.run_root, path):
            raise ValueError("run workspace escapes run namespace")
        return path

    def prepare(self, run_id: str) -> Path:
        run = self._run_root(run_id)
        (run / "proposals").mkdir(parents=True, exist_ok=True)
        return run

    def source_snapshot(self) -> tuple[str, list[dict[str, str]]]:
        source = (self.root / self.manifest.source_root).resolve()
        if not _inside(self.root, source):
            raise ValueError("source_root escapes case root")
        if not source.exists():
            raise ValueError(f"source_root does not exist: {self.manifest.source_root}")
        items: list[dict[str, str]] = []
        digest = hashlib.sha256()
        paths = [source] if source.is_file() else sorted(p for p in source.rglob("*") if p.is_file())
        for path in paths:
            rel = path.relative_to(self.root).as_posix()
            file_hash = sha256_file(path)
            items.append({"path": rel, "hash": file_hash})
            digest.update(rel.encode("utf-8"))
            digest.update(file_hash.encode("utf-8"))
        return f"sha256:{digest.hexdigest()}", items

    def write_manifest(self, run_id: str, source_hash: str, source_files: list[dict[str, str]]) -> None:
        run = self.prepare(run_id)
        payload = {
            "case_id": self.manifest.case_id,
            "team_id": self.manifest.team_id,
            "run_id": run_id,
            "source_hash": source_hash,
            "source_files": source_files,
            "created_at": utc_now(),
        }
        (run / "run.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        append_event(self.root, "swarm.run.created", case_id=self.manifest.case_id, team_id=self.manifest.team_id, run_id=run_id, source_hash=source_hash)

    def write_proposal(self, run_id: str, proposal: Proposal) -> Path:
        path = self._run_root(run_id) / "proposals" / f"{proposal.agent_id}.md"
        body: list[str] = [
            _frontmatter({
                "type": "agent-proposal",
                "status": "draft" if proposal.parse_status == "structured" else "unstructured",
                "created": proposal.created_at[:10],
                "updated": proposal.created_at[:10],
                "case-id": proposal.case_id,
                "team-id": proposal.team_id,
                "run-id": proposal.run_id,
                "agent-id": proposal.agent_id,
                "role": proposal.role,
                "proposal-id": proposal.proposal_id,
                "parse-status": proposal.parse_status,
                "source-hash": proposal.source_hash,
                "jurisdiction": proposal.jurisdiction or "",
                "tags": ["swarm", "proposal", "analysis"],
            }),
            f"# Proposal — {proposal.agent_id}",
            "",
            "> This is an unapproved agent proposal. It is not Evidence and cannot change a note status.",
            "",
            f"**Summary:** {_line(proposal.summary) or 'No structured summary returned.'}",
            "",
            "## Claims",
            "",
            "| ID | Claim | Support refs | Counter refs | Confidence | Limitations |",
            "|---|---|---|---|---|---|",
        ]
        if proposal.claims:
            for claim in proposal.claims:
                body.append(
                    "| {id} | {text} | {support} | {counter} | {confidence} | {limits} |".format(
                        id=_cell(claim.claim_id),
                        text=_cell(claim.text),
                        support=_cell(", ".join(claim.supporting_refs)),
                        counter=_cell(", ".join(claim.counter_refs)),
                        confidence=_cell(claim.confidence),
                        limits=_cell(", ".join(claim.limitations)),
                    )
                )
        else:
            body.append("| — | No structured claims | — | — | unknown | parse or agent failure |")
        body.extend(["", "## Known gaps", ""])
        body.extend(f"- {_cell(gap)}" for gap in proposal.known_gaps) if proposal.known_gaps else body.append("- No gaps returned; this is not evidence that no gaps exist.")
        raw_tail = proposal.raw_text[-12000:]
        open_fence, close_fence = _fenced(raw_tail)
        body.extend(["", "## Raw response (untrusted analysis text)", "", open_fence + "text", raw_tail, close_fence, ""])
        path.write_text("\n".join(body), encoding="utf-8")
        append_event(self.root, "swarm.proposal.written", case_id=proposal.case_id, team_id=proposal.team_id, run_id=proposal.run_id, agent_id=proposal.agent_id, proposal_id=proposal.proposal_id, parse_status=proposal.parse_status, source_hash=proposal.source_hash)
        return path

    def write_conflicts(self, run_id: str, conflicts: Iterable[Conflict]) -> Path:
        items = list(conflicts)
        path = self._run_root(run_id) / "conflicts.md"
        body = [
            _frontmatter({"type": "swarm-conflict-report", "status": "pending-human-review" if items else "draft", "created": utc_now()[:10], "updated": utc_now()[:10], "case-id": self.manifest.case_id, "team-id": self.manifest.team_id, "run-id": run_id, "tags": ["swarm", "conflict", "human-gate"]}),
            f"# Conflicts — {run_id}",
            "",
            "> Conflicts are unresolved analysis. They must not be silently averaged or promoted.",
            "",
            "| Conflict | Claim | Proposals | Descriptions | Status |",
            "|---|---|---|---|---|",
        ]
        for item in items:
            body.append(f"| {_cell(item.conflict_id)} | {_cell(item.claim_id)} | {_cell(', '.join(item.proposal_ids))} | {_cell('; '.join(item.descriptions))} | {_cell(item.status)} |")
        if not items:
            body.append("| — | — | — | No exact claim-id conflict detected; semantic review is still required. | none-detected |")
        path.write_text("\n".join(body) + "\n", encoding="utf-8")
        return path

    def write_consensus(self, run_id: str, proposals: Iterable[Proposal], conflicts: Iterable[Conflict]) -> tuple[Path, Path]:
        proposals_list = list(proposals)
        conflicts_list = list(conflicts)
        run = self._run_root(run_id)
        draft = run / "consensus-draft.md"
        gate = Gate(gate_id=f"GATE-{self.manifest.team_id}-{run_id}", case_id=self.manifest.case_id, team_id=self.manifest.team_id, run_id=run_id)
        body = [
            _frontmatter({"type": "consensus-draft", "status": "pending-human-review", "created": utc_now()[:10], "updated": utc_now()[:10], "case-id": self.manifest.case_id, "team-id": self.manifest.team_id, "run-id": run_id, "human-gate": gate.gate_id, "tags": ["swarm", "consensus", "draft"]}),
            f"# Consensus Draft — {run_id}",
            "",
            "> This is a synthesis draft, not a conclusion. Human Gate is mandatory before any promotion.",
            "",
            f"**Proposals received:** {len(proposals_list)}  ",
            f"**Conflicts detected:** {len(conflicts_list)}  ",
            "**Promotion:** forbidden by this MVP.",
            "",
            "## Inputs",
            "",
        ]
        for proposal in proposals_list:
            body.append(f"- [[proposals/{proposal.agent_id}]] — {proposal.role} — {proposal.parse_status} — {len(proposal.claims)} claims")
        body.extend(["", "## Claims to review", "", "| Agent | Claim ID | Text | Supporting refs | Counter refs |", "|---|---|---|---|---|"])
        for proposal in proposals_list:
            for claim in proposal.claims:
                body.append(f"| {_cell(proposal.agent_id)} | {_cell(claim.claim_id)} | {_cell(claim.text)} | {_cell(', '.join(claim.supporting_refs))} | {_cell(', '.join(claim.counter_refs))} |")
        body.extend(["", "## Required human decisions", "", "- Are any claims supported by source notes rather than agent assertions?", "- Are counter-hypotheses substantive and represented?", "- Are jurisdiction and limitations explicit?", "- Which gaps must remain open?", ""])
        draft.write_text("\n".join(body), encoding="utf-8")
        gate_path = run / "human-gates" / f"{gate.gate_id}.md"
        gate_path.parent.mkdir(parents=True, exist_ok=True)
        gate_path.write_text(
            _frontmatter({"type": "human-gate", "status": gate.status, "created": utc_now()[:10], "updated": utc_now()[:10], "case-id": gate.case_id, "team-id": gate.team_id, "run-id": gate.run_id, "gate-id": gate.gate_id, "tags": ["swarm", "human-gate"]})
            + f"# Human Gate — {gate.gate_id}\n\nReview `[[../consensus-draft]]` and `[[../conflicts]]`.\n\n- Reviewer: \n- Decision: pending\n- Reason: {gate.reason}\n- Decided at: \n\nNo Evidence or final report may be promoted until this file is completed by a human reviewer.\n",
            encoding="utf-8",
        )
        append_event(self.root, "swarm.consensus.draft", case_id=self.manifest.case_id, team_id=self.manifest.team_id, run_id=run_id, proposals=len(proposals_list), conflicts=len(conflicts_list), gate_id=gate.gate_id)
        return draft, gate_path
