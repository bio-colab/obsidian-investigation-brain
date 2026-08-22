from __future__ import annotations

import json
from pathlib import Path
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import threading

import pytest

ROOT = Path(__file__).resolve().parents[2]
WRAPPER = ROOT / "swarm-wrapper"
sys.path.insert(0, str(WRAPPER))

from models import AgentSpec, TeamManifest  # noqa: E402
from orchestrator import OpenMausBotClient, detect_conflicts, run_team  # noqa: E402
from vault import append_event  # noqa: E402


@pytest.fixture
def manifest() -> TeamManifest:
    return TeamManifest.from_mapping(
        {
            "case_id": "CASE-TEST-SWARM-001",
            "team_id": "TEAM-TEST-001",
            "title": "Test team",
            "source_root": "01-Evidence",
            "mode": "dry-run",
            "max_workers": 3,
            "timeout_seconds": 10,
            "agents": [
                {"agent_id": "osint", "role": "OSINT", "task": "find leads"},
                {"agent_id": "finance", "role": "Finance", "task": "find patterns"},
                {"agent_id": "redteam", "role": "Red Team", "task": "challenge claims"},
            ],
        }
    )


def test_dry_run_fanout_writes_only_bounded_artifacts(tmp_path: Path, manifest: TeamManifest) -> None:
    evidence = tmp_path / "01-Evidence"
    evidence.mkdir()
    source = evidence / "source.md"
    source.write_text("---\ntype: evidence\nstatus: unverified\n---\nA fixture source.\n", encoding="utf-8")

    result = run_team(manifest, tmp_path, run_id="RUN-TEST-001")

    assert result["proposals"] == 3
    assert result["failures"] == []
    assert result["conflicts"] == 0
    assert result["promotion_allowed"] is False
    run_root = tmp_path / "08-Tooling" / "Swarm" / manifest.team_id / "runs" / "RUN-TEST-001"
    assert (run_root / "consensus-draft.md").exists()
    assert list((run_root / "proposals").glob("*.md"))
    assert (run_root / "human-gates" / "GATE-TEAM-TEST-001-RUN-TEST-001.md").exists()
    assert not (run_root.parent.parent / "agents").exists()
    assert not (run_root.parent.parent / "shared").exists()
    assert source.read_text(encoding="utf-8").startswith("---")
    assert {p.relative_to(tmp_path).parts[0] for p in tmp_path.rglob("*") if p.is_file()} >= {"01-Evidence", "08-Tooling", "case-logs"}


def test_openmausbot_mode_requires_bot_ids(tmp_path: Path) -> None:
    (tmp_path / "01-Evidence").mkdir()
    manifest = TeamManifest.from_mapping(
        {
            "case_id": "CASE-TEST-SWARM-002",
            "team_id": "TEAM-TEST-002",
            "title": "Invalid live team",
            "source_root": "01-Evidence",
            "mode": "openmausbot",
            "agents": [{"agent_id": "a1", "role": "analyst", "task": "inspect", "bot_id": ""}],
        }
    )
    result = run_team(manifest, tmp_path, run_id="RUN-LIVE-MISSING-BOT")
    assert result["failures"]
    assert "needs bot_id" in result["failures"][0]["error"]


def test_conflicting_same_claim_id_is_held_for_human_review() -> None:
    class FixedClient:
        def run(self, agent: AgentSpec, prompt: str, timeout_seconds: int) -> str:
            text = "The shipment was in Riyadh." if agent.agent_id == "one" else "The shipment was in Dubai."
            return json.dumps(
                {
                    "summary": "two competing test interpretations",
                    "claims": [{"claim_id": "LOC-001", "text": text, "confidence": "low"}],
                    "known_gaps": ["fixture has no corroborating source"],
                }
            )

    proposals = []
    for agent in (
        AgentSpec("one", "Analyst", "inspect"),
        AgentSpec("two", "Analyst", "inspect"),
    ):
        from models import Proposal

        proposals.append(
            Proposal.from_reply(
                agent=agent,
                manifest=TeamManifest.from_mapping(
                    {
                        "case_id": "CASE-TEST-SWARM-003",
                        "team_id": "TEAM-TEST-003",
                        "title": "Conflict",
                        "source_root": "01-Evidence",
                        "agents": [{"agent_id": "one", "role": "Analyst", "task": "inspect"}],
                    }
                ),
                run_id="RUN-X",
                raw_text=FixedClient().run(agent, "", 10),
                source_hash="sha256:test",
            )
        )
    conflicts = detect_conflicts(proposals)
    assert len(conflicts) == 1
    assert conflicts[0].claim_id == "LOC-001"


def test_openmausbot_adapter_uses_loopback_api(tmp_path: Path) -> None:
    (tmp_path / "01-Evidence").mkdir()
    state = {"busy": False, "messages": [{"role": "bot", "kind": "text", "text": "welcome"}]}

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, format: str, *args: object) -> None:
            return

        def _send(self, body: dict) -> None:
            data = json.dumps(body).encode()
            self.send_response(200)
            self.send_header("content-type", "application/json")
            self.send_header("content-length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self) -> None:  # noqa: N802
            if self.path == "/api/bots":
                self._send({"bots": [{"id": "bot-1", "busy": state["busy"], "messages": state["messages"]}]})
            else:
                self.send_error(404)

        def do_POST(self) -> None:  # noqa: N802
            length = int(self.headers.get("content-length", "0"))
            _ = self.rfile.read(length)
            state["messages"].append({"role": "user", "kind": "text", "text": "prompt"})
            state["messages"].append(
                {
                    "role": "bot",
                    "kind": "text",
                    "text": json.dumps({"summary": "local fake response", "claims": [], "known_gaps": ["fixture"]}),
                }
            )
            state["busy"] = False
            self._send({"ok": True})

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        manifest = TeamManifest.from_mapping(
            {
                "case_id": "CASE-TEST-SWARM-006",
                "team_id": "TEAM-TEST-006",
                "title": "Live adapter",
                "source_root": "01-Evidence",
                "mode": "openmausbot",
                "openmaus_url": f"http://127.0.0.1:{server.server_port}",
                "timeout_seconds": 10,
                "agents": [{"agent_id": "a1", "role": "analyst", "task": "inspect", "bot_id": "bot-1"}],
            }
        )
        result = run_team(manifest, tmp_path, run_id="RUN-ADAPTER", client=OpenMausBotClient(manifest.openmaus_url))
        assert result["failures"] == []
        assert result["proposals"] == 1
    finally:
        server.shutdown()
        thread.join(timeout=3)
        server.server_close()


def test_source_root_cannot_escape_vault(tmp_path: Path, manifest: TeamManifest) -> None:
    outside = tmp_path.parent / "outside-source.txt"
    outside.write_text("secret", encoding="utf-8")
    escaped = TeamManifest.from_mapping(
        {
            "case_id": "CASE-TEST-SWARM-004",
            "team_id": "TEAM-TEST-004",
            "title": "Escape",
            "source_root": "../outside-source.txt",
            "agents": [{"agent_id": "a1", "role": "analyst", "task": "inspect"}],
        }
    )
    with pytest.raises(ValueError, match="escapes case root"):
        run_team(escaped, tmp_path, run_id="RUN-ESCAPE")


def test_openmausbot_url_must_be_loopback() -> None:
    with pytest.raises(ValueError, match="loopback"):
        TeamManifest.from_mapping(
            {
                "case_id": "CASE-TEST-SWARM-005",
                "team_id": "TEAM-TEST-005",
                "title": "Remote blocked",
                "source_root": "01-Evidence",
                "mode": "openmausbot",
                "openmaus_url": "https://example.com:8799",
                "agents": [{"agent_id": "a1", "role": "analyst", "task": "inspect", "bot_id": "bot-1"}],
            }
        )


def test_human_gate_cannot_be_disabled() -> None:
    with pytest.raises(ValueError, match="Human Gate is mandatory"):
        TeamManifest.from_mapping(
            {
                "case_id": "CASE-TEST-SWARM-007",
                "team_id": "TEAM-TEST-007",
                "title": "No bypass",
                "source_root": "01-Evidence",
                "require_human_gate": False,
                "agents": [{"agent_id": "a1", "role": "analyst", "task": "inspect"}],
            }
        )


def test_swarm_event_ids_are_unique_under_rapid_writes(tmp_path: Path) -> None:
    for index in range(200):
        append_event(tmp_path, "test.event", index=index)
    rows = [json.loads(line) for line in (tmp_path / "case-logs" / "session.jsonl").read_text(encoding="utf-8").splitlines()]
    assert len({row["event_id"] for row in rows}) == len(rows)


@pytest.mark.parametrize("run_id", ["/tmp/escaped-run", "../escaped-run", "runs/escaped"])
def test_run_id_is_bounded_before_any_artifact_write(tmp_path: Path, manifest: TeamManifest, run_id: str) -> None:
    evidence = tmp_path / "01-Evidence"
    evidence.mkdir()
    (evidence / "source.md").write_text("source\n", encoding="utf-8")
    outside = tmp_path.parent / "escaped-run"

    with pytest.raises(ValueError, match="safe identifier"):
        run_team(manifest, tmp_path, run_id=run_id)

    assert not outside.exists()
    assert not (tmp_path / "08-Tooling" / "Swarm").exists()
