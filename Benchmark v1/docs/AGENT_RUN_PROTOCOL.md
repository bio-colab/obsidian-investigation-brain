# Agent Run Protocol — Investigation Benchmark v1

Use this when the vault producer is a **free-form agent** (LLM + skill), not `build_run_vaults.py`.

## 1. Inputs (agent-visible only)

For each case directory `cases/CASE-*/`:

| Allowed | Forbidden |
|---------|-----------|
| `source_packet/**` | `ground_truth.yaml` |
| `prompts/*.md` | `designer_notes.md` |
| Skill tree: `SKILL.md`, `references/`, `assets/templates/`, `scripts/audit_vault.py` | Other cases' GT / designer notes |
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

## 7. Suggested first agent batch (10)

**ORG:** 021–025 · **SK:** 026–030  
Or mixed smoke: WAREHOUSE-014, INFORMANT-017, RICO-023, RIPPER-026, CORRIDOR-030.
