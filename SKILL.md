---
name: obsidian-investigation-brain
description: مِحَكّ الدماغ التحقيقي — بناء وإدارة vault أوبسيديان كمرجع تحقيقي موثوق مضاد للانحراف والتحيز. استخدم عند بناء قضية من نطاق وخطة تحقيق، إدارة أدلة وكيانات وفرضيات، سلسلة حفظ أدلة، خط زمني، لوحة خيوط (Evidence Board)، كشف فجوات وتحقيق، مقاومة التحيز التأكيدي، إنتاج تقرير قضية أو ملف محكمة. تفصل صارماً بين Evidence المتحقق والفرضيات والاستكشاف. تُكمّل obsidian-research-brain ولا تستبدلها. الإصدار 0.1.2 — Chain of Custody + Counter-Hypotheses + Timeline-first + Visual Protocols.
metadata:
  type: workflow
  version: "0.1.2"
  based-on: obsidian-research-brain@1.1.9
---

# 🕵️ مِحَكّ الدماغ التحقيقي
## بناء وإدارة second brain تحقيقي + تنسيق تقرير القضية — فوق أوبسيديان

**الإصدار:** 0.1.2 (Chain of Custody · Counter-Hypotheses · Timeline-first · Human Gate · Gap Intelligence · Visual Protocols)  
**مبني على:** `obsidian-research-brain` v1.1.9

---

## 1. المهمة الواحدة

هذه المهارة تتقن شيئين مترابطين:

> **(أ) الوعاء:** تحويل قضية (نطاق + خطة تحقيق + فريق) إلى vault أوبسيديان منظم يمنع التوهان واختلاط الأدلة بالتخمين، مع فصل صارم بين المتحقق والفرضيات.  
> **(ب) التقرير:** عند وجود خطة تحقيق، تشغيل مسار إنتاج موجه بالمراحل عبر Coverage Ledger + سلسلة إثبات (Hypotheses + support-level)، دون اختلاق أدلة ودون تجاهل الفرضيات المضادة.

**ما تفعله:**
- ✅ سقالة كاملة لقضية واحدة من نطاق + خطة + أدوار فريق.
- ✅ إدارة أدلة → كيانات → فرضيات (Primary / Alternative / Counter / Rejected).
- ✅ سلسلة حفظ أدلة (Chain of Custody) إلزامية.
- ✅ خط زمني كعنصر أساسي (Timeline-first).
- ✅ لوحة خيوط بصرية (Evidence Board) عبر Canvas كبروتوكول عمل.
- ✅ مقاومة التحيز التأكيدي (Counter-Hypothesis إلزامي).
- ✅ تدقيق قابل للقياس + Gap Intelligence تحقيقي.
- ✅ Human Gate قبل اعتماد فرضية أو إغلاق مرحلة.

**ما لا تفعله:**
- ❌ اختلاق أدلة أو شهادات أو نتائج في `01-Evidence`.
- ❌ تجاهل فرضية مضادة لفرضية رئيسية.
- ❌ تجاوز Human Gate للمحتوى الحرج (فرضيات قوية، أدلة حساسة، تقرير نهائي).
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

7. **سلسلة حفظ الأدلة (Chain of Custody)** — كل دليل في `01-Evidence` يجب أن يكون له سجل في `Chain-of-Custody/`.

8. **سلسلة الإثبات (Provenance)** — كل فرضية جوهرية قابلة للتتبع إلى أدلة عبر `supporting-notes` + `support-level`.

9. **مقاومة التحيز** — كل فرضية Primary **يجب** أن يكون لها Counter-Hypothesis صريحة. الرفض يحتاج سبباً مكتوباً.

10. **بوابة المراجعة البشرية (Human Gate)** — الفرضيات القوية والأدلة الحساسة والتقارير تمر بـ `pending-human-review`.

11. **العرض ≠ الحقيقة** — Dashboard / Graph / Canvas أدوات عمل؛ الحقيقة في الملفات + YAML + Ledger + Chain-of-Custody.

---

## 3. أوضاع التشغيل (أ · ب · ج · د)

حدد الوضع من الطلب. أعلن الوضع. لا تخلط دون إعلان.

### الوضع أ — Scaffold Mode (بناء قضية)
**متى:** بناء vault قضية من الصفر.

**خطوات:**
1. استخرج: رقم/اسم القضية، نوع الجريمة (إن وُجد)، النطاق (داخل/خارج)، خطة التحقيق أو المراحل، أدوار الفريق.
2. اقرأ `references/folder-structure.md` و`note-types-taxonomy.md`.
3. ولّد الشجرة + القوالب + Case-Scope + Investigation-Plan + Team-Roles + AGENTS + Coverage-Ledger + Review-Queue.
4. **طبقة بصرية:** Dashboard + Graph-Setup + **Canvases كبروتوكولات** (Evidence-Board، Crime-Scene-Map، Timeline، Suspect-Profile، Link-Analysis).
5. فرضيات أولية → `03-Hypotheses` (Primary + Counter إلزامي) أو `02b-Exploration`.
6. ملخص قابل للقياس (مجلدات، قوالب، Scope، AGENTS، Ledger، Review-Queue، Dashboard، Canvas).

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
1. اقرأ Investigation-Plan + Coverage-Ledger.
2. **Plan-Driven:** الترتيب الافتراضي = مراحل الخطة.
3. **Readiness Gate** قبل اعتماد تقرير:
   - حد أدنى من أدلة verified المناسبة؛
   - الفرضيات الجوهرية مرتبطة بـ supporting-notes صالحة؛
   - وجود Counter لكل Primary أو تبرير صريح لغيابها؛
   - سلسلة حفظ مكتملة للأدلة المستخدمة.
4. بعد النثر: حدّث Ledger + Snapshots عند الحاجة؛ Macro-Review + Human Gate قبل الاعتماد النهائي.
5. التفاصيل: `references/reporting-pipeline.md`.

---

## 4. طيف الأدلة التحقيقية (Evidence Spectrum)

| طبقة | أمثلة | متى تُطلب |
|------|--------|-----------|
| **L-Physical** | بصمات، DNA، أسلحة، آثار مادية، أجسام | ربط مادي بمسرح أو شخص |
| **L-Digital** | سجلات هاتف، كاميرات، رسائل، بيانات موقع، hash | إثبات وجود رقمي أو تواصل |
| **L-Testimonial** | إفادة شاهد، اعتراف، مقابلة | مع ظروف الإدلاء وتاريخ الجلسة |
| **L-Documentary** | مستندات رسمية، سجلات بنكية، عقود، مراسلات | إثبات علاقات أو معاملات |
| **L-Temporal** | أحداث مؤرخة، Alibi، تناقضات زمنية | بناء الخط الزمني |
| **L-Behavioral** | نمط عمل، دوافع، سوابق موثقة | تحليل أسلوب ودافع |

**قاعدة الطيف:**  
اختر الطبقات حسب نوع القضية.  
إن ادّعى النص طبقة غير المدعومة في Evidence → **draft** أو وسم فجوة — لا ملء Evidence.

---

## 5. أنواع الملاحظات الأساسية

راجع `references/note-types-taxonomy.md`. أبرز الأنواع:

| نوع | مجلد رئيسي | ملاحظة |
|-----|------------|--------|
| Evidence (Physical/Digital/...) | `01-Evidence/` | مع رابط إلزامي إلى Chain-of-Custody |
| Chain-of-Custody Entry | `01-Evidence/Chain-of-Custody/` | جامع، وقت، مكان، حالة، شهود |
| Person / Location / Vehicle / Organization | `02-Entities/` | كيانات مع علاقات |
| Hypothesis | `03-Hypotheses/` | support-level + supporting-notes + counter عند Primary |
| Timeline-Event | `04-Timeline/Events/` | timestamp + مصدر |
| Alibi / Contradiction | `04-Timeline/` | مرتبطة بأشخاص وأحداث |
| Analysis | `05-Analysis/` | status يحدد المنطقة المنطقية |
| Coverage Ledger | `00-Scaffold/` | مراحل × فجوات × فرضيات |
| Case-Report / Court-File | `06-Outputs/` | مخرجات قابلة للتصدير |

---

## 6. معايير الجودة

### 6.1 صحة الوعاء
- مناطق سليمة، AGENTS موجود، Scope مكتوب.
- كل دليل له سلسلة حفظ.
- كل Primary لها Counter (أو تبرير مسجّل).
- لا يوجد محتوى verified بلا مصدر/دليل.
- Human Gate غير متجاوز.

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
| `scripts/audit_vault.py` | تدقيق آلي (لاحقاً) |

---

## 10. سجل الإصدارات

| الإصدار | التغيير |
|---------|---------|
| 0.1.2 | الإصدار الأولي — تكييف كامل من research-brain للتحقيق: Chain of Custody، Counter-Hypotheses، Timeline-first، أوضاع أ/ب/ج/د، طيف أدلة تحقيقي، Visual Protocols |
