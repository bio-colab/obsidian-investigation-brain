# Investigation Benchmark v1

Benchmark harness for **`obsidian-investigation-brain`** (skill v0.2.0).

Evaluates investigation vaults produced under modes **A/B/C/D** against desensitized case packs with explicit **ground truth**.

## Metrics (12)

| ID | Metric | Higher is better? |
|----|--------|-------------------|
| M01 | Evidence coverage | yes |
| M02 | Source provenance completeness | yes |
| M03 | Hypothesis coverage | yes |
| M04 | Counter-hypothesis quality | yes |
| M05 | Timeline reconstruction | yes |
| M06 | Contradiction detection | yes |
| M07 | Missing-evidence detection | yes |
| M08 | False inference rate | **no** (reported inverted as score) |
| M09 | Confirmation-bias resistance | yes |
| M10 | Report traceability | yes |
| M11 | Readiness-gate violations | **no** (reported inverted as score) |
| M12 | Final conclusion calibration | yes |

Full definitions: [`docs/BENCHMARK_SPEC.md`](docs/BENCHMARK_SPEC.md) · scoring: [`rubrics/scoring.yaml`](rubrics/scoring.yaml).

## Layout

```
Benchmark v1/
├── README.md
├── config.yaml
├── docs/BENCHMARK_SPEC.md
├── schemas/                 # JSON Schemas
├── rubrics/scoring.yaml
├── cases/
│   ├── _template/           # blank case pack
│   └── CASE-*/              # case packs (20–50 target)
├── tools/
│   ├── check_environment.py
│   ├── validate_case.py
│   ├── init_case.py
│   ├── score_vault.py
│   ├── run_benchmark.py
│   ├── aggregate_results.py
│   ├── seed_historical_cases.py
│   └── lib/                 # shared parsers & metrics
├── fixtures/                # synthetic vaults for scorer tests
├── tests/
└── results/                 # run outputs (gitignored content OK)
```

## Quick start

```powershell
# From repo root (obsidian-investigation-brain-0.2.0)
cd "Benchmark v1"

# 1) Environment
python tools/check_environment.py

# 2) Seed 20 historical/desensitized case skeletons (if not already present)
python tools/seed_historical_cases.py

# 3) Validate all cases
python tools/validate_case.py --all

# 4) Smoke-test scorer on fixtures
python tools/score_vault.py --case-id FIXTURE-GOOD --vault fixtures/sample_vault_good --ground-truth fixtures/sample_vault_good/ground_truth.yaml --out results/smoke_good.json
python tools/score_vault.py --case-id FIXTURE-BAD  --vault fixtures/sample_vault_bad  --ground-truth fixtures/sample_vault_bad/ground_truth.yaml  --out results/smoke_bad.json

# 5) After agents produce vaults under results/runs/<run_id>/<case_id>/vault
python tools/run_benchmark.py --run-id demo --vaults-root results/runs/demo --producer baseline --cases-glob "cases/CASE-*"
python tools/aggregate_results.py --run-id demo

# 6) Free-form agent path
# see docs/AGENT_RUN_PROTOCOL.md
python tools/prepare_agent_run.py --run-id agent-01 --cases CASE-ORG-RICO-SHELL-023 CASE-SK-FICT-CORRIDOR-030
python tools/run_benchmark.py --run-id agent-01 --vaults-root results/runs/agent-01 --producer agent --only CASE-ORG-RICO-SHELL-023
```


## Case pack contract

Each case directory must contain:

| File | Purpose |
|------|---------|
| `case.yaml` | Metadata, scope, phases, difficulty, tags |
| `ground_truth.yaml` | Expected evidence, hypotheses, timeline, traps |
| `source_packet/BRIEF.md` | What the agent is allowed to see |
| `prompts/*.md` | Mode prompts (scaffold / manage / audit / report) |
| `README.md` | Human notes (optional but recommended) |

Schemas: `schemas/case_definition.schema.json`, `schemas/ground_truth.schema.json`.

## Scoring model (summary)

- Each metric → subscore in **[0, 1]**.
- Case score = weighted mean of metric subscores (weights in `rubrics/scoring.yaml`).
- Run score = mean / median of case scores + per-metric means + failure rates.
- **Hard fails** (optional): inventing forbidden entities, readiness-gate bypass on court-file, etc.

## Safety

- Cases are **historical or fictional**, desensitized; no real active-case PII.
- Benchmark **never** requires inventing evidence; gaps must be declared.
- Do not upload sensitive vaults to public remotes.

## Transparency (release)

Skill-facing disclosure of what the benchmark measured and how it changed the skill:

- **[`../docs/BENCHMARK_TRANSPARENCY.md`](../docs/BENCHMARK_TRANSPARENCY.md)** (Arabic/English mixed technical)
- Packet enrichment log: [`docs/PACKET_ENRICHMENT_LOG.md`](docs/PACKET_ENRICHMENT_LOG.md)
- Reform plan status: [`docs/REFORM_PLAN_FROM_BENCHMARK.md`](docs/REFORM_PLAN_FROM_BENCHMARK.md)

**Always label scores with `producer`:** `baseline` ≠ `agent`.

## Relation to skill audit

`scripts/audit_vault.py` (skill root) measures **structural hygiene**.  
This benchmark measures **investigative correctness vs ground truth**.  
`score_vault.py` can optionally call the skill auditor and fold results into M11 / hygiene appendix.
