# خطة الإصلاح — من نتائج Investigation Benchmark v1

**تاريخ:** 2026-08-08  
**المهارة المستهدفة:** `obsidian-investigation-brain` **v0.2.0 → v0.3.0 (مقترح)**  
**أساس الأدلة:** تشغيلات `run-5a` · `run-5b` · `run-org-sk` + تحليل الحزام/المقيّم + سجل 0.2.0  

---

## 1) ملخص تنفيذي

| البند | الواقع |
|--------|--------|
| حجم الكوربس | **30** حزمة قضية صالحة |
| قضايا مُقيَّمة baseline | **20** (5+5+10) |
| متوسط الدرجة (baseline) | **≈ 0.994** |
| أضعف مقياس ظاهر | **M10 report_traceability** (في `run-5a` فقط جزئياً) |
| الاستنتاج الخاطئ | «المهارة كاملة ولا تحتاج إصلاح» |
| الاستنتاج الصحيح | الـ **baseline المنضبط** يُثبت *قابلية* البروتوكول، لا صلابة الوكيل الحر؛ والإصلاح يجب أن يعالج **فجوات المهارة + صلابة البنchmark + جودة الحزم** |

**مبدأ الإصلاح (نفس مبدأ 0.2.0):**  
كل بند يجب أن يجيب: هل يزيد قدرة المحقق على الدفاع عن سلامة الأدلة ومسار الاستدلال أمام جهة إشراف أو محكمة؟

---

## 2) قراءة النتائج — ماذا قاست التشغيلات فعلاً؟

### 2.1 ما نجح (إشارات إيجابية)

على مسار `build_run_vaults.py` (منتج أوضاع أ–د منضبط):

| مقياس | دلالة |
|--------|--------|
| M01 Evidence coverage | القوالب + تصنيف الأدلة كافيان لاستيعاب الحزم الحالية |
| M02 Provenance/CoC | مسار `source-provenance` vs CoC التشغيلي يعمل عند الالتزام |
| M03–M04 Hypotheses + Counter | Primary↔Counter قابل للتمثيل في YAML والهيكل |
| M05–M07 Timeline / Contradiction / Gaps | البنية الزمنية والـ Ledger تستوعب الفجوات والتناقضات المعلنة |
| M08–M09 False inference / bias | عند انضباط الصياغة: لا اختلاق DNA/هويات/wiretaps |
| M11–M12 Readiness / calibration | cold/open/cause-unknown و bands الدعم قابلة للمعايرة |

هذا يؤكد أن **إصلاحات 0.2.0 الحرجة** (provenance، cold-case، group-entity، informant templates…) في الاتجاه الصحيح.

### 2.2 أين ظهر الضعف داخل نفس المنهج

| ظاهرة | أين | تفسير |
|--------|-----|--------|
| **M10 < 1** | `CASE-FICT-PAYROLL-015`, `CASE-FICT-LABGAP-018` (run-5a قبل/جزئياً) | التقرير لا يُرجع ادّعاءات GT بنفس الصياغة؛ المهارة لا تفرض **claim→evidence id** صريحاً في القالب |
| **M08 إيجابيات كاذبة** | run-5b مبكراً (Zodiac/TWA/Aviation/Titanic) | المقيّم يطابق عبارات ممنوعة حتى داخل «لا تدّعِ X» — أُصلح جزئياً بنفي-نافذة |
| **M07/M05 حساسية صياغة** | payroll/warehouse مبكراً | الفجوات والأحداث تُسجَّل بمفردات مختلفة عن GT aliases |
| **سقف درجات ~1.0** | run-5b و run-org-sk | المنتج يعرف «كيف ينجح البنchmark»؛ ليس وكيلاً أعمى |

### 2.3 ما لم يُقَس بعد (فجوة منهجية حرجة)

1. **وكيل حر / نموذج** يقرأ `source_packet` فقط دون `CASE_INTEL` ولا `ground_truth`.  
2. **حزم مصادر غنية** (متعددة الصفحات، متناقضة، مشتتة) بدل مقتطفات قصيرة.  
3. **تسرّب تلميح** في BRIEF: `Truth band for designers` يجب ألا يراه الوكيل.  
4. **hard_fail_enabled: false** — لا عقوبة قصوى حالياً.  
5. **audit_vault.py** لا يغطي كل قواعد v0.2.0 الجديدة بعمق (informant verified، group-entity، cold-case folder، linkage notes).

---

## 3) تشخيص الفجوات حسب محور الإصلاح

### أ) فجوات المهارة (Skill) — مرشحة لـ v0.3.0

#### P0 — حرجة (تمنع دفاعاً تحقيقاً/قضائياً)

| ID | الفجوة | دليل من البنchmark / الضغط | الإصلاح المقترح |
|----|--------|---------------------------|------------------|
| **S-P0-1** | لا بروتوكول إلزامي **Claim Trace Matrix** في التقارير | M10 هش؛ `report_must_cite` يفشل بسهولة | قالب `Case-Report` + قسم إلزامي: جدول (ادّعاء → supporting-notes/evidence-id → support-level) |
| **S-P0-2** | Informant/Wiretap: قواعد «لا verified» غير مُنفَّذة آلياً بقوة | حزم ORG/INFORMANT؛ المهارة توثّق لكن audit لا يفرض | `audit_vault.py`: critical إذا `informant-testimony` أو wiretap `verified` بلا `credibility-assessment` / `legal-authorization` |
| **S-P0-3** | منع الاختلاق عند **group-entity-only** غير مُدقَّق آلياً | SK-RIPPER/GREENRIVER/TITANIC/OSAGE | audit + قاعدة SKILL: إذا `group-entity` للضحايا وعدد named-individuals=0، أي Person role=victim بأسماء جديدة → major/critical |
| **S-P0-4** | **Readiness Gate** غير قابل للقياس من داخل الـ vault | M11 يعتمد heuristics؛ court-file قد يُنشأ خطأ | ملف `00-Scaffold/Readiness-Checklist.md` + حقول YAML على التقرير `readiness-passed: false` افتراضياً |

#### P1 — جوهرية (تحسّن مقاومة التحيز وجودة الاستدلال)

| ID | الفجوة | الإصلاح المقترح |
|----|--------|------------------|
| **S-P1-1** | Counter «شكلي» (رابط فقط) بلا مضمون موضوعي | قاعدة: body counter ≥ N حرف + themes إلزامية في YAML `counter-themes: []`؛ audit يتحقق substantive |
| **S-P1-2** | لا نوع ملاحظة **Linkage / Series-Pattern** للسلاسل | قالب `Series-Linkage.md` تحت `05-Analysis/` + حقول: inclusion-criteria، peripheral-cases، confidence |
| **S-P1-3** | لا نوع **Enterprise / Predicate** للجريمة المنظمة | قالب `Enterprise-Map.md` + حقول predicates، org-roles، financial-layer |
| **S-P1-4** | Coverage-Ledger بلا schema ثابت للفجوات | YAML في Ledger: `gaps: [{id, description, phase_id, status}]` لتثبيت M07 |
| **S-P1-5** | Timeline: لا تمييز series-index vs single-incident | إرشاد + حقل `event-role: index \| peripheral \| communication \| financial` |
| **S-P1-6** | `status: open` وغيره خارج VALID_STATUSES يظهر في fixtures | توحيد الحالات؛ contradiction → `draft`/`unverified` فقط |

#### P2 — تحسينات (قابلية الاستخدام والتوسع)

| ID | الفجوة | الإصلاح |
|----|--------|---------|
| **S-P2-1** | Canvas بروتوكولات لا تُحدَّث من الأدلة آلياً | دليل «minimal canvas sync» بعد كل ingest |
| **S-P2-2** | دليل المحقق لا يغطي serial linkage / RICO | فصول في `guide-for-investigator.md` |
| **S-P2-3** | لا أمثلة vault ذهبية (golden) في المستودع | `examples/golden-CASE-FICT-WAREHOUSE` مصغّر |
| **S-P2-4** | version string في audit ما زال يذكر 0.1.0 | مزامنة الإصدارات |

### ب) فجوات البنchmark (Harness) — حتى لا نخدع أنفسنا

| ID | الفجوة | الإصلاح |
|----|--------|---------|
| **B-P0-1** | Baseline builder ≈ oracle → سقف 1.0 | فصل مسارات: `producer=baseline` vs `producer=agent`؛ لا تُحسب baseline وحدها «نجاح مهارة» |
| **B-P0-2** | تسرّب `Truth band for designers` في BRIEF | إزالة من `source_packet`؛ نقلها إلى `meta/designer_notes.md` (غير مرئي للوكيل) |
| **B-P0-3** | حزم المصادر سطحية | ترقية الحزم الحرجة (ORG/SK) إلى 4–8 مستندات + تناقضات صريحة |
| **B-P1-1** | M08 يضرب النفي | إبقاء negation-window + قائمة أنماط «affirmative-only» |
| **B-P1-2** | M10 يعتمد تشابه نصي | قبول جدول claim-id في التقرير أو wikilink لـ RC-* |
| **B-P1-3** | hard_fail معطّل | تفعيل على مسار agent؛ الإبقاء اختيارياً على baseline |
| **B-P1-4** | لا runner لوكيل حر | `tools/run_agent_protocol.md` + سكربت تجميع مخرجات فقط |
| **B-P2-1** | لا مقارنة بين إصدارات المهارة | `aggregate` يكتب `skill_version` + diff جداول |

### ج) فجوات الحزم (Case packs) — محتوى الضغط

| ID | المطلوب | على أي قضايا أولاً |
|----|---------|---------------------|
| **C-P0-1** | إخفاء designer truth band | كل BRIEF |
| **C-P1-1** | إثراء ORG: مخططات تحويلات، ملكية متضاربة | 021–025 |
| **C-P1-2** | إثراء SK: معايير linkage + حالة peripheral صريحة | 026–030 |
| **C-P1-3** | traps أقوى: confessions مزيفة، lab «مؤكد» كفخ | Informant, Corridor, Port |
| **C-P2-1** | حزم «adversarial agent」 منخفضة الجودة كـ fixtures | sample_vault_biased |

---

## 4) خريطة الأولويات الزمنية (مقترحة)

```
المرحلة 0 (فوري، 1–2 أيام)     ← صدق القياس
  B-P0-2  إزالة تسرّب truth band من BRIEF
  B-P0-1  وسم producer في النتائج + تقرير «لا تخلط baseline بـ agent»
  S-P2-4  مزامنة أرقام الإصدار في audit

المرحلة 1 (v0.3.0-core، أسبوع)  ← دفاع تحقيقي
  S-P0-1  Claim Trace Matrix في Reporting
  S-P0-2  audit informant/wiretap
  S-P0-3  audit group-entity invent-names
  S-P0-4  Readiness-Checklist + YAML على التقارير
  B-P1-1  تثبيت M08 negation
  B-P1-2  M10 claim-id

المرحلة 2 (v0.3.0-domain، أسبوع) ← ORG + Serial
  S-P1-2  Series-Linkage template
  S-P1-3  Enterprise-Map template
  S-P1-4  Coverage-Ledger gaps schema
  C-P1-1/2 إثراء 10 حزم ORG/SK
  تحديث taxonomy + guide + anti-drift

المرحلة 3 (v0.3.1-eval)         ← بنشمارك حقيقي للوكيل
  B-P1-3/4 hard_fail + agent protocol
  C-P0/P1 حزم غنية + traps
  إعادة تشغيل: baseline vs agent على 10 قضايا ORG/SK
  قبول v0.3.x فقط إذا تحسّن agent أو ثبتت فجوات موثّقة
```

---

## 5) مواصفات إصلاحات المهارة التفصيلية (v0.3.0)

### 5.1 Reporting — Claim Trace Matrix (S-P0-1)

**الملفات:** `assets/templates/` (Case-Report إن وُجد أو قسم في reporting-pipeline) · `references/reporting-pipeline.md` · `SKILL.md` § الوضع د  

**الشكل الإلزامي في كل تقرير غير-مسودة نهائية:**

```yaml
# frontmatter
type: case-report
claim-trace:
  - claim-id: RC-001
    claim: "..."
    evidence: ["[[EV-...]]"]
    support-level: moderate
```

وفي الجسم جدول Markdown مطابق.  
**قاعدة:** إن وُجد `06-Outputs/**/Court-File*` بلا claim-trace → Readiness فاشل.

### 5.2 audit_vault.py — قواعد جديدة (S-P0-2/3/4)

| code | severity | الشرط |
|------|----------|--------|
| `INFORMANT_VERIFIED_NO_CRED` | critical | type informant-testimony + status verified + لا credibility-assessment مكتمل |
| `WIRETAP_NO_AUTH` | critical | wiretap-evidence verified بلا legal-authorization |
| `GROUP_VICTIM_NAME_INVENT` | major/critical | (heuristic) شخص victim خارج قائمة named في group-entity عند وجود group-entity victims |
| `COURT_WITHOUT_READINESS` | critical | court-file و readiness-passed != true |
| `PRIMARY_COUNTER_THIN` | major | counter رابط فقط أو body أقصر من الحد |
| `LEDGER_GAPS_UNSTRUCTURED` | minor | لا `gaps:` في Coverage-Ledger عند وجود مراحل |

### 5.3 قوالب نطاق ORG / Serial (S-P1-2/3)

**`Enterprise-Map.md`**
- org-nodes، roles، predicates، financial-edges، counter-enterprise-theory  

**`Series-Linkage.md`**
- series-id، inclusion-criteria، members[], peripheral[], linkage-confidence، alternative-cluster-hypothesis  

ربط إلزامي من الفرضية الرئيسية في قضايا domain_tags تحتوي organized-crime أو serial-offender / homicide series.

### 5.4 Coverage-Ledger gaps schema (S-P1-4)

```yaml
type: coverage-ledger
gaps:
  - id: GAP-DNA
    description: "..."
    phase_id: P2
    status: open   # open | mitigated | accepted-risk
```

---

## 6) مواصفات إصلاحات البنchmark

### 6.1 فصل المسارات

| مسار | producer | يُستخدم لـ |
|------|----------|-----------|
| `baseline` | build_run_vaults | انحدار هيكلي / regression للمهارة |
| `agent` | نموذج+مهارة فقط | قياس القدرة الحقيقية |
| `adversarial` | vault متعمد السوء | حساسية المقيّم |

التقرير النهائي للمهارة يجب أن يعرض **الثلاثة** أو على الأقل baseline+agent.

### 6.2 تنظيف الحزم

- سكربت `tools/sanitize_packets.py`: يحذف أسطر Truth band من كل BRIEF.  
- `designer_notes.md` بجانب ground_truth (خارج source_packet).

### 6.3 عتبات قبول الإصدار

| المعيار | Baseline | Agent (هدف v0.3) |
|---------|----------|------------------|
| mean case score | ≥ 0.95 | يُقاس ويُوثَّق (لا سقف مصطنع) |
| M08 mean | ≥ 0.95 | ≥ 0.85 |
| M10 mean | ≥ 0.90 | ≥ 0.70 |
| M11 mean | ≥ 0.95 | ≥ 0.80 |
| hard_fail rate (agent) | n/a | يُتابع؛ هدف تنازلي بين الإصدارات |
| audit critical على golden | 0 | 0 |

---

## 7) مصفوفة تتبّع (Backlog جاهز للتنفيذ)

| # | العمل | طبقة | أولوية | جهد تقريبي | يعتمد على |
|---|--------|------|--------|-------------|-----------|
| 1 | sanitize BRIEFs + designer_notes | Benchmark | P0 | S | — |
| 2 | وسم producer في score/aggregate | Benchmark | P0 | S | — |
| 3 | Claim-trace في reporting + قالب | Skill | P0 | M | — |
| 4 | قواعد audit informant/wiretap/group/court | Skill | P0 | M | 3 جزئياً |
| 5 | Readiness-Checklist template | Skill | P0 | S | 3 |
| 6 | M08/M10 scorer hardening | Benchmark | P1 | S | 1 |
| 7 | Series-Linkage + Enterprise-Map | Skill | P1 | M | taxonomy |
| 8 | Ledger gaps schema | Skill | P1 | S | 4 |
| 9 | إثراء 10 حزم ORG/SK | Benchmark | P1 | L | 1 |
| 10 | دليل investigator ORG/Serial | Skill | P2 | S | 7 |
| 11 | Agent run protocol + hard_fail | Benchmark | P1 | M | 1–6 |
| 12 | إعادة بنشمارك مقارنة 0.2 vs 0.3 | Both | P0 (إغلاق) | M | الكل |

S ≈ ساعات · M ≈ 1–3 أيام · L ≈ عدة أيام  

---

## 8) قرارات تصميم يجب تثبيتها قبل التنفيذ

1. **هل v0.3.0 يكسر توافق vaults قديمة؟**  
   - مقترح: الحقول الجديدة *موصى بها*؛ audit يحذّر (major) لا يفشل strict إلا مع `--strict-v03`.

2. **هل نمنع Court-File تماماً دون readiness؟**  
   - مقترح: نعم critical في audit + soft في المهارة (اكتب draft فقط).

3. **هل Group-Entity يمنع أي اسم ضحية؟**  
   - مقترح: يمنع فقط الأسماء *خارج* `named-individuals` و`entities` في scope القضية.

4. **هل البنchmark يبقى داخل المستودع العام؟**  
   - نعم مع قضايا منزوعة الحساسية؛ لا محتوى حسّاس تشغيلي.

---

## 9) تعريف «نجاح الإصلاح»

يُغلق بند الإصلاح فقط إذا:

1. وُجد PR/تغيير واضح في المهارة أو الحزام،  
2. أُضيف/حُدّث اختبار (fixture أو case)،  
3. أُعيد تشغيل البنchmark ذي الصلة وذُكر في CHANGELOG،  
4. الإجابة «نعم» على سؤال المحكمة/الإشراف (مبدأ 0.2.0).

---

## 11) حالة التنفيذ (2026-08-08)

| بند | الحالة |
|-----|--------|
| B-P0-2 sanitize BRIEFs + designer_notes | **تم** — 30/30 |
| B-P0-1 وسم producer | **تم** — score/run/aggregate/config |
| S-P0-1 Claim Trace + قوالب Case-Report/Court-File | **تم** |
| S-P0-2/3/4 audit informant/wiretap/group/court + Readiness | **تم** |
| S-P2-4 مزامنة إصدار audit 0.3.0 | **تم** |
| SKILL/CHANGELOG/references v0.3.0 | **تم** |
| P1 Series-Linkage / Enterprise-Map / Ledger gaps | **تم** (0.3.1) |
| مسار agent حر + hard_fail | **تم** — AGENT_RUN_PROTOCOL + prepare_agent_run + producer hard_fail |
| إثراء كل حزم ORG/SK 021–030 | **تم** — انظر PACKET_ENRICHMENT_LOG + BENCHMARK_TRANSPARENCY |
| وثيقة شفافية الإصدار | **تم** — `docs/BENCHMARK_TRANSPARENCY.md` |

---

## 10) الخلاصة

- نتائج **0.99** الحالية = **انحدار هيكلي ناجح للبروتوكول**، وليست شهادة اكتمال ضد وكيل حر.  
- أضعف إشارة كمية داخل المنهج الحالي: **تتبع ادّعاءات التقرير (M10)**.  
- أكبر فجوات نوعية للضغط القادم (ORG/Serial/Informant/Cold):  
  **claim-trace · audit enforcement · linkage/enterprise templates · تنظيف الحزم · مسار agent منفصل**.  
- خطة v0.3.0 أعلاه تحوّل دروس البنchmark إلى إصلاحات قابلة للتنفيذ والقياس.

---

## ملحق أ — مرجع التشغيلات

| Run | N | Mean | محتوى |
|-----|---|------|--------|
| run-5a | 5 | 0.976 | متنوعة (warehouse, payroll, Hudson, Cooper, labgap) |
| run-5b | 5 | 1.000 | حافة (informant, zodiac, TWA, Titanic, aviation) |
| run-org-sk | 10 | 1.000 | 5 جريمة منظمة + 5 تسلسلي |
| **مجموع مُقيَّم** | **20** | **≈0.994** | baseline producer |

## ملحق ب — ملفات يُتوقع لمسها في v0.3.0

```
SKILL.md
CHANGELOG.md
scripts/audit_vault.py
references/reporting-pipeline.md
references/note-types-taxonomy.md
references/yaml-frontmatter-standards.md
references/anti-drift-rules.md
references/guide-for-investigator.md
references/vault-quality-checklist.md
assets/templates/  (+ Case-Report, Series-Linkage, Enterprise-Map, Readiness-Checklist)
Benchmark v1/tools/*  (sanitize, scorer, aggregate)
Benchmark v1/cases/*/source_packet/BRIEF.md
```
