# Investigation Benchmark v1 — Specification

## 1. Purpose

Push `obsidian-investigation-brain` to the edge on **real investigative failure modes**:

- inventing evidence or names
- missing chain-of-custody / provenance
- primary hypotheses without counters
- weak timeline reconstruction
- ignored contradictions and known gaps
- confirmation bias
- untraceable reports and readiness-gate bypass
- overconfident conclusions

Corpus size target: **20–50** desensitized historical or fictional cases.

## 2. Units of evaluation

| Unit | Definition |
|------|------------|
| **Case pack** | Self-contained folder under `cases/CASE-*` |
| **Vault** | Obsidian vault produced by an agent using the skill |
| **Run** | Scoring of N vaults (one per case) under one `run_id` |
| **Ground truth (GT)** | Authoritative expected facts, traps, and calibration targets |

Agents only receive `source_packet/` (+ prompts).  
They **must not** receive `ground_truth.yaml` at generation time.

## 3. Metric definitions

All metric scores are normalized to **[0, 1]** where **1 = best**.

### M01 — Evidence coverage

- **GT items:** `ground_truth.evidence[]` with `id`, aliases, required zone/type.
- **Recall** = matched_gt / total_gt_required
- **Precision** (optional weight) = matched_vault_evidence / vault_evidence_count
- **Score** = `0.7 * recall + 0.3 * precision` (precision=1.0 if no vault evidence)

A match is: same `evidence-id` **or** text similarity ≥ threshold on title/body **or** alias hit.

### M02 — Source provenance completeness

For every evidence note in the vault (or matched GT evidence if `score_only_matched: true`):

- operational → valid `chain-of-custody` link **or** CoC note with `evidence-ref`
- archival (`source-kind` public-archive / …) → valid `source-provenance` (archive + record-id|url)

**Score** = complete / total_applicable  
Empty vault evidence → 0.

### M03 — Hypothesis coverage

GT `hypotheses[]` marked `required: true` must appear (by id/alias/similarity) with correct `hypothesis-kind` when specified.

**Score** = covered_required / total_required

### M04 — Counter-hypothesis quality

For each **Primary** in vault (and GT primaries):

| Check | Weight |
|-------|--------|
| Counter field present and resolvable | 0.40 |
| Counter content is substantive (not empty / not copy of primary) | 0.30 |
| Counter matches GT expected counter theme (if provided) | 0.30 |

**Score** = mean over primaries. No primaries → 0 if GT requires any primary, else 1.

### M05 — Timeline reconstruction

GT `timeline_events[]` matched by:

1. date within `date_tolerance_days` (precision-aware)
2. participant/location overlap if provided
3. text similarity on summary

**Score** = matched_events / total_gt_events  
Bonus (capped): contradictions timeline links present (see M06).

### M06 — Contradiction detection

GT `contradictions[]` each has description + related event/evidence ids.

Detected if vault has `type: contradiction` (or analysis note) matching aliases/text **or** explicitly linked related ids.

**Score** = detected / total_gt

### M07 — Missing-evidence detection

GT `known_gaps[]` / `missing_evidence[]` should appear in:

- Coverage-Ledger body/YAML, **or**
- Case report “gaps” section, **or**
- dedicated gap notes

**Score** = declared_gaps / total_gt_gaps

### M08 — False inference rate (inverted)

GT `forbidden_inferences[]` and `forbidden_entities[]`:

- rate = hits / max(1, total_forbidden_items)
- **Score** = `1 - rate` (clipped)

Also flags inventing named persons when GT says `group-entity-only`.

### M09 — Confirmation-bias resistance

Composite:

1. All primaries have counters (share)
2. Preferred hypothesis (if GT marks one) is **not** marked conclusive without required support
3. Alternative/counter hypotheses exist when GT requires multi-hypothesis set
4. Rejected alternatives have written reasons when present

**Score** = weighted mean of subchecks.

### M10 — Report traceability

In `06-Outputs/**` report notes:

- extract claim-like sentences / bullet claims (heuristic) **or** use GT `report_must_cite[]`
- each required claim must wikilink or list `supporting-notes` / evidence ids

**Score** = traced_required_claims / total_required_claims  
No report when required → 0.

### M11 — Readiness-gate violations (inverted)

Count violations:

- court-file / final report without CoC/provenance on cited evidence
- strong/conclusive primary without supporting-notes
- primary without counter
- `verified` exploration content
- skill `audit_vault.py` critical issues (if enabled)

`raw = min(1, violations / violation_cap)` with `violation_cap` default 5  
**Score** = `1 - raw`

### M12 — Final conclusion calibration

Compare vault final hypothesis/report conclusion vs GT `truth_status`:

| GT truth_status | Expected vault support-level band |
|-----------------|-----------------------------------|
| established | strong–conclusive |
| probable | moderate–strong |
| disputed | weak–moderate + counter retained |
| unknown / cold | weak or cause-unknown; no conclusive |
| false_trap | must **not** be primary conclusive |

**Score** from calibration matrix in `rubrics/scoring.yaml`.

## 3.1 — Integrity gates (not a truth metric)

تُسجل سلامة الصيغة والتشغيل منفصلة عن جودة الاستدلال، لأن صحة JSON/YAML أو وجود trace لا يثبت أن النتيجة صحيحة. عند تفعيل `run_benchmark.py` دون `--no-native-check` تُحفظ `native-validation.json` لكل قضية، وتشمل:

| البوابة | الفشل |
|---|---|
| Native Markdown | frontmatter غير صالح أو wikilinks غير قابلة للحل، ويُبلغ عنها كتحذير/خطأ |
| JSON Canvas | JSON غير صالح، IDs مكررة، أو edges معلقة |
| Bases | YAML غير صالح أو formulas غير معرفة |
| Tool trace | manifest ناقص، writes-to خارج الحدود، أو غياب Tool-Audit عند استخدام أداة |
| Sandbox | تشغيل الكود على المضيف دون `--allow-host` لا يُعد تشغيل قضية مقبولاً |

يفشل `--strict-native` عند أخطاء native، بينما لا يدخل تحذير التنسيق أو وجود tooling بحد ذاته في case score. يمكن تفسير `native_error_cases` في `summary.json` دون خلطه بمقياس المعرفة.

## 4. Aggregation

- **Case score** = Σ (weight_i * metric_i) / Σ weights
- **Run score** = mean of case scores
- Also report: median, stdev, per-metric means, hard-fail count, skill-audit critical totals

## 5. Difficulty tiers

| Tier | Intent |
|------|--------|
| D1 | Single incident, clean sources, one primary |
| D2 | Multi-source, alibis, mild contradiction |
| D3 | Archival + operational mix, group entities |
| D4 | Cold case / cause-unknown, systemic factors |
| D5 | Organized crime / financial / wiretap / informant traps |

## 6. Protocol (human + agent)

1. Validate case packs (`validate_case.py --all`).
2. For each case: run skill modes A→B→C→D with **only** source_packet.
3. If the case creates tools, preserve `08-Tooling/` and `case-logs/`; do not expose ground truth.
4. Score vault (`score_vault.py`) and run native validation unless explicitly disabled.
5. Aggregate (`aggregate_results.py`).
6. Optional: human adjudication on M04/M08/M12 edge cases → `adjudication.yaml`.

## 7. Out of scope for v1

- Courtroom legal accuracy of statutes
- Lab science correctness beyond GT statements
- Multi-vault cross-case entity resolution
- Live web retrieval quality (packets are offline)

## 8. Versioning

- Benchmark spec version: **v1.0.0**
- Incompatible GT schema changes → bump minor/major and regenerate seeds.
