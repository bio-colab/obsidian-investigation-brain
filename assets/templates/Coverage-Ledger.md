---
type: coverage-ledger
status: verified
created: {{date}}
updated: {{date}}
case-id: 
plan-ref: "[[Investigation-Plan]]"
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

## Gap Intelligence — استعلامات مقترحة
- مراحل `in_scope=yes` و`evidence_status=none` → فجوة أدلة حرجة
- فرضيات Primary بلا Counter (`counter_ok=no`)
- أدلة بلا سجل في Chain-of-Custody
- فترات زمنية فارغة في Master-Timeline
- تناقضات مفتوحة (`resolution-status: open`)
- أسئلة تحقيقية بلا فرضية أو دليل كافٍ

## ملخص سريع للفجوات الحالية
- 
- 
