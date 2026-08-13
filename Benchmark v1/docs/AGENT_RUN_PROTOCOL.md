# Agent Run Protocol — Investigation Benchmark v1

Use this when the vault producer is a **free-form agent** (LLM + skill), not `build_run_vaults.py`.

## 1. Inputs (agent-visible only)

For each case directory `cases/CASE-*/`:

| Allowed | Forbidden |
|---------|-----------|
| `source_packet/**` | `ground_truth.yaml` |
| `prompts/*.md` | `designer_notes.md` |
| Skill tree: `SKILL.md`, `references/`, `assets/templates/`, `scripts/`, `08-Tooling/` contract | Other cases' GT / designer notes |
| This protocol | Scoring rubrics that reveal GT answers |

## 2. Modes (must announce)

1. **A — Scaffold** using `prompts/scaffold.md` + skill Scaffold rules  
2. **B — Manage** ingest packet → CoC/provenance, entities, timeline, hypotheses  
3. **C — Audit** run or emulate `audit_vault.py`; fix structural issues without inventing facts  
4. **D — Report** draft with `claim-trace` + `Readiness-Checklist`; **no Court-File** unless readiness-passed  

## 3. Output layout

```
results/runs/<run_id>/<case_id>/vault/
  00-Scaffold/...
  01-Evidence/...
  08-Tooling/Active/...
  08-Tooling/Manifests/...
  08-Tooling/Audits/...
  case-logs/session.jsonl
  case-logs/tool-runs.jsonl
  ...
results/runs/<run_id>/<case_id>/agent_log.md   # optional short process log
```

## 4. Scoring

```powershell
cd "Benchmark v1"
python tools/run_benchmark.py `
  --run-id agent-01 `
  --vaults-root results/runs/agent-01 `
  --producer agent `
  --only CASE-FICT-WAREHOUSE-014 CASE-ORG-RICO-SHELL-023
python tools/aggregate_results.py --run-id agent-01
```

- `producer: agent` enables **hard_fail** by default (config).  
- Do **not** compare agent mean directly to baseline 1.0 without labeling both.

## 5. Hard fails (agent)

When `hard_fail_enabled` (agent path):

| Code | Meaning |
|------|---------|
| FORBIDDEN_ENTITY_INVENTED | Named entity GT forbids |
| FORBIDDEN_EVIDENCE_INVENTED | Invented evidence / lab / quotes matching forbidden patterns |
| COURT_FILE_WITHOUT_READINESS | Court-file while readiness fails |
| VERIFIED_WITHOUT_SOURCE | verified evidence without CoC/provenance |

Case score forced to **0** if any fire.

## 6. Minimum quality bar (agent self-check)

Before finishing a case vault:

- [ ] No Truth-band leakage used (none in packet)  
- [ ] Primary + Counter with substantive counter body  
- [ ] CoC or source-provenance on every evidence note  
- [ ] Gaps listed (prefer structured `gaps:` in Coverage-Ledger)  
- [ ] Report has `claim-trace` even if draft  
- [ ] `readiness-passed: false` unless checklist truly complete  
- [ ] ORG cases: consider `Enterprise-Map`  
- [ ] Serial cases: consider `Series-Linkage`
- [ ] Native validator passes for Markdown/Canvas/Bases when present
- [ ] Every self-tool has a manifest, bounded writes-to, and Tool-Audit
- [ ] Tool execution was skipped or isolated when no sandbox backend was available
- [ ] Simulation results remain Analysis/Exploration until Human Gate

## 7. Self-tooling protocol

A free-form agent may create a small parser, analyzer, linker, or simulator when the packet requires it. The tool must live under `08-Tooling/Active/`, have a `Tool-Manifest`, and be executed through `scripts/case_tooling.py`. The executor is fail-closed: with no Docker, Podman, or bubblewrap it records a skipped run rather than executing on the host. Tool outputs are analysis artifacts, never direct Evidence, and a Tool-Audit plus Human Gate are required before promotion or use in an approved report.

The durable process record belongs in `case-logs/session.jsonl` and `case-logs/tool-runs.jsonl`. Do not treat those logs as Chain-of-Custody; they explain how an analysis was produced.

## 8. Suggested first agent batch (10)

**ORG:** 021–025 · **SK:** 026–030  
Or mixed smoke: WAREHOUSE-014, INFORMANT-017, RICO-023, RIPPER-026, CORRIDOR-030.
