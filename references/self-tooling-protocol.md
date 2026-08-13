# بروتوكول Self-Tooling للتحقيق

## الفكرة

يمكن للوكيل أن يبني أداة صغيرة عند مواجهة شكل بيانات أو سؤال جديد، على طريقة `arc-code`. لكن الأداة هنا **مساعد تحليل** وليست مصدراً للحقيقة ولا بديلاً عن الحكم المهني. تنتج الأداة artifacts تحليلية قابلة لإعادة التشغيل، ولا تكتب مباشرة في `01-Evidence` ولا تعتمد نتيجة غير مراجعة لتغيير `status` إلى `verified`.

## دورة الحياة

| المرحلة | الناتج | حالة المعرفة |
|---|---|---|
| Discover | تعريف السؤال والمدخلات والقيود | `draft` |
| Build | ملف أو أكثر داخل `08-Tooling/Active/` | `draft` |
| Validate | فحوص static وfixtures وhash | `pending-human-review` |
| Simulate | تشغيل على نسخة من المدخلات دون تعديل المصدر | `analysis` أو `exploration` |
| Review | `Tool-Audit.md` وتوقيع/قرار بشري | `pending-human-review` |
| Promote | نسخ أداة عامة إلى `08-Tooling/Library/` | library معتمدة، لا Evidence |
| Retire | نقل الأداة الفاشلة أو القديمة إلى `Archive/` | `deprecated` |

## بنية مساحة القضية

```text
08-Tooling/
├── Active/                         # أدوات هذه القضية قيد التجربة
├── Library/                        # أدوات مرشحة لإعادة الاستخدام بعد مراجعة
├── Archive/                       # أدوات متقاعدة مع سبب الاحتفاظ أو الحذف
├── Manifests/                     # Tool-Manifest.md أو YAML
├── Audits/                        # Tool-Audit.md
├── Fixtures/                      # مدخلات صغيرة غير حساسة للاختبار
└── Runs/                          # مخرجات تشغيل قابلة لإعادة التحقق

case-logs/
├── session.jsonl                  # أحداث الوكيل والأوامر المختصرة
├── tool-runs.jsonl                # تشغيلات الأدوات وحالتها
└── decisions.md                   # قرارات بشرية وترقيات/رفض
```

## حدود الأمان

التنفيذ الافتراضي **مغلق** ما لم يتوفر backend عازل معروف. يقبل executor أحد backends التالية:

| backend | الوضع | الشبكة | متى يستخدم |
|---|---|---|---|
| `docker` | مفضل | مغلقة افتراضياً | تشغيل أداة في Container للقضية |
| `podman` | بديل | مغلقة افتراضياً | بيئات لا تستخدم Docker |
| `bwrap` | بديل محلي | يمكن منعها عبر namespaces | Linux مع bubblewrap |
| `host` | opt-in فقط | غير مضمون | تطوير محلي موثوق مع `--allow-host` |
| `none` | تحقق فقط | لا تشغيل | CI أو غياب runtime عازل |

لا يُسمح للأداة بالخروج من `case-root`. تُحظر الأسرار وملفات `.git` وبيئات المستخدم، ويُمرر `PATH` محدود. لا يُرفع أي ملف إلى الشبكة. إذا لم يتوفر runtime عازل، يخرج executor برسالة واضحة بدلاً من تنفيذ الكود على المضيف.

## Tool Factory — بناء صغير لا عبء دائم

يُستخدم `scripts/tool_factory.py` عندما لا تكفي الأدوات الموجودة. ينشئ الأمر scaffold واحداً صغيراً، وTool-Manifest، وTool-Audit، ويسجل سبب الإنشاء في الذاكرة الخارجية. لا يستدعي نموذجاً ولا ينفذ الكود؛ يترك للوكيل أو المحقق تعديل أقل جزء ممكن ثم إضافة fixture وتشغيله عبر `case_tooling.py`.

```bash
python3 scripts/tool_factory.py create <case-root> \\
  --tool-id TOOL-INVOICE-001 \\
  --kind analyzer \\
  --question "detect repeated invoice patterns" \\
  --input 08-Tooling/Fixtures/invoices.json
```

الهدف هو **أداة واحدة صغيرة لكل سؤال**، لا بناء مكتبة ضخمة مسبقاً. إذا لم يثبت scaffold فائدته في fixture صغير، يُؤرشف ولا يُوسع.

## الذاكرة الخارجية

السجل الكامل المهيكل هو `case-logs/session.jsonl`. يسجل الأحداث الملحوظة فقط: `summary` و`observation` و`decision` و`uncertainty` و`next_action` و`confidence` و`refs`، مع `event_id` ووقت التنفيذ. لا يسجل سلسلة التفكير السرية أو كل محتوى السياق.

يُنشأ تلقائياً `case-logs/memory-snapshot.md` كواجهة استئناف مختصرة. عند بدء جلسة أو استئنافها:

```bash
python3 scripts/case_memory.py resume <case-root> --last 12
```

وعند اتخاذ قرار أو تسجيل ملاحظة مهمة:

```bash
python3 scripts/case_memory.py add <case-root> \\
  --event-type decision \\
  --summary "تأجيل توسيع parser" \\
  --observation "fixture الأولي لا يغطي الحالات المركبة" \\
  --decision "نبقي الأداة صغيرة ونضيف fixture واحداً" \\
  --uncertainty "لم تُختبر مصادر متعددة بعد" \\
  --next-action "إضافة fixture ثانٍ" \\
  --ref 08-Tooling/Manifests/TOOL-INVOICE-001.md
```

تُسجل قرارات العمل المهمة فقط، لا كل أمر shell. هذا يجعل الذاكرة خفيفة ويمنح الوكيل نقطة استئناف قابلة للتدقيق من دون إغراق الـ vault أو السياق.

## Tool Manifest

كل أداة تملك manifest يثبت:

- `tool-id` و`version` و`status`.
- الغرض، المدخلات، المخرجات، وحدود الاستخدام.
- `entrypoint` و`runtime` و`network: denied`.
- `writes-to`، ويجب أن تكون داخل `08-Tooling/` أو `05-Analysis/` أو `02b-Exploration/` أو `case-logs/`.
- hash للكود، وhash للمدخلات عند التشغيل.
- `human-review: required` قبل promotion أو استخدام النتيجة في تقرير معتمد.

## Tool Audit

يسجل `Tool-Audit.md` ما الذي بُني ولماذا، نسخة الكود، الاختبارات، أمر التشغيل، backend، exit code، hashes، ومراجعة المخرجات. لا يُعد audit دليلاً على صحة النتيجة؛ هو سجل قابلية التتبع وقابلية إعادة التشغيل.

## Simulation Before Commit

قبل تنفيذ دفعة كبيرة أو اعتماد فرضية ناتجة عن analyzer، ينشئ الوكيل Simulation Run على نسخة read-only من البيانات. يسجل التوقع والمخرجات والاختلافات، ثم يطلب Human Gate عند وجود أثر على attribution أو evidence أو court-file.

## قواعد Evidence

الأداة لا تُنشئ دليلاً من لا شيء، ولا تحول نتائج تحليلية إلى دليل تشغيلي. إذا استُخدمت أداة لاستخراج بيانات من ملف مصدر، يبقى الملف المصدر هو Evidence، وتكون نتيجة الاستخراج `analysis` مع رابط إلى المصدر وTool-Audit. أي ترقية إلى Evidence تحتاج مصدر قابل للفحص ومراجعة بشرية.

## سياسة المكتبة

لا تُستدعى أداة من `Library/` تلقائياً لمجرد وجودها. يجب التحقق من hash، الإصدار، نطاق المدخلات، ونتيجة آخر audit. تنقل الأداة إلى Library فقط بعد نجاح fixtures ومراجعة بشرية وتوثيق سبب إعادة الاستخدام.
