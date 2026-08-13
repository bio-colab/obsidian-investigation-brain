# عقد صيغ Obsidian الأصلية — Native Format Contract

## الغرض

هذا العقد يدمج مبادئ `obsidian-skills` مع `obsidian-investigation-brain` دون نسخ مستودع خارجي داخل المهارة. وظيفته ضمان أن مخرجات الوكيل صالحة لعرضها وتحريرها في Obsidian، مع إبقاء **سلامة المعرفة** خاضعة لقواعد Investigation Brain لا لقواعد العرض.

> الصياغة الصحيحة تجعل الملاحظة قابلة للقراءة والتصفح؛ لكنها لا تجعل الادعاء صحيحاً. التحقق المعرفي يظل مرتبطاً بالمصدر، والحالة، وسلسلة الحفظ، والبوابة البشرية.

## نطاق الطبقة

تتعامل الطبقة مع أربعة امتدادات أساسية:

| الامتداد | ما يجب التحقق منه | ما لا تثبته الصيغة |
|---|---|---|
| `.md` | frontmatter، wikilinks، embeds، callouts، وعناوين قابلة للربط | صحة الدليل أو قوة الفرضية |
| `.canvas` | JSON صالح، معرفات فريدة، edges بلا مراجع معلقة، وأنواع nodes صحيحة | أن الرسم يعكس كامل الحقيقة |
| `.base` | YAML صالح، filters/views/formulas المشار إليها معرفة، وصياغة الاقتباسات سليمة | صحة الحسابات المهنية خارج الصيغة |
| Obsidian CLI | أوامر موجهة إلى vault مفتوح عند توفر CLI | نجاح التشغيل في بيئة لا تحتوي Obsidian |

## قواعد Markdown التحقيقية

تستخدم الروابط داخل الـ vault بصيغة `[[Note Name]]` أو `[[Note Name|Display Text]]`. تستخدم الروابط الخارجية بصيغة Markdown العادية. يمكن استخدام embeds وcallouts، لكن لا يجوز إخفاء حقيقة جوهرية داخل callout أو embed دون إبقاء الرابط إلى الملاحظة الأصلية.

كل ملاحظة تحقيقية تحمل frontmatter متوافقاً مع `yaml-frontmatter-standards.md`. يسمح العقد بإضافة `aliases` و`cssclasses` وخصائص Obsidian الأخرى، لكنه لا يغيّر الحقول الإلزامية `type` و`status` و`created` و`updated`.

## قواعد Canvas

كل Canvas يجب أن يكون JSON قابلاً للتحليل، وأن يحتوي معرفات فريدة لكل node وedge. يجب أن تشير `fromNode` و`toNode` إلى nodes موجودة. لا تُستخدم Canvas لإدخال دليل جديد؛ أي معلومة تظهر على اللوحة يجب أن تشير إلى ملاحظة مصدرية في vault.

## قواعد Bases

ملفات `.base` اختيارية. إذا أنشئت، يجب أن تكون YAML صالحة وأن تكون كل formula مستخدمة في `order` أو `properties` معرفة في قسم `formulas`. يجب وضع فلاتر واضحة تحدد المنطقة أو الوسم، وتجنب formulas التي تفترض وجود خاصية في كل الملاحظات دون حارس null.

## Obsidian CLI

يُستخدم CLI فقط إذا كان Obsidian مفتوحاً وظهر الأمر في PATH. المسار الأساسي للتحقق والتعديل هو الملفات المباشرة؛ لذلك لا تفشل اختبارات CI عندما لا يكون Obsidian موجوداً. أي عملية CLI تنفيذية تسجل الأمر ونتيجته في case log، ولا تعتمد عليها وحدها لإثبات حالة معرفية.

## بوابة التحقق

قبل اعتماد مخرج native-format:

1. شغّل `python3 scripts/validate_obsidian_native.py <vault>`.
2. أصلح JSON/YAML والروابط المعلقة قبل الانتقال إلى audit المعرفي.
3. شغّل `python3 scripts/audit_vault.py <vault> --strict`.
4. لا ترفع `status` أو `support-level` بسبب نجاح validator الصيغي وحده.

## مصدر التصميم

العقد مستلهم من `obsidian-markdown` و`json-canvas` و`obsidian-bases` و`obsidian-cli` في مستودع `kepano/obsidian-skills`، لكنه مكيّف هنا بحيث تكون قواعد التحقيق وHuman Gate أعلى أولوية من قواعد العرض.
