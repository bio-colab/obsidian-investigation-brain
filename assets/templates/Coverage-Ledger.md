---
type: coverage-ledger
status: draft
created: {{date}}
updated: {{date}}
case-id: 
plan-ref: "[[Investigation-Plan]]"
# v0.3.1 structured gaps (preferred for audit + benchmark M07)
gaps: []
# gaps:
#   - id: GAP-DNA
#     description: "DNA lab report pending"
#     phase_id: P2
#     status: open   # open | mitigated | accepted-risk
tags: [ledger]
---

# جدول التغطية التحقيقي (Coverage Ledger)

يربط **مراحل الخطة × حالة الأدلة × الفرضيات × الفجوات**. يُستخدم لقياس تقدم التحقيق و**Gap Intelligence**.

## جدول التغطية

| stage_id | stage_title | in_scope | evidence_status | key_evidence | hypotheses_status | counter_ok | timeline_coverage | gaps | notes |
|----------|-------------|----------|-----------------|--------------|-------------------|------------|-------------------|------|-------|
|          |             | yes/no   | none / partial / solid |              | none / weak / moderate / strong | yes/no     | none / partial / solid |      |       |
|          |             |          |                 |              |                   |            |                   |      |       |

> **قاعدة التحديث:** يُحدَّث بعد كل دفعة أدلة جديدة، كل فرضية جديدة أو مرفوضة، وكل مراجعة Timeline.

## Structured gaps (v0.3.1 — YAML + mirror table)

| id | description | phase_id | status |
|----|-------------|----------|--------|
| GAP- | | P2 | open |

Mirror the same rows under frontmatter `gaps:`.

## Gap Intelligence — استعلامات مقترحة
- مراحل `in_scope=yes` و`evidence_status=none` → فجوة أدلة حرجة
- فرضيات Primary بلا Counter (`counter_ok=no`)
- أدلة بلا سجل في Chain-of-Custody / provenance
- فترات زمنية فارغة في Master-Timeline
- تناقضات مفتوحة
- تقارير بلا claim-trace (v0.3)

## ملخص سريع للفجوات الحالية
- 
- 
