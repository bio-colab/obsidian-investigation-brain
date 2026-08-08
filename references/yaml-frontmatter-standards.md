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
