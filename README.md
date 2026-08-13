# مِحَكّ الدماغ التحقيقي — `obsidian-investigation-brain`

مهارة (Skill) لبناء وإدارة **vault أوبسيديان** كمرجع تحقيقي موثوق مضاد للانحراف والتحيز.

**الإصدار:** 0.4.0
**مبني على:** [Obsidian Research Brain Skill](https://github.com/bio-colab/obsidian-research-brain-skill) (v1.1.9)

### شفافية البنشمارك (يُرجى القراءة قبل تفسير أي درجات)

هذا الإصدار طُوِّر تحت ضغط **Investigation Benchmark v1** (`Benchmark v1/`).  
الوثيقة المركزية للأثر والحدود والمنهج:

**→ [`docs/BENCHMARK_TRANSPARENCY.md`](docs/BENCHMARK_TRANSPARENCY.md)**

باختصار: درجات **baseline** تقيس قابلية التعبير عن البروتوكول؛ درجات **agent** (منفصلة) تقيس الوكيل الحر. لا تُخلط الاثنتان.

---

## لماذا هذه المهارة؟

التحقيق الطويل ينزلق بسهولة إلى:
- اختلاط الأدلة بالتخمين
- تحيز تأكيدي (البحث فقط عما يدعم الفرضية المفضلة)
- فقدان سلسلة حفظ الأدلة
- خط زمني مبعثر
- تقارير تتجاهل الفجوات

هذه المهارة تفرض وعاءً منظماً، وسلسلة إثبات قابلة للدفاع، ومقاومة صريحة للتحيز، دون استبدال الحكم المهني للمحقق.

---

## الميزات الرئيسية

- **أربعة أوضاع:** Scaffold · Management · Audit · Reporting
- فصل صارم بين Evidence والفرضيات ومنطقة الاستكشاف
- **سلسلة حفظ أدلة (Chain of Custody)** + **source-provenance** للأرشيف
- **Counter-Hypothesis** إلزامي لكل فرضية رئيسية
- **Claim Trace Matrix** + **Readiness-Checklist** (v0.3) — لا Court-File دون جاهزية
- **Series-Linkage** / **Enterprise-Map** (v0.3.1) لأنماط التسلسل والجريمة المنظمة
- **Native Format Contract** لـ Markdown وJSON Canvas وBases وCLI، مع `validate_obsidian_native.py`
- **Self-Tooling** لحالة القضية: أدوات مؤقتة، manifests، simulations، Tool-Audits، وcase logs
- **Timeline-first** · **Human Gate** · **Gap Intelligence**
- Canvas كبروتوكولات عمل + `audit_vault.py` (قواعد v0.4+)
- حزام بنشمارك اختياري: `Benchmark v1/` (30 قضية تدريبية + مقيّم)

---

## Quick Start

1. فعّل المهارة واطلب بناء vault قضية من: رقم/اسم القضية + النطاق + خطة التحقيق (أو المراحل) + أدوار الفريق إن وُجدت.
2. الوكيل يعمل بـ **الوضع أ (Scaffold)**.
3. أضف الأدلة والكيانات والفرضيات في **الوضع ب** — Evidence فقط بأدلة حقيقية + سلسلة حفظ + Human Gate عند الحاجة.
4. للتدقيق: **الوضع ج** أو شغّل `scripts/audit_vault.py`.
5. عند الحاجة إلى أداة تحليل مخصصة: أنشئها داخل `08-Tooling/Active/`، اكتب manifest، وشغّلها عبر `scripts/case_tooling.py`؛ التنفيذ fail-closed عند غياب backend عازل.
6. لإنتاج تقرير: **الوضع د (Reporting)**.

**دليل مبسّط للمحقق:** [`references/guide-for-investigator.md`](references/guide-for-investigator.md)
**وثيقة الدمج التفصيلية:** [`docs/SELF_TOOLING_INTEGRATION.md`](docs/SELF_TOOLING_INTEGRATION.md)

---

## هيكل المستودع

```
obsidian-investigation-brain/
├── SKILL.md                          # تعريف المهارة والسلوك
├── README.md
├── CHANGELOG.md
├── references/
│   ├── folder-structure.md
│   ├── note-types-taxonomy.md
│   ├── yaml-frontmatter-standards.md
│   ├── agents-instructions-template.md
│   ├── anti-drift-rules.md
│   ├── vault-quality-checklist.md
│   ├── visual-investigation-layer.md
│   ├── native-format-contract.md     # عقد Markdown/Canvas/Bases/CLI
│   ├── self-tooling-protocol.md      # الأدوات المؤقتة والعزل والسجلات
│   ├── reporting-pipeline.md
│   └── guide-for-investigator.md     # دليل المستخدم غير التقني
├── assets/templates/                 # قوالب الملاحظات + tooling + Canvas
│   └── canvases/                     # لوحات بروتوكولية
├── assets/tooling-examples/          # مثال metadata comparator + fixture + manifest
└── scripts/
    ├── audit_vault.py                # تدقيق حتمي معرفي
    ├── validate_obsidian_native.py   # تدقيق الصيغ الأصلية
    ├── case_tooling.py               # executor/manifest/logs
    └── tools-review.py               # curation دون حذف تلقائي
```

---

## طبقات الدمج الثلاث

| الطبقة | الوظيفة | حدودها |
|---|---|---|
| Obsidian Native Formats | كتابة Markdown وCanvas وBases وتشغيل CLI اختيارياً | لا تثبت صحة المعرفة |
| Investigation Brain | Evidence، provenance، hypotheses، timeline، readiness | لا ينفذ كوداً ذاتياً غير معزول |
| ARC-style Self-Tooling | بناء parsers/analyzers/simulators وقت الحاجة | لا يكتب Evidence ولا يرفع status تلقائياً |

تفاصيل العقد في [`references/native-format-contract.md`](references/native-format-contract.md) و[`references/self-tooling-protocol.md`](references/self-tooling-protocol.md).

## الأوضاع الأربعة

| الوضع | متى |
|-------|-----|
| **أ — Scaffold** | بناء vault قضية من الصفر |
| **ب — Management** | إضافة أدلة، كيانات، فرضيات، أحداث |
| **ج — Audit** | فحص سلسلة الحفظ، Counter، الفجوات |
| **د — Reporting** | تقرير قضية أو ملف محكمة |

---

## تحذيرات مهمة

- استخدم قضايا عامة أو تدريبية (مثل ملفات FBI Vault العامة) عند المشاركة أو النشر.
- القضايا الحقيقية الحساسة تبقى **محلية ومشفرة**.
- هذه أداة مساعدة للمحقق وليست بديلاً عن الإجراءات الرسمية أو الحكم القضائي.
- لا تُستخدم لاختلاق أدلة أو شهادات.
- الكود الذي ينشئه الوكيل يبقى داخل مساحة القضية، ولا يُشغّل على المضيف افتراضياً؛ يحتاج backend عازلاً مثل Docker/Podman/bwrap.
- نتائج الأدوات المؤقتة تُصنف Analysis/Exploration إلى أن تجتاز Tool-Audit وHuman Gate.

---

## التوافق

- أوبسيديان (محلي أولاً)
- إضافات موصى بها للطبقة البصرية: Dataview، Image Toolkit، Excalidraw، Leaflet / Map View
- يعمل مع وكلاء الذكاء الاصطناعي عبر تعليمات `AGENTS.md` داخل كل vault
