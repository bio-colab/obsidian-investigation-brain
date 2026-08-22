# مِحَكّ الدماغ التحقيقي — `obsidian-investigation-brain`

مهارة (Skill) لبناء وإدارة **vault أوبسيديان** كمرجع تحقيقي موثوق مضاد للانحراف والتحيز.

**الإصدار:** 0.4.2
**مبني على:** [Obsidian Research Brain Skill](https://github.com/bio-colab/obsidian-research-brain-skill) (v1.1.9)

### Benchmark اختياري للمطورين

`Benchmark v1/` ليس مطلوباً لاستخدام المهارة أو لإدارة قضية يومية. هو حزام Advanced لتقييم البروتوكول على حزم تدريبية ومقارنة baseline مع agent. عند استخدامه، راجع [`docs/BENCHMARK_TRANSPARENCY.md`](docs/BENCHMARK_TRANSPARENCY.md)، ولا تخلط درجات **baseline** بدرجات **agent**.

**خرائط القراءة:** [`ARCHITECTURE.md`](ARCHITECTURE.md) للمعمارية الموحدة، [`OBSIDIAN_NATIVE_STRATEGY.md`](OBSIDIAN_NATIVE_STRATEGY.md) لاستراتيجية Dataview/Bases، و[`DEVELOPMENT.md`](DEVELOPMENT.md) و[`CONTRIBUTING.md`](CONTRIBUTING.md) للمطورين.

## اختر مسار الاستخدام

| المسار | لمن؟ | ابدأ بـ | لا تحتاجه الآن |
|---|---|---|---|
| **Basic** | الهاوي أو المحقق الذي يريد تنظيم قضية واحدة | [`references/guide-for-investigator.md`](references/guide-for-investigator.md)، ثم أوضاع Scaffold/Management/Audit/Reporting | Benchmark، Self-Tooling، وSwarm |
| **Advanced** | المطور أو الفريق الذي يحتاج أدوات قابلة للتتبع أو مقارنة منهجية | [`ARCHITECTURE.md`](ARCHITECTURE.md)، [`docs/SELF_TOOLING_INTEGRATION.md`](docs/SELF_TOOLING_INTEGRATION.md)، و[`swarm-wrapper/README.md`](swarm-wrapper/README.md) | لا تستخدم هذه الطبقة قبل استقرار vault الأساسي |

**قاعدة عملية:** ابدأ بـBasic، ولا تنتقل إلى Advanced إلا عند وجود سؤال تحليلي أو حاجة تشغيلية محددة. `Benchmark v1/` حزام تطوير اختياري، وليس جزءاً من العمل اليومي أو شرطاً لاستخدام المهارة.

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
- **Dynamic Tool Factory** لبناء scaffold صغير لكل سؤال تحليلي، مع discard-early بدلاً من مكتبة ضخمة
- **External Decision Memory** مع decision trace وmemory snapshot للاستئناف والتدقيق
- **Bounded Investigation Swarm MVP** لتنسيق proposals متعددة الوكلاء داخل namespace مستقل مع conflict report وHuman Gate
- **Timeline-first** · **Human Gate** · **Gap Intelligence**
- Canvas كبروتوكولات عمل + `audit_vault.py` (قواعد v0.4+)
- حزام بنشمارك اختياري: `Benchmark v1/` (30 قضية تدريبية + مقيّم)

---

## Quick Start — المسار الأساسي

1. فعّل المهارة واطلب بناء vault قضية من رقم/اسم القضية، النطاق، وخطة التحقيق إن وُجدت.
2. ابدأ بـ **الوضع أ (Scaffold)**، ثم اقرأ `AGENTS.md` و`Case-Scope.md` داخل vault.
3. أضف الأدلة والكيانات والفرضيات في **الوضع ب (Management)**؛ Evidence لا يحتوي إلا ما له مصدر حقيقي وسجل حفظ مناسب.
4. شغّل **الوضع ج (Audit)** قبل أي تقرير، ثم استخدم **الوضع د (Reporting)** عند اكتمال الجاهزية.

في الاستخدام الأساسي لا تحتاج إلى Benchmark أو Self-Tooling أو Swarm. عند اتخاذ قرار مهم استخدم `scripts/case_memory.py add/resume`؛ يسجل القرار المختصر ولا يسجل سلسلة التفكير السرية.

## المسار المتقدم — عند الحاجة فقط

عند وجود سؤال تحليلي محدد، أنشئ scaffold عبر `scripts/tool_factory.py`، أضف fixture صغيراً، ثم شغّله عبر `scripts/case_tooling.py`؛ التنفيذ fail-closed عند غياب backend عازل. وللتنسيق متعدد الوكلاء استخدم `swarm-wrapper/run.py` في `dry-run` ثم افحص النتائج بـ `scripts/validate_swarm.py`. تبقى كل المخرجات Proposals/Analysis ويظل Human Gate إلزامياً.

**دليل مبسّط للمحقق:** [`references/guide-for-investigator.md`](references/guide-for-investigator.md)

**وثيقة الدمج التفصيلية:** [`docs/SELF_TOOLING_INTEGRATION.md`](docs/SELF_TOOLING_INTEGRATION.md)

**Swarm Wrapper MVP:** [`swarm-wrapper/README.md`](swarm-wrapper/README.md)

---

## هيكل المستودع

```
obsidian-investigation-brain/
├── SKILL.md                          # تعريف المهارة والسلوك
├── README.md
├── ARCHITECTURE.md                    # خريطة الطبقات والتكاملات
├── OBSIDIAN_NATIVE_STRATEGY.md       # استراتيجية Dataview/Bases
├── CONTRIBUTING.md
├── DEVELOPMENT.md
├── CHANGELOG.md
├── .github/workflows/ci.yml           # Linux CI
├── tests/                             # اختبارات القواعد والتدقيق
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
├── swarm-wrapper/                    # bounded multi-agent orchestration MVP
│   ├── models.py                     # Team/Proposal/Conflict/Gate contracts
│   ├── orchestrator.py               # dry-run + OpenMausBot adapter + fan-out
│   ├── vault.py                      # bounded artifacts and decision events
│   ├── run.py                        # validate/run CLI
│   └── examples/                     # safe training manifest
└── scripts/
    ├── audit_vault.py                # تدقيق حتمي معرفي
    ├── validate_obsidian_native.py   # تدقيق الصيغ الأصلية
    ├── case_tooling.py               # executor/manifest/logs
    ├── tool_factory.py               # scaffold صغير لكل سؤال تحليلي
    ├── case_memory.py                # decision trace + memory snapshot
    ├── tools-review.py               # curation دون حذف تلقائي
    └── validate_swarm.py              # فحص artifacts وHuman Gate دون promotion
```

---

## طبقات الدمج الثلاث

| الطبقة | الوظيفة | حدودها |
|---|---|---|
| Obsidian Native Formats | كتابة Markdown وCanvas وBases وتشغيل CLI اختيارياً | لا تثبت صحة المعرفة |
| Investigation Brain | Evidence، provenance، hypotheses، timeline، readiness | لا ينفذ كوداً ذاتياً غير معزول |
| ARC-style Self-Tooling | بناء parsers/analyzers/simulators وقت الحاجة عبر Tool Factory | لا يكتب Evidence ولا يرفع status تلقائياً |
| External Decision Memory | session.jsonl وmemory-snapshot للاستئناف والتدقيق | لا يحفظ chain-of-thought الخام ولا يحل محل Evidence |

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
