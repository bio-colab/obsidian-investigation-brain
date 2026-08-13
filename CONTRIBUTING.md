# المساهمة في `obsidian-investigation-brain`

شكراً لاهتمامك بالمساهمة. هذا المستودع بروتوكول تحقيقي، لذلك جودة التغيير لا تقاس بعدد الأسطر فقط؛ بل بقدرته على حفظ الفصل بين Evidence والفرضيات والتحليل الآلي، وبقابليته لإعادة التدقيق.

## قبل البدء

اقرأ `ARCHITECTURE.md` أولاً لفهم الطبقات، ثم راجع الوثيقة المتخصصة التي ستتغير. التغييرات التي تمس Evidence أو Human Gate أو Benchmark تحتاج وصفاً واضحاً للمخاطر والمنهجية. لا تستخدم قضية حقيقية حساسة في fixture أو مثال عام.

## أنواع المساهمات

| النوع | نقطة البداية | المطلوب |
|---|---|---|
| قاعدة منهجية | `SKILL.md` و`references/anti-drift-rules.md` | مثال، سبب، واختبار أو حالة تحقق |
| قالب أو منطقة | `assets/templates/` و`references/folder-structure.md` | frontmatter صالح وتحديث taxonomy |
| مدقق | `scripts/` | اختبار regression ومخرج JSON مستقر |
| Benchmark | `Benchmark v1/` | تحديث spec وشفافية producer وfixture مستقل |
| Swarm/Tooling | `swarm-wrapper/` و`08-Tooling` | حدود كتابة، Human Gate، واختبار fail-closed |
| توثيق | `ARCHITECTURE.md` أو `docs/` | روابط صحيحة وعدم تكرار متضارب |

## سير العمل المحلي

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements-dev.txt
pytest -q
python3 -m py_compile scripts/*.py swarm-wrapper/*.py
python3 scripts/validate_obsidian_native.py /path/to/vault --strict
python3 scripts/audit_vault.py /path/to/vault --strict --native
```

قبل فتح Pull Request شغّل `git diff --check`، وتأكد أن نتائج Benchmark أو ملفات `/tmp` لم تدخل Git، وأن كل تغيير في قاعدة حرجة يملك اختباراً أو تفسيراً موثقاً لسبب عدم الاختبار.

## قواعد السلامة

لا تضف كوداً ينفذ shell strings أو يكتب إلى `01-Evidence` تلقائياً. لا تُسجّل أسراراً أو سلسلة تفكير خاماً. مخرجات Self-Tooling وSwarm تبقى Analysis/Exploration أو `pending-human-review` إلى أن يراجعها إنسان. لا تخلط درجات `baseline` و`agent` في Benchmark.

## Pull Request

اجعل كل PR ذا غرض واحد. اذكر الملفات المتأثرة، القاعدة التي يحافظ عليها التغيير، الاختبارات التي شُغلت، وأي أثر على التوافق الخلفي. تغييرات Benchmark يجب أن توضّح هل تغيّر protocol أم metric أم fixture، وأن تحدّث وثيقة الشفافية عند الحاجة.

يُقبل التغيير عندما تكون الاختبارات خضراء، ولا توجد مسافات زائدة أو artifacts، وتظل الوثائق المتقاطعة متزامنة. الترخيص MIT؛ راجع `LICENSE` قبل إعادة استخدام مواد خارجية.
