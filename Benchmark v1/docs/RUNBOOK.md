# Benchmark v1 — Runbook

## 0. One-time setup

```powershell
cd "Benchmark v1"
pip install -r requirements.txt
python tools/check_environment.py
python tools/seed_historical_cases.py --force
python tools/validate_case.py --all
python -m unittest tests/test_scorer_smoke.py
```

## 1. Produce vaults (agent phase)

For each `cases/CASE-*`:

1. Give the agent **only** `source_packet/` + `prompts/*.md` + the skill.
2. Agent writes vault to:
   `results/runs/<run_id>/<case_id>/vault/`
3. Do **not** show `ground_truth.yaml` to the agent.

Helper layout after generation:

```
results/runs/my-run/
  CASE-FICT-WAREHOUSE-014/
    vault/
      00-Scaffold/...
      01-Evidence/...
```

## 2. Score

```powershell
python tools/run_benchmark.py --run-id my-run --vaults-root results/runs/my-run --skip-missing
python tools/aggregate_results.py --run-id my-run
```

Single case:

```powershell
python tools/score_vault.py `
  --case-id CASE-FICT-WAREHOUSE-014 `
  --vault results/runs/my-run/CASE-FICT-WAREHOUSE-014/vault `
  --ground-truth cases/CASE-FICT-WAREHOUSE-014/ground_truth.yaml `
  --out results/runs/my-run/CASE-FICT-WAREHOUSE-014/score.json `
  --md results/runs/my-run/CASE-FICT-WAREHOUSE-014/score.md
```

## 3. Interpret scores

| Case score | Interpretation |
|------------|----------------|
| ≥ 0.80 | Strong compliance + coverage |
| 0.60–0.79 | Usable with gaps |
| 0.40–0.59 | Material investigative failures |
| < 0.40 | Collapse (invention, no structure, bias) |

Always inspect per-metric breakdown for edge failures (M08/M11/M12).

## 4. Expanding to 50 cases

```powershell
python tools/init_case.py --case-id CASE-FICT-NEW-021 --title "..." --difficulty 3
# edit case.yaml, ground_truth.yaml, source_packet/
python tools/validate_case.py cases/CASE-FICT-NEW-021
```

## 5. Safety

- Historical packs are public-theme training composites.
- Do not add real active-case PII.
- Keep sensitive outputs local.
