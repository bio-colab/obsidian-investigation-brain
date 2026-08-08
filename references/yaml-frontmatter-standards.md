# معايير YAML Frontmatter — الدماغ التحقيقي

## الحقول المشتركة الإلزامية

| الحقل | القيم المسموحة | ملاحظة |
|-------|----------------|--------|
| `type` | انظر note-types-taxonomy | يحدد القالب والمنطقة |
| `status` | `verified` · `unverified` · `draft` · `stub` · `deprecated` · `exploration` · `pending-human-review` · `rejected` | إلزامي على كل ملاحظة |
| `created` | `YYYY-MM-DD` أو `{{date}}` | |
| `updated` | `YYYY-MM-DD` أو `{{date}}` | يُحدَّث عند كل تعديل جوهري |
| `tags` | قائمة | مساعدة للتصفية |

## حقول خاصة بالأدلة

- `evidence-id` — معرّف فريد داخل القضية
- `collected-by` / `collected-at` / `location-collected`
- `chain-of-custody` — رابط إلزامي إلى ملاحظة CoC
- `support-level` — `weak` · `moderate` · `strong` · `conclusive`
- `integrity-hash` — للأدلة الرقمية
- `related-entities` / `related-events` — قوائم روابط

## حقول خاصة بالفرضيات

- `hypothesis-kind` — `primary` · `alternative` · `counter` · `rejected`
- `support-level`
- `supporting-notes` — قائمة روابط (إلزامية عند الرفع إلى مستوى أعلى)
- `counter-hypothesis` — إلزامي إذا كانت `primary`
- `rejects` — نص سبب الرفض عند `rejected`

## حقول خاصة بالخط الزمني

- `timestamp` — ISO قدر الإمكان
- `precision` — `exact` · `approximate` · `day-only` · `unknown`
- `source` — رابط إلى دليل أو إفادة
- `participants` / `location` / `contradicts`

## قواعد عامة

1. لا تترك `supporting-notes: []` على فرضية `support-level: strong` أو أعلى.
2. عند تغيير `status` إلى `verified` أو `rejected` سجّل السبب في Changelog أو في الحقل المخصص.
3. الروابط الداخلية بصيغة `[[Note Name]]`.
4. التواريخ بصيغة ISO (`YYYY-MM-DD` أو `YYYY-MM-DDTHH:mm`).
5. القوائم الفارغة تُكتب `[]` وليس فارغة.


## حقول اختيارية موصى بها (v0.1.1+)

| الحقل | النوع | الاستخدام |
|-------|-------|-----------|
| `support-history` | list | تاريخ تغيّر قوة الفرضية |
| `superseded-by` | link | فرضية حلت محل أخرى |
| `related-analysis` | list | ربط حدث زمني بتحليل نمط |
| `related-events` | list | على Analysis و Hypothesis |
| `source-kind` | string | public-archive / operational / other |


## كيانات — حقول v0.1.2+

| الحقل | على النوع | الاستخدام |
|-------|-----------|-----------|
| `relationships` | person | روابط أسرية/ارتباطية منظمة |
| `org-kind` | organization | تصنيف الجهة |
| `related-persons` | organization | أشخاص مرتبطون بالمنظمة |
| `role: investigator` | person | محقق / وكيل ضمن الفريق أو الوكالة |

## إضافات v0.2.0 — حرجة من بنشمارك

### الحالات الجديدة
`status` يقبل أيضاً: `open-investigation` · `cold-case` · `cause-unknown`

### source-provenance (بديل CoC للأرشيف)
```yaml
source-kind: public-archive   # أو archival / official-archive / declassified
source-provenance:
  archive: "NARA"
  collection: ""
  record-id: ""
  date-accessed: YYYY-MM-DD
  url: ""
  authenticity: official      # official | declassified | leaked | unverified
```
**قاعدة:** إذا `source-kind` أرشيفي → `source-provenance` إلزامي؛ لا تُرفع انتهاك "missing CoC".

### Vehicle موسّع
```yaml
vehicle-class: road | vessel | aircraft | other
vessel-id: ""           # IMO
flag-state: ""
classification-society: ""
aircraft-id: ""         # N-number
type-certificate: ""
flight-hours: 
```

### Group-Entity
```yaml
type: group-entity
role: victims | passengers | crew | suspects | witnesses
estimated-count: 
named-individuals: []
unnamed-count: 
```

### Financial / Wiretap / Informant / Data-Analysis
انظر القوالب الجديدة في `assets/templates/`. الحقول الرئيسية:
- `record-kind`, `amount`, `currency`, `period`
- `legal-authorization`, `participants`, `quality`
- `credibility-assessment` (reliability / motivation / deal-terms / protection-status)
- `methodology`, `input-data`, `output-data`, `confidence-level`, `limitations`

### Timeline
```yaml
era: ""                 # Prohibition-Era / Cold-War / ...
period: "1920-1933"
severity: ""            # لتحذيرات الطقس وغيرها
```

### Case-Scope
```yaml
case-status: active | open-investigation | cold-case | closed
cold-since: YYYY-MM-DD
```

### Person أدوار إضافية
`role` يقبل أيضاً: `crew` · `passenger` · `missing-person` · `informant`  
`legal-status`: `convicted` · `acquitted` · `charged` · `suspected` · `unknown`

## إضافات v0.3.0 — Reporting / Readiness

### على case-report / court-file / cold-case-report
```yaml
readiness-passed: false
claim-trace:
  - claim-id: RC-001
    claim: "..."
    evidence: ["[[EV-001]]"]
    support-level: moderate
```

### readiness-checklist
```yaml
type: readiness-checklist
readiness-passed: false
```

**قواعد:** Court-File يتطلب `readiness-passed: true` و claim-trace غير فارغ.  
Informant verified يتطلب `credibility-assessment` مكتمل.  
Wiretap verified يتطلب `legal-authorization`.

## إضافات v0.3.1 — Series / Enterprise / Ledger

### series-linkage
```yaml
type: series-linkage
series-id: SER-001
linkage-confidence: weak
inclusion-criteria: []
members: []
peripheral: []
alternative-cluster-hypothesis: "[[H-...]]"
```

### enterprise-map
```yaml
type: enterprise-map
enterprise-id: ENT-001
enterprise-confidence: moderate
org-nodes: []
predicates: []
financial-edges: []
counter-enterprise-theory: "[[H-...]]"
```

### coverage-ledger gaps
```yaml
gaps:
  - id: GAP-001
    description: "..."
    phase_id: P2
    status: open  # open | mitigated | accepted-risk
```
