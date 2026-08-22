# تطوير `obsidian-investigation-brain`

## الصورة السريعة

المشروع Python/Markdown/YAML في جوهره. لا يحتاج إلى خادم أو build frontend. توجد ثلاث دوائر في core: المهارة والوثائق، قوالب Obsidian، وسكربتات التدقيق وSelf-Tooling. طبقة `swarm-wrapper/` اختيارية وتعمل محلياً في `dry-run` أو مع OpenMausBot loopback. Benchmark موجود كتوزيع تطوير مستقل.

## إعداد البيئة

يتطلب التطوير Python 3.10 أو أحدث. يفضّل إنشاء بيئة افتراضية:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements-dev.txt
```

## أوامر التحقق

| الأمر | الغرض |
|---|---|
| `pytest -q` | كل اختبارات core، بما فيها `tests/` و`swarm-wrapper/tests/` |
| `python3 -m py_compile scripts/*.py swarm-wrapper/*.py` | فحص syntax |
| `python3 scripts/validate_obsidian_native.py <vault> --strict` | Markdown/YAML/Canvas/Bases |
| `python3 scripts/audit_vault.py <vault> --strict --native` | قواعد التحقيق والذاكرة والصيغ |
| `python3 swarm-wrapper/run.py validate --manifest <manifest>` | Team Manifest |
| `python3 scripts/validate_swarm.py <vault> --team-id <id> --run-id <id>` | artifacts وHuman Gate |
| `git diff --check` | المسافات والتنسيق |

## دورة تغيير قاعدة

ابدأ بتحديد المنطقة التي تنتمي إليها القاعدة. إذا كانت القاعدة تتعلق بالدليل أو الفرضيات، حدّث `SKILL.md` و`references/anti-drift-rules.md` وtaxonomy أو checklist عند الحاجة، ثم أضف حالة اختبار. إذا كانت القاعدة تخص native formats، حدّث `native-format-contract.md` وvalidator. إذا كانت تخص Swarm، لا تسمح بالمخرجات المشتركة قبل Human Gate.

بعد ذلك شغّل الاختبار المستهدف، ثم `pytest -q`، ثم native/audit على fixture، ثم فحص diff. لا تعتبر نجاح أي benchmark نجاحاً لوكيل حر؛ يجب أن يظل `producer` واضحاً في النتائج.

## Benchmark (اختياري)

يعيش Benchmark في مستودع مستقل: [obsidian-investigation-brain-benchmark](https://github.com/bio-colab/obsidian-investigation-brain-benchmark). لا يحتاج core إلى حزم القضايا أو ground truth أو أدوات القياس. راجع README لذلك المستودع عند تطوير المقاييس أو تشغيل baseline/agent، ولا تجعل `ground_truth.yaml` أو `designer_notes.md` متاحين لمسار الوكيل.

## تطوير Swarm Wrapper

ابدأ دائماً بـ `dry-run`. كل Team Manifest يثبت `case_id` و`team_id` وsource root وworker/timeout budgets. لا تستخدم `ask_bot` الداخلي كمنسق؛ الـ wrapper يملك fan-out والـ correlation والمهلة. العميل الحي لا يقبل إلا loopback، ويجب تعطيل computer وComposio للقضايا التدريبية.

لا تضف promotion تلقائياً. أي conflict أو consensus draft يبقى `pending-human-review`. إذا احتجت دعماً لـ fork/merge أو semantic agreement، أضف schema واختبارات وحاجزاً بشرياً قبل تعديل writer.

## CI

تعمل CI الخاصة بـcore على Python 3.10 و3.11 و3.12. لا تحتاج إلى OpenMausBot حي أو secrets أو Docker؛ تستخدم `dry-run` وfake HTTP harness. يملك Benchmark المستقل CI منفصلة لفحوصه، ولا يجعل core نجاحها شرطاً لمسار الاستخدام الأساسي.

## ملاحظات الصيانة

لا تحفظ نتائج تشغيل مولدة داخل core. لا تضف اعتماديات ثقيلة لعملية يمكن تنفيذها بمكتبة Python القياسية. حافظ على مخرجات JSON قابلة للاستهلاك الآلي، وعلى رسائل أخطاء تفيد المطور دون كشف أسرار أو محتوى قضية.
