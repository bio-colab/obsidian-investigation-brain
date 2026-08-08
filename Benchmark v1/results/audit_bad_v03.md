# تقرير تدقيق الـ Vault التحقيقي

**المسار:** `Benchmark v1\fixtures\sample_vault_bad`
**إجمالي الملاحظات:** 4
**أدلة:** 1 · **سجلات CoC:** 0 · **فرضيات:** 1

## الدرجة

- 🔴 حرج (critical): **8**
- 🟠 جوهري (major): **1**
- 🟡 طفيف (minor): **0**

## الملفات الهيكلية الحرجة

- ❌ `00-Scaffold/AGENTS.md`
- ✅ `00-Scaffold/Case-Scope.md`
- ❌ `00-Scaffold/Investigation-Plan.md`
- ❌ `00-Scaffold/Coverage-Ledger.md`
- ❌ `00-Scaffold/Review-Queue.md`

## توزيع المناطق

| المنطقة | عدد الملاحظات |
|---------|----------------|
| `00-Scaffold` | 1 |
| `01-Evidence` | 1 |
| `02-Entities` | 0 |
| `03-Hypotheses` | 1 |
| `04-Timeline` | 0 |
| `05-Analysis` | 0 |
| `02b-Exploration` | 0 |
| `06-Outputs` | 1 |
| `90-Reference-Sources` | 0 |
| `99-Attachments` | 0 |

## توزيع status

- `verified`: 3
- `draft`: 1

## Gap Intelligence

- أدلة بلا سلسلة حفظ: **1**
  - `01-Evidence/mystery-note.md`

- فرضيات Primary بلا Counter: **1**
  - `03-Hypotheses/only-primary.md`

## قائمة المشكلات

### CRITICAL (8)

- **MISSING_CRITICAL_FILE** — ملف هيكلي مفقود: 00-Scaffold/AGENTS.md
  - `00-Scaffold/AGENTS.md`
- **MISSING_CRITICAL_FILE** — ملف هيكلي مفقود: 00-Scaffold/Investigation-Plan.md
  - `00-Scaffold/Investigation-Plan.md`
- **MISSING_CRITICAL_FILE** — ملف هيكلي مفقود: 00-Scaffold/Coverage-Ledger.md
  - `00-Scaffold/Coverage-Ledger.md`
- **MISSING_CRITICAL_FILE** — ملف هيكلي مفقود: 00-Scaffold/Review-Queue.md
  - `00-Scaffold/Review-Queue.md`
- **EVIDENCE_NO_COC** — دليل بلا سلسلة حفظ (chain-of-custody) صالحة
  - `01-Evidence/mystery-note.md`
- **PRIMARY_NO_COUNTER** — فرضية Primary بلا Counter-Hypothesis مرتبطة
  - `03-Hypotheses/only-primary.md`
- **COURT_WITHOUT_READINESS** — court-file بدون readiness-passed على التقرير أو Readiness-Checklist
  - `06-Outputs/Court-File.md`
- **COURT_NO_CLAIM_TRACE** — court-file بلا claim-trace (مصفوفة تتبع الادعاءات)
  - `06-Outputs/Court-File.md`

### MAJOR (1)

- **STRONG_HYP_NO_SUPPORT** — فرضية conclusive بلا supporting-notes
  - `03-Hypotheses/only-primary.md`

---
*تولّد بواسطة `scripts/audit_vault.py` — obsidian-investigation-brain*