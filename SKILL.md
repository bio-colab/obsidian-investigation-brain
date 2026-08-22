---
name: obsidian-investigation-brain
description: مِحَكّ الدماغ التحقيقي — بناء وإدارة vault أوبسيديان كمرجع تحقيقي موثوق مضاد للانحراف والتحيز، مع طبقة Native Formats وSelf-Tooling معزولة قابلة للتتبع. استخدم عند بناء قضية من نطاق وخطة تحقيق، إدارة أدلة وكيانات وفرضيات، سلسلة حفظ أدلة، خط زمني، لوحة خيوط، كشف فجوات، تشغيل أدوات تحليل مؤقتة، ومقاومة التحيز التأكيدي. تفصل صارماً بين Evidence المتحقق والفرضيات والاستكشاف والتحليل الآلي. تُكمّل obsidian-research-brain ولا تستبدلها. الإصدار 0.4.2 — Native Formats + Dynamic Tool Factory + External Decision Memory + Bounded Investigation Swarm + Self-Tooling + Series-Linkage + Enterprise-Map + Claim-Trace + Readiness.
metadata:
  type: workflow
  version: "0.4.2"
  based-on: obsidian-research-brain@1.1.9
---

# 🕵️ مِحَكّ الدماغ التحقيقي
## بناء وإدارة second brain تحقيقي + تنسيق تقرير القضية — فوق أوبسيديان

**الإصدار:** 0.4.2 (Native Formats · Dynamic Tool Factory · External Decision Memory · Bounded Investigation Swarm · Self-Tooling · Series-Linkage · Enterprise-Map · Ledger gaps schema · فوق 0.3.0 Claim-Trace/Readiness)
**مبني على:** `obsidian-research-brain` v1.1.9

---

## 1. المهمة الواحدة

هذه المهارة تتقن شيئين مترابطين:

> **(أ) الوعاء:** تحويل قضية (نطاق + خطة تحقيق + فريق) إلى vault أوبسيديان منظم يمنع التوهان واختلاط الأدلة بالتخمين، مع فصل صارم بين المتحقق والفرضيات.  
> **(ب) التقرير:** عند وجود خطة تحقيق، تشغيل مسار إنتاج موجه بالمراحل عبر Coverage Ledger + سلسلة إثبات (Hypotheses + support-level) + **Claim Trace Matrix** + **Readiness Gate**، دون اختلاق أدلة ودون تجاهل الفرضيات المضادة.

### مسار الاستخدام الافتراضي

ابدأ دائماً بالمسار **Basic**: Scaffold ثم Management ثم Audit ثم Reporting. لا تُنشئ Self-Tooling أو Swarm ولا تشغّل Benchmark إلا إذا طلب المستخدم ذلك أو وُجد سؤال تحليلي محدد يبررها. هذا فصل في العرض وسير العمل، وليس تخفيفاً لقواعد Evidence أو Chain-of-Custody أو Human Gate.

| المستوى | ما يظهر أولاً | متى تنتقل؟ |
|---|---|---|
| **Basic** | vault، Evidence، Hypotheses، Timeline، Audit، Report | هذا هو المسار المعتاد للهاوي والمحقق |
| **Advanced** | Self-Tooling، External Memory، Swarm، Native validators، Benchmark | عند الحاجة إلى تحليل مخصص أو إعادة تشغيل أو مقارنة منهجية |

**ما تفعله:**
- ✅ سقالة كاملة لقضية واحدة من نطاق + خطة + أدوار فريق + **Readiness-Checklist**.
- ✅ إدارة أدلة → كيانات → فرضيات (Primary / Alternative / Counter / Rejected).
- ✅ سلسلة حفظ أدلة (Chain of Custody) إلزامية + source-provenance للأرشيف.
- ✅ خط زمني كعنصر أساسي (Timeline-first).
- ✅ لوحة خيوط بصرية (Evidence Board) عبر Canvas كبروتوكول عمل.
- ✅ مقاومة التحيز التأكيدي (Counter-Hypothesis إلزامي + مضمون substantive).
- ✅ تدقيق قابل للقياس + Gap Intelligence تحقيقي (`audit_vault.py` v0.4).
- ✅ Human Gate قبل اعتماد فرضية أو إغلاق مرحلة.
- ✅ **Claim Trace** يربط كل ادعاء جوهري في التقرير بأدلة.
- ✅ Native Format Contract لصياغة Obsidian Markdown وJSON Canvas وBases، مع validator مستقل.
- ✅ Self-Tooling للحالات: أدوات مؤقتة قابلة لإعادة التشغيل، manifests، audits، simulations، وسجل case خارجي.
- ✅ Tool Factory خفيف يبني scaffold واحداً لكل سؤال، بدلاً من تثبيت مكتبة أدوات ضخمة مسبقاً.
- ✅ External Decision Memory: `session.jsonl` للأحداث الملحوظة و`memory-snapshot.md` للاستئناف، دون حفظ سلسلة التفكير السرية.
- ✅ عزل fail-closed: لا تشغيل للكود الذاتي التوليد على المضيف عند غياب Docker/Podman/bwrap، ولا شبكة افتراضياً.
- ✅ Swarm Wrapper MVP: fan-out محدود، proposals مهيكلة، conflict report، consensus draft، وHuman Gate داخل namespace مستقل.
- ✅ OpenMausBot adapter اختياري: يستخدم bots محددة عبر loopback، ولا يعتمد على ask_bot الداخلي لتنسيق الفريق.

**ما لا تفعله:**
- ❌ اختلاق أدلة أو شهادات أو نتائج في `01-Evidence`.
- ❌ تجاهل فرضية مضادة لفرضية رئيسية.
- ❌ تجاوز Human Gate للمحتوى الحرج (فرضيات قوية، أدلة حساسة، تقرير نهائي).
- ❌ **Court-File** دون `readiness-passed: true` و claim-trace.
- ❌ `verified` لمخبر/wiretap دون مصداقية/تفويض.
- ❌ اختلاق أسماء ضحايا/ركاب عند استخدام group-entity.
- ❌ استخدام قضايا محلية حقيقية في مستودع عام أو مفتوح المصدر.
- ❌ استبدال الحكم المهني للمحقق أو المدعي العام.
- ❌ اعتبار اتفاق الوكلاء دليلاً مستقلاً أو ترقية Proposal إلى Evidence/Court-File تلقائياً.
- ❌ تشغيل swarm حي على قضية حساسة قبل تعطيل computer/Composio ووضع retention وredaction واضحين.

---

## 2. المبادئ الحاكمة (غير قابلة للتفاوض)

1. **الفصل المناطقي** — `00-Scaffold` · `01-Evidence` · `02-Entities` · `03-Hypotheses` · `04-Timeline` · `05-Analysis` · `02b-Exploration` · `06-Outputs` · `99-Attachments`.
   - Evidence = أدلة مثبتة فقط (بعد Human Gate عند الحاجة).
   - Hypotheses = ادعاءات تحقيقية مع درجة قرينة.
   - Exploration = تفكير حر مؤقت (`status: exploration` فقط).

2. **لا معرفة مخترعة في Evidence** — أي توليد بلا مصدر/دليل/إفادة موثقة → Hypotheses أو Exploration أو رفض.

3. **كل ملاحظة تحمل `status`:** `verified` | `unverified` | `draft` | `stub` | `deprecated` | `exploration` | `working` | `pending-human-review` | `rejected`.

4. **الـ vault يحمل تعليماته** — `AGENTS.md` إلزامي.

5. **مضاد الانحراف** — أسماء صريحة، Scope مكتوب، روابط حية، Changelog لقرارات النطاق والترقيات والرفض.

6. **Timeline-first** — الأحداث الزمنية عنصر أساسي وليست ملحقاً. أي ادعاء زمني يجب أن يرتبط بـ Event أو Alibi.

7. **سلسلة حفظ الأدلة (Chain of Custody) + Source Provenance** — كل دليل تشغيلي في `01-Evidence` يجب أن يكون له سجل CoC. المصادر الأرشيفية/العامة تستخدم `source-provenance` كبديل منطقي.

8. **سلسلة الإثبات (Provenance)** — كل فرضية جوهرية قابلة للتتبع إلى أدلة عبر `supporting-notes` + `support-level`.

9. **مقاومة التحيز** — كل فرضية Primary **يجب** أن يكون لها Counter-Hypothesis صريحة. الرفض يحتاج سبباً مكتوباً.

10. **بوابة المراجعة البشرية (Human Gate)** — الفرضيات القوية والأدلة الحساسة والتقارير تمر بـ `pending-human-review`.

11. **العرض ≠ الحقيقة** — Dashboard / Graph / Canvas أدوات عمل؛ الحقيقة في الملفات + YAML + Ledger + Chain-of-Custody.

12. **Claim Trace + Readiness (v0.3)** — كل تقرير معتمد يحمل `claim-trace`؛ Court-File ممنوع دون `readiness-passed: true` على Readiness-Checklist والتقرير.

---

## 3. أوضاع التشغيل (أ · ب · ج · د)

حدد الوضع من الطلب. أعلن الوضع. لا تخلط دون إعلان.

### الوضع أ — Scaffold Mode (بناء قضية)
**متى:** بناء vault قضية من الصفر.

**خطوات:**
1. استخرج: رقم/اسم القضية، نوع الجريمة (إن وُجد)، النطاق (داخل/خارج)، خطة التحقيق أو المراحل، أدوار الفريق.
2. اقرأ `references/folder-structure.md` و`note-types-taxonomy.md`.
3. ولّد الشجرة + القوالب + Case-Scope + Investigation-Plan + Team-Roles + AGENTS + Coverage-Ledger + Review-Queue + **Readiness-Checklist**.
4. **طبقة بصرية:** Dashboard + Graph-Setup + **Canvases كبروتوكولات** (Evidence-Board، Crime-Scene-Map، Timeline، Suspect-Profile، Link-Analysis).
5. فرضيات أولية → `03-Hypotheses` (Primary + Counter إلزامي) أو `02b-Exploration`.
6. ملخص قابل للقياس (مجلدات، قوالب، Scope، AGENTS، Ledger، Review-Queue، Readiness-Checklist، Dashboard، Canvas).

### الوضع ب — Management Mode (إدارة محتوى)
**متى:** إضافة دليل، كيان، حدث زمني، فرضية، تحديث حالة، ربط، ترقية من Exploration.

**خطوات:**
1. المنطقة أولاً (Evidence vs Hypotheses vs Exploration).
2. القالب + YAML المناسب (لـ Hypothesis: `support-level` + `supporting-notes` + `counter-hypothesis` عند Primary).
3. حدّث Coverage-Ledger و Review-Queue و Master-Timeline إن تغيّرت التغطية أو الحالة.
4. «تحقق» → فقط بعد دليل حقيقي + Human Gate عند الحاجة.
5. أي دليل جديد → سجل Chain-of-Custody فوراً.

### الوضع ج — Audit Mode (تدقيق الوعاء)
**متى:** فحص جودة vault، اختلاط مناطق، فجوات أدلة، غياب Counter، ثغرات Timeline، سلسلة حفظ.

**خطوات:**
1. شغّل `scripts/audit_vault.py` إن أمكن (أو فحص يدوي وفق القائمة).
2. `references/vault-quality-checklist.md` (يشمل Chain-of-Custody و Counter-Hypotheses و Human Gate).
3. Gap Intelligence تحقيقي: ما ينقص المرحلة؟ أي فرضية بلا Counter؟ أي دليل بلا سلسلة حفظ؟ أي فترة زمنية فارغة؟
4. بصري: Dashboard + Graph + مراجعة Canvas؛ Ledger لحالة الأدلة والفرضيات.

### الوضع د — Reporting Mode (إنتاج المخرجات)
**متى:** كتابة تقرير قضية، ملف محكمة، إحاطة، أو إغلاق مرحلة.

**خطوات إلزامية:**
1. اقرأ Investigation-Plan + Coverage-Ledger + **Readiness-Checklist**.
2. **Plan-Driven:** الترتيب الافتراضي = مراحل الخطة.
3. **Readiness Gate** قبل اعتماد تقرير أو أي Court-File:
   - حد أدنى من أدلة verified المناسبة؛
   - الفرضيات الجوهرية مرتبطة بـ supporting-notes صالحة؛
   - وجود Counter لكل Primary أو تبرير صريح لغيابها؛
   - سلسلة حفظ / source-provenance مكتملة للأدلة المستخدمة؛
   - **Claim Trace Matrix** (`claim-trace` في YAML + جدول)؛
   - `readiness-passed: true` فقط بعد اكتمال checklist.
4. ابنِ التقرير من قالب `Case-Report`؛ لا تُنشئ Court-File إن فشل readiness.
5. بعد النثر: حدّث Ledger + Snapshots عند الحاجة؛ Macro-Review + Human Gate قبل الاعتماد النهائي.
6. التفاصيل: `references/reporting-pipeline.md`.

---

## 4. طبقات التكامل الثلاث

### 4.1 طبقة Obsidian Native Formats

يضمن `references/native-format-contract.md` أن المخرجات قابلة للعرض والتحرير في Obsidian. تشمل الطبقة Markdown الخاص بـ Obsidian، wikilinks وembeds وcallouts، JSON Canvas، Bases، وObsidian CLI الاختياري. الصياغة لا تغيّر status أو support-level ولا تستبدل Human Gate.

### 4.2 طبقة Investigation Brain

تبقى قواعد Evidence وChain of Custody وCounter-Hypothesis وTimeline-first وClaim Trace وReadiness هي طبقة الحقيقة المنهجية. أي نتيجة آلية جديدة تُسجل أولاً كـ Analysis أو Exploration أو pending-human-review، مع رابط إلى الأداة والمدخلات.

### 4.3 طبقة ARC-style Self-Tooling

يمكن للوكيل أن ينشئ parser أو analyzer أو linker أو simulator صغيراً داخل `08-Tooling/Active/`. يبدأ ذلك عبر `scripts/tool_factory.py` الذي ينشئ scaffold واحداً وmanifest وaudit، ثم يُعدّل بأقل قدر ويُختبر على fixture صغير. يجب أن يعمل كل tool عبر `scripts/case_tooling.py` داخل backend عازل عند توفره. غياب backend عازل يؤدي إلى skip fail-closed، لا إلى تنفيذ صامت على المضيف. التفاصيل في `references/self-tooling-protocol.md`.

### 4.4 Swarm Wrapper MVP

`swarm-wrapper/` طبقة اختيارية تنسق أدواراً متعددة فوق vault القضية. تبدأ بـ Team Manifest، تثبت source snapshot hash، تشغّل fan-out محدوداً في `dry-run` أو عبر OpenMausBot loopback، ثم تكتب `proposals/` و`conflicts.md` و`consensus-draft.md` وHuman Gate داخل `08-Tooling/Swarm/`. لا تملك الطبقة دالة promotion ولا تكتب إلى `01-Evidence`. افحص المخرجات بـ `scripts/validate_swarm.py`. التفاصيل في `docs/INVESTIGATION_SWARM_MVP.md`.

### 4.5 الذاكرة والسجل

السجل الآلي في `case-logs/session.jsonl` يحفظ الأحداث الملحوظة: observation وdecision وuncertainty وnext-action وrefs، وتُفهرس تشغيلات الأدوات أيضاً في `case-logs/tool-runs.jsonl`. أما `case-logs/memory-snapshot.md` فهو عرض مختصر للاستئناف، لا نسخة من كامل السياق ولا سلسلة تفكير سرية. تبقى القرارات البشرية في `case-logs/decisions.md`. هذه السجلات تشرح كيف نتجت المخرجات ولا تحل محل Evidence أو CoC.

لتسجيل قرار مهم أو استئناف جلسة استخدم `scripts/case_memory.py add/resume`. لا تسجل كل أمر shell؛ سجّل ما يغيّر الفرضية أو الاختيار أو الخطوة التالية.

---

## 5. طيف الأدلة التحقيقية (Evidence Spectrum)

| طبقة | أمثلة | متى تُطلب |
|------|--------|-----------|
| **L-Physical** | بصمات، DNA، أسلحة، آثار مادية، أجسام | ربط مادي بمسرح أو شخص |
| **L-Digital** | سجلات هاتف، كاميرات، رسائل، بيانات موقع، hash، wiretap | إثبات وجود رقمي أو تواصل |
| **L-Testimonial** | إفادة شاهد، اعتراف، مقابلة، informant | مع ظروف الإدلاء + تقييم مصداقية عند الحاجة |
| **L-Documentary** | مستندات رسمية، سجلات بنكية، عقود، مراسلات، financial-record | إثبات علاقات أو معاملات |
| **L-Temporal** | أحداث مؤرخة، Alibi، تناقضات زمنية، تحذيرات طقس | بناء الخط الزمني |
| **L-Behavioral** | نمط عمل، دوافع، سوابق موثقة | تحليل أسلوب ودافع |
| **L-Archival** | وثائق أرشيفية منشورة (NARA, FBI Vault, NTSB…) | مصدر تاريخي أو رسمي — يستخدم source-provenance |
| **L-Technical** | محاكاة، نماذج، حسابات ثباتية، data-analysis | نتائج تحليل بيانات أو محاكاة (NTSB-style) |

**قاعدة الطيف:**  
اختر الطبقات حسب نوع القضية.  
إن ادّعى النص طبقة غير المدعومة في Evidence → **draft** أو وسم فجوة — لا ملء Evidence.  
للمصادر الأرشيفية: `source-provenance` بدلاً من (أو مع) Chain-of-Custody التشغيلي.

---

## 5. أنواع الملاحظات الأساسية

راجع `references/note-types-taxonomy.md`. أبرز الأنواع (محدثة v0.2.0):

| نوع | مجلد رئيسي | ملاحظة |
|-----|------------|--------|
| Evidence (Physical/Digital/…) | `01-Evidence/` | CoC تشغيلي أو source-provenance للأرشيف |
| Chain-of-Custody / Source-Provenance | `01-Evidence/...` | حسب طبيعة المصدر |
| Person / Group-Entity / Location / Vehicle (Vessel/Aircraft) / Organization | `02-Entities/` | + System-Failures / Regulatory-Gaps |
| Hypothesis | `03-Hypotheses/` | support-level + supporting-notes + counter عند Primary |
| Timeline-Event | `04-Timeline/Events/` | timestamp + era/period عند الحاجة |
| Alibi / Contradiction | `04-Timeline/` | مرتبطة بأشخاص وأحداث |
| Analysis / Data-Analysis / Safety-Culture | `05-Analysis/` | تقني + سلوكي |
| Series-Linkage | `05-Analysis/Series-Linkage/` | v0.3.1 — سلاسل / overlinking discipline |
| Enterprise-Map | `05-Analysis/Enterprise-Maps/` | v0.3.1 — جريمة منظمة / predicates |
| Coverage Ledger | `00-Scaffold/` | مراحل × فجوات منظمة (`gaps:`) |
| Tooling / Manifest / Audit / Simulation | `08-Tooling/` و`case-logs/` | أداة مؤقتة أو قابلة لإعادة الاستخدام، مع حدود وسجل تشغيل |
| Readiness-Checklist | `00-Scaffold/` | v0.3 — بوابة جاهزية قابلة للتدقيق |
| Case-Report / Court-File / Recommendations / Cold-Case-Report | `06-Outputs/` | + claim-trace + readiness-passed |
| financial-record / wiretap-evidence / informant-testimony | `01-Evidence/` | قوالب متخصصة |

---

## 6. معايير الجودة

### 6.1 صحة الوعاء
- مناطق سليمة، AGENTS موجود، Scope مكتوب، Readiness-Checklist موجود.
- كل دليل له سلسلة حفظ أو source-provenance.
- كل Primary لها Counter (أو تبرير مسجّل) بمضمون substantive.
- لا يوجد محتوى verified بلا مصدر/دليل.
- Human Gate غير متجاوز.
- التقارير المعتمدة/Court-File تحمل claim-trace؛ Court-File فقط مع readiness-passed.
- ملفات Markdown/Canvas/Bases تمر عبر validator native عند وجودها.
- كل Self-Tooling له manifest وTool-Audit، ونتائج التشغيل قابلة لإعادة الحساب من hashes والسجل.
- لا أداة تكتب خارج case-root أو ترفع Evidence/status تلقائياً.

### 6.2 Gap Intelligence تحقيقي
- % مراحل الخطة التي لها صف في Coverage-Ledger.
- أدلة بلا سلسلة حفظ.
- فرضيات Primary بلا Counter.
- فترات زمنية فارغة في Master-Timeline.
- تناقضات غير محلولة.
- أسئلة تحقيقية ما زالت ضعيفة الدعم.

---

## 7. التكامل

- **obsidian-research-brain:** الأصل المفاهيمي. هذه المهارة تكييف متخصص للتحقيق.
- **methodology-auditor:** يمكن استخدامه لتدقيق منطق الفرضيات عند الحاجة.
- لا تخلط بناء الوعاء بحكم قضائي نهائي أو باختبار أدلة مخبرية.

---

## 8. قواعد التنفيذ السريع

1. أعلن الوضع (أ/ب/ج/د).
2. اقرأ AGENTS + Case-Scope (+ Coverage-Ledger + Review-Queue عند الحاجة).
3. Evidence = أدلة حقيقية فقط + سلسلة حفظ.
4. كل Primary Hypothesis تحتاج Counter.
5. لا تفرط في التخمين داخل Evidence.
6. الفراغ المنظم خير من الاختلاق.
7. Timeline-first: اربط الادعاءات الزمنية بأحداث.
8. لا تتجاوز Human Gate.
9. Exploration حرية مضبوطة؛ الترقية لها بروتوكول صريح.
10. القضايا الحقيقية الحساسة تبقى محلية ومشفرة — لا تُرفع إلى مستودعات عامة.
11. Claim-trace قبل اعتماد التقرير؛ لا Court-File دون readiness.
12. **Informant/wiretap و group-entity: التزم بقواعد v0.3 في anti-drift و audit.
13. طبقة Obsidian الأصلية تحافظ على wikilinks وembeds وcallouts وJSON Canvas وBases صالحة، لكنها لا تمنح أي ادعاء صحة معرفية.
14. Self-Tooling يكتب فقط داخل حدود القضية، ويسجل command digest وhashes وexit code، ولا يرفع Evidence أو status تلقائياً.
15. شغّل `scripts/validate_obsidian_native.py` قبل `scripts/audit_vault.py` عند التعامل مع `.canvas` أو `.base` أو تغييرات Markdown البنيوية.
16. شغّل Swarm Wrapper أولاً في `dry-run`؛ كل Proposal غير معتمد، وكل consensus draft يحتاج Human Gate، و`validate_swarm.py` قبل أي مراجعة بشرية.

---

## 9. الملفات المرجعية والأصول

| الملف | الغرض |
|-------|------|
| `references/folder-structure.md` | الشجرة المعيارية |
| `references/note-types-taxonomy.md` | أنواع الملاحظات + الحقول |
| `references/yaml-frontmatter-standards.md` | معايير YAML |
| `references/anti-drift-rules.md` | قواعد منع الانحراف |
| `references/agents-instructions-template.md` | قالب AGENTS |
| `references/vault-quality-checklist.md` | قائمة تدقيق |
| `references/reporting-pipeline.md` | مسار إنتاج التقارير |
| `references/visual-investigation-layer.md` | الطبقة البصرية + بروتوكولات Canvas |
| `assets/templates/` | قوالب الملاحظات + Canvas + Tool Manifest/Audit/Simulation |
| `scripts/audit_vault.py` | تدقيق آلي v0.4 (CoC، Counter، claim-trace، informant/wiretap، group، court، tooling boundaries) |
| `scripts/validate_obsidian_native.py` | فحص Markdown/frontmatter وCanvas JSON وBases YAML والروابط |
| `scripts/case_tooling.py` | إنشاء workspace وتشغيل الأدوات داخل backend عازل وتسجيل hashes/events |
| `scripts/tools-review.py` | مراجعة curation دون حذف أو promotion تلقائي |
| `swarm-wrapper/` | تنسيق bounded multi-agent proposals وHuman Gate دون promotion |
| `scripts/validate_swarm.py` | فحص مخرجات Swarm وحدودها وسجلها |

---

## 10. سجل الإصدارات

| الإصدار | التغيير |
|---------|---------|
| 0.4.2 | Bounded Investigation Swarm MVP · Team/Proposal/Conflict/Gate contracts · OpenMausBot adapter · vault validator |
| 0.4.1 | Dynamic Tool Factory · External Decision Memory · compact recovery snapshots · audit health checks |
| 0.4.0 | Native Format Contract + validator · Self-Tooling workspace/executor/audit/logs · fail-closed sandbox policy |
| 0.3.1 | Series-Linkage · Enterprise-Map · Coverage-Ledger gaps schema · Agent run protocol (benchmark) |
| 0.3.0 | Claim Trace Matrix · Readiness-Checklist · Court-File gate · audit: INFORMANT/WIRETAP/GROUP/COURT/CLAIM_TRACE · من بنشمارك v1 |
| 0.2.0 | source-provenance · Technical/Data-Analysis · Cold-Case · Probable-Cause · Group-Entity · Vessel/Aircraft · Financial/Wiretap/Informant |
| 0.1.2 | الإصدار الأولي — تكييف كامل من research-brain للتحقيق: Chain of Custody، Counter-Hypotheses، Timeline-first، أوضاع أ/ب/ج/د، طيف أدلة تحقيقي، Visual Protocols |
