# تصنيف أنواع الملاحظات — الدماغ التحقيقي

## 1. المبادئ

- كل ملاحظة تحمل `type` و `status` في YAML.
- الروابط الخلفية (backlinks) أهم من التكرار.
- Evidence لا يحتوي تخميناً أبداً.

## 2. الأنواع الأساسية

### 2.1 Evidence

| الحقل | مطلوب | وصف |
|-------|--------|-----|
| `type` | نعم | `physical-evidence` / `digital-evidence` / `testimonial` / `documentary` |
| `status` | نعم | `verified` / `pending-human-review` / `deprecated` |
| `evidence-id` | نعم | معرّف فريد داخل القضية |
| `collected-by` | نعم | من جمع الدليل |
| `collected-at` | نعم | تاريخ ووقت الجمع |
| `location-collected` | مفضل | مكان الجمع |
| `chain-of-custody` | نعم | رابط إلى سجل الحفظ |
| `related-entities` | مفضل | أشخاص / مواقع / مركبات مرتبطة |
| `related-events` | مفضل | أحداث زمنية مرتبطة |
| `support-level` | اختياري | قوة الدليل نفسه (weak / moderate / strong / conclusive) |
| `attachments` | اختياري | روابط إلى ملفات في 99-Attachments |

### 2.2 Chain-of-Custody Entry

| الحقل | مطلوب | وصف |
|-------|--------|-----|
| `type` | نعم | `chain-of-custody` |
| `evidence-ref` | نعم | رابط إلى ملاحظة الدليل |
| `custody-log` | نعم | قائمة أحداث (من → إلى، وقت، سبب، حالة) |
| `current-custodian` | نعم | المسؤول الحالي |
| `integrity-hash` | مفضل | للرقمي |

### 2.3 Person (Entity)

- الحقل الاختياري `relationships`: قائمة روابط أشخاص (sibling/spouse/parent/child/cousin/nephew/associate/…).
- الدور قد يشمل `investigator` إضافة إلى victim/suspect/witness/person-of-interest.


| الحقل | مطلوب | وصف |
|-------|--------|-----|
| `type` | نعم | `person` |
| `role` | نعم | `victim` / `suspect` / `witness` / `person-of-interest` / `other` |
| `status` | نعم | |
| `aliases` | اختياري | أسماء مستعارة |
| `related-locations` | مفضل | |
| `related-vehicles` | مفضل | |
| `related-organizations` | مفضل | |
| `timeline-links` | مفضل | أحداث مرتبط بها |
| `hypotheses-links` | مفضل | فرضيات يظهر فيها |

### 2.4 Location / Vehicle / Organization / Object

- **Organization:** استخدم القالب `Organization.md` مع `org-kind` (law-enforcement / government / corporate / tribal / criminal-group / ngo / other).
- لا تخلط المنظمة مع Person.


حقول مماثلة مع `type` المناسب + علاقات بالأشخاص والأحداث.

### 2.5 Hypothesis

| الحقل | مطلوب | وصف |
|-------|--------|-----|
| `type` | نعم | `hypothesis` |
| `hypothesis-kind` | نعم | `primary` / `alternative` / `counter` / `rejected` |
| `status` | نعم | |
| `support-level` | نعم | `weak` / `moderate` / `strong` / `conclusive` |
| `supporting-notes` | نعم عند الرفع | روابط إلى أدلة أو أحداث |
| `counter-hypothesis` | إلزامي إذا primary | رابط إلى الفرضية المضادة |
| `rejects` | إذا rejected | سبب الرفض + تاريخ |
| `related-entities` | مفضل | |
| `related-events` | مفضل | |

### 2.6 Timeline-Event

| الحقل | مطلوب | وصف |
|-------|--------|-----|
| `type` | نعم | `timeline-event` |
| `timestamp` | نعم | تاريخ ووقت (أو نطاق) |
| `precision` | مفضل | `exact` / `approximate` / `day-only` / `unknown` |
| `source` | نعم | رابط إلى دليل أو إفادة |
| `participants` | مفضل | أشخاص |
| `location` | مفضل | |
| `contradicts` | اختياري | روابط إلى أحداث أو إفادات متناقضة |

### 2.7 Alibi / Contradiction

- `type: alibi` أو `type: contradiction`
- مرتبطة بشخص + أحداث + مصدر.

### 2.7b Hypothesis evolution

- الحقل الاختياري `support-history` يسجّل تغيّر `support-level` عبر الزمن.
- الحقل `superseded-by` لربط فرضية أُزيحت بفرضية لاحقة.

### 2.8 Analysis

- `type: analysis` (modus-operandi / motive / behavioral / link)
- `status` يحدد هل هي مسودة أم معتمدة.

### 2.9 Coverage-Ledger / Review-Queue / Case-Report

أنواع بنيوية في Scaffold و Outputs.

## 3. قواعد عامة للـ YAML

- استخدم `status` دائماً.
- الروابط الداخلية بأسلوب `[[Note Name]]`.
- عند الرفض أو الإهلاك: لا تحذف — غيّر `status` إلى `rejected` أو `deprecated` وسجّل السبب.
- التواريخ بصيغة ISO قدر الإمكان (`YYYY-MM-DD` أو `YYYY-MM-DDTHH:mm`).


### قالب Analysis

استخدم `assets/templates/Analysis.md` لملاحظات النمط / الدافع / السلوك مع `related-events` إلزامي تقريباً عند الحديث عن سلسلة حوادث.


### 2.10 ملاحظات النطاق الجماعي (قضايا تاريخية)

- عند وجود عشرات الضحايا غير المسمّين في المصدر العام: أنشئ ملاحظة كيان جماعية أو أعلن الفجوة في Coverage-Ledger — **لا تختلق أسماء**.
