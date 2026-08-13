# استراتيجية Obsidian Native

## القرار المختصر

في `v0.4.x` يدعم المشروع **Dataview وBases بالتوازي**. لا نزيل Dataview، ولا نعيد كتابة القوالب أو الاستعلامات الموجودة قبل إصدار `v0.5` رسمي يعلن عقد التوافق ومسار migration. الهدف هو الاستفادة من الصيغ الأصلية في Obsidian تدريجياً دون كسر vault قائم أو جعل صحة الصيغة بديلاً عن صحة التحقيق.

> **Native format validity is necessary, not sufficient.**
> نجاح Markdown/YAML أو Canvas أو Bases في parser لا يثبت صحة الدليل أو الاستنتاج؛ `audit_vault.py` والـ Human Gate يظلان حاكمين للسلامة المنهجية.

## الوضع الحالي: v0.4.x

| المكوّن | الحالة الحالية | الاستخدام |
|---|---|---|
| Markdown + YAML frontmatter | أساسي | كل note type وقابل للعمل دون community plugin |
| Canvas | مدعوم | خرائط الفرضيات والعلاقات، مع JSON graph validation |
| Bases | مدعوم تدريجياً | views وformulas أصلية، مع validator syntax/contract |
| Dataview | مدعوم بالتوازي | استعلامات vault الحالية، ولا يزال مساراً مشروعاً للتوافق الخلفي |
| CLI validator | متاح | `scripts/validate_obsidian_native.py` |
| Audit validator | حاكم منهجي | `scripts/audit_vault.py --native` يجمع التدقيق مع native validation |

### لماذا لا نوقف Dataview الآن؟

هناك vaults وقوالب واستعلامات تاريخية تعتمد على Dataview، بينما Bases لا يغطي بعد كل حالات العرض أو التصفية أو التوافق المطلوب. الإيقاف المبكر يخلق migration مفاجئة ويحوّل تغيير العرض إلى خطر على قابلية القراءة والتدقيق. لذلك يبقى Dataview **واجهة قراءة/استكشاف**، ولا يغيّر قواعد provenance أو status أو Human Gate.

## العلاقة بين Dataview وBases

Dataview وBases طبقتا عرض واستعلام، وليستا مصدر الحقيقة. المصدر هو Markdown/frontmatter والعلاقات الموثقة وملفات الأدلة وCoC. يمكن للـ note أن يظهر في Dataview وBase معاً إذا قرأا نفس الحقول المعيارية.

| الحاجة | Dataview | Bases | سياسة المشروع |
|---|---|---|---|
| جدول سريع لقائمة notes | query | table view | اسمح بالاثنين، واجعل الحقول متطابقة |
| filter بسيط حسب status/zone | قوي في vault قائم | native ومرئي | ابدأ بإصدار Base موازي دون حذف query |
| formulas | تعبيرات Dataview | `formulas` داخل `.base` | لا تنقل formula قبل تعريفها واختبارها |
| portability | يحتاج plugin | native format | استخدم Bases للمخرجات الجديدة عندما يغطي الحالة |
| auditability | query غير كافٍ | file قابل للفحص | افحص المصدر بـ validator وaudit لا بالعرض |

### قواعد التعايش

1. لا تغيّر أسماء frontmatter لتناسب صيغة واحدة دون migration موثق.
2. لا تجعل Dataview query أو Base view يكتب إلى Evidence أو يغيّر `status`.
3. حافظ على query القديم عند إضافة `.base` مكافئ، واذكر الاثنين في الوثيقة أو template.
4. اعتبر Broken wikilink وinvalid YAML أخطاء جودة مستقلة عن نجاح query.
5. لا تستخدم `.base` كـ ground truth لنتيجة Benchmark؛ النتيجة تقاس على vault المصدر والـ audit.

## ماذا يفحص `validate_obsidian_native.py`؟

المدقق حتمي ومحدود النطاق. يفحص الصياغة والروابط البيانية، لا حقيقة الادعاء:

### Markdown

يفحص وجود YAML frontmatter على الأقل كتحذير، وأن يكون frontmatter mapping صالحاً، ويرصد wikilinks التي لا يمكن حلها من أسماء notes المعروفة.

### Canvas

يفحص JSON root، وجود arrays لـ `nodes` و`edges`، node IDs، أنواع nodes (`text`, `file`, `link`, `group`)، الإحداثيات الهندسية، الحقول الخاصة بالنص/الملف/الرابط، edges dangling، sides/ends، وتكرار IDs.

### Bases

يفحص YAML، وأن يكون root mapping، وأن تكون `formulas` mapping، وأن كل `formula.NAME` المشار إليه في properties/views/summaries معرف، وأن تكون views list من الأنواع `table`, `cards`, `list`, `map`.

### وضعا التشغيل

```bash
# تحذيرات الصيغة ظاهرة لكن لا تفشل العملية إلا عند errors
python3 scripts/validate_obsidian_native.py /path/to/vault

# fail-closed للترحيل أو CI: يفشل عند errors وwarnings
python3 scripts/validate_obsidian_native.py /path/to/vault --strict

# ربط الصياغة بالتدقيق المنهجي
python3 scripts/audit_vault.py /path/to/vault --strict --native
```

لا يزيل validator الملفات، ولا يصلحها تلقائياً، ولا يقرر أن note صار Evidence. التصحيح يبقى تغييراً قابلاً للمراجعة.

## مسار التطور المقترح

### المرحلة A — v0.4.x: parallel support

- تثبيت field names وnote taxonomy.
- إضافة `.base` فقط حيث توجد فائدة واضحة، مع إبقاء Dataview query المكافئ.
- تشغيل native validator ضمن التدقيق أو قبل التسليم.
- تسجيل الفروق بين Dataview وBases كمسألة توافق، لا كفشل منهجي.

### المرحلة B — v0.5: migration contract

لا يبدأ الإيقاف التدريجي إلا إذا صدر `v0.5` رسمياً ومعه:

- جدول توافق Dataview → Bases لكل query مدعوم.
- `MIGRATION_GUIDE.md` وحالات قبل/بعد قابلة للاختبار.
- validator يتحقق من الحقول المعيارية ووجود view بديل.
- فترة deprecation معلنة، مع إبقاء قراءة Dataview خلال فترة الانتقال.
- benchmark/regression يثبت عدم فقدان التغطية أو traceability.

### المرحلة C — بعد v0.5: native-first where safe

- تكون Bases هي الخيار الافتراضي للمخرجات الجديدة التي يغطيها العقد.
- تبقى Dataview compatibility layer للـ vaults القديمة والحالات التي لا يغطيها Bases.
- لا تُحذف query إلا بعد وجود بديل مكافئ، وقرار موثق، واختبار migration.
- أي feature غير مغطاة تعود إلى Markdown/frontmatter بدلاً من hack غير قابل للتدقيق.

## سياسة كتابة القوالب

القالب الجديد يجب أن يعمل دون أن يتطلب Dataview لقراءة المحتوى الأساسي. استخدم frontmatter واضحاً وثابتاً، واجعل Dataview/Base طبقة عرض اختيارية. عند تقديم `.base`، أرفق مثالاً بالـ fields التي يعتمد عليها ونتيجة validator المتوقعة.

## قائمة ترحيل مختصرة

1. جرد queries وحقولها قبل لمس أي ملف.
2. تحديد query الذي يملك Base equivalent فعلياً، وليس مجرد view مشابه.
3. إنشاء `.base` في namespace غير حرج وتشغيل native validator.
4. مقارنة صفوف/filters يدوياً أو باختبار fixture.
5. إبقاء Dataview query أثناء deprecation window.
6. تحديث الوثائق والروابط وCHANGELOG فقط بعد مراجعة بشرية.
7. عدم تغيير Evidence أو status أو readiness كأثر جانبي للترحيل.

## ما لا تفعله هذه الاستراتيجية

لا تعد هذه الوثيقة بإزالة Dataview، ولا تجعل Bases بديلاً عن `audit_vault.py`، ولا تفترض أن كل Dataview query قابل للتحويل آلياً. كما لا تنقل القرار من الإنسان إلى parser: الصيغ الأصلية تحمي قابلية النقل والتدقيق، بينما قواعد التحقيق تحمي المعنى.
