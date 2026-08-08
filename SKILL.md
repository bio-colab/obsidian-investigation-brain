---
name: obsidian-investigation-brain
description: مِحَكّ الدماغ التحقيقي — بناء وإدارة vault أوبسيديان كمرجع تحقيقي موثوق مضاد للانحراف والتحيز. استخدم عند بناء قضية من نطاق وخطة تحقيق، إدارة أدلة وكيانات وفرضيات، سلسلة حفظ أدلة، خط زمني، لوحة خيوط (Evidence Board)، كشف فجوات وتحقيق، مقاومة التحيز التأكيدي، إنتاج تقرير قضية أو ملف محكمة. تفصل صارماً بين Evidence المتحقق والفرضيات والاستكشاف. تُكمّل obsidian-research-brain ولا تستبدلها. الإصدار 0.3.1 — Series-Linkage + Enterprise-Map + Claim-Trace + Readiness + structured gaps.
metadata:
  type: workflow
  version: "0.3.1"
  based-on: obsidian-research-brain@1.1.9
---

# 🕵️ مِحَكّ الدماغ التحقيقي
## بناء وإدارة second brain تحقيقي + تنسيق تقرير القضية — فوق أوبسيديان

**الإصدار:** 0.3.1 (Series-Linkage · Enterprise-Map · Ledger gaps schema · فوق 0.3.0 Claim-Trace/Readiness)  
**مبني على:** `obsidian-research-brain` v1.1.9

---

## 1. المهمة الواحدة

هذه المهارة تتقن شيئين مترابطين:

> **(أ) الوعاء:** تحويل قضية (نطاق + خطة تحقيق + فريق) إلى vault أوبسيديان منظم يمنع التوهان واختلاط الأدلة بالتخمين، مع فصل صارم بين المتحقق والفرضيات.  
> **(ب) التقرير:** عند وجود خطة تحقيق، تشغيل مسار إنتاج موجه بالمراحل عبر Coverage Ledger + سلسلة إثبات (Hypotheses + support-level) + **Claim Trace Matrix** + **Readiness Gate**، دون اختلاق أدلة ودون تجاهل الفرضيات المضادة.

**ما تفعله:**
- ✅ سقالة كاملة لقضية واحدة من نطاق + خطة + أدوار فريق + **Readiness-Checklist**.
- ✅ إدارة أدلة → كيانات → فرضيات (Primary / Alternative / Counter / Rejected).
- ✅ سلسلة حفظ أدلة (Chain of Custody) إلزامية + source-provenance للأرشيف.
- ✅ خط زمني كعنصر أساسي (Timeline-first).
- ✅ لوحة خيوط بصرية (Evidence Board) عبر Canvas كبروتوكول عمل.
- ✅ مقاومة التحيز التأكيدي (Counter-Hypothesis إلزامي + مضمون substantive).
- ✅ تدقيق قابل للقياس + Gap Intelligence تحقيقي (`audit_vault.py` v0.3).
- ✅ Human Gate قبل اعتماد فرضية أو إغلاق مرحلة.
- ✅ **Claim Trace** يربط كل ادعاء جوهري في التقرير بأدلة.

**ما لا تفعله:**
- ❌ اختلاق أدلة أو شهادات أو نتائج في `01-Evidence`.
- ❌ تجاهل فرضية مضادة لفرضية رئيسية.
- ❌ تجاوز Human Gate للمحتوى الحرج (فرضيات قوية، أدلة حساسة، تقرير نهائي).
- ❌ **Court-File** دون `readiness-passed: true` و claim-trace.
- ❌ `verified` لمخبر/wiretap دون مصداقية/تفويض.
- ❌ اختلاق أسماء ضحايا/ركاب عند استخدام group-entity.
- ❌ استخدام قضايا محلية حقيقية في مستودع عام أو مفتوح المصدر.
- ❌ استبدال الحكم المهني للمحقق أو المدعي العام.

---

## 2. المبادئ الحاكمة (غير قابلة للتفاوض)

1. **الفصل المناطقي** — `00-Scaffold` · `01-Evidence` · `02-Entities` · `03-Hypotheses` · `04-Timeline` · `05-Analysis` · `02b-Exploration` · `06-Outputs` · `99-Attachments`.
   - Evidence = أدلة مثبتة فقط (بعد Human Gate عند الحاجة).
   - Hypotheses = ادعاءات تحقيقية مع درجة قرينة.
   - Exploration = تفكير حر مؤقت (`status: exploration` فقط).

2. **لا معرفة مخترعة في Evidence** — أي توليد بلا مصدر/دليل/إفادة موثقة → Hypotheses أو Exploration أو رفض.

3. **كل ملاحظة تحمل `status`:** `verified` | `unverified` | `draft` | `stub` | `deprecated` | `exploration` | `pending-human-review` | `rejected`.

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

## 4. طيف الأدلة التحقيقية (Evidence Spectrum)

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
12. Informant/wiretap و group-entity: التزم بقواعد v0.3 في anti-drift و audit.

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
| `assets/templates/` | قوالب الملاحظات + Canvas |
| `scripts/audit_vault.py` | تدقيق آلي v0.3 (CoC، Counter، claim-trace، informant/wiretap، group، court) |

---

## 10. سجل الإصدارات

| الإصدار | التغيير |
|---------|---------|
| 0.3.1 | Series-Linkage · Enterprise-Map · Coverage-Ledger gaps schema · Agent run protocol (benchmark) |
| 0.3.0 | Claim Trace Matrix · Readiness-Checklist · Court-File gate · audit: INFORMANT/WIRETAP/GROUP/COURT/CLAIM_TRACE · من بنشمارك v1 |
| 0.2.0 | source-provenance · Technical/Data-Analysis · Cold-Case · Probable-Cause · Group-Entity · Vessel/Aircraft · Financial/Wiretap/Informant |
| 0.1.2 | الإصدار الأولي — تكييف كامل من research-brain للتحقيق: Chain of Custody، Counter-Hypotheses، Timeline-first، أوضاع أ/ب/ج/د، طيف أدلة تحقيقي، Visual Protocols |
