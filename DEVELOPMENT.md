# تطوير `obsidian-investigation-brain`

## الصورة السريعة

المشروع Python/Markdown/YAML في جوهره. لا يحتاج إلى خادم أو build frontend. توجد أربع دوائر مترابطة: المهارة والوثائق، قوالب Obsidian، سكربتات التدقيق وSelf-Tooling، وحزام Benchmark v1. طبقة `swarm-wrapper/` اختيارية وتعمل محلياً في `dry-run` أو مع OpenMausBot loopback.

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
| `pytest -q` | كل اختبارات المشروع، بما فيها `tests/` و`swarm-wrapper/tests/` وBenchmark tests |
| `python3 -m py_compile scripts/*.py swarm-wrapper/*.py` | فحص syntax |
| `python3 scripts/validate_obsidian_native.py <vault> --strict` | Markdown/YAML/Canvas/Bases |
| `python3 scripts/audit_vault.py <vault> --strict --native` | قواعد التحقيق والذاكرة والصيغ |
| `python3 swarm-wrapper/run.py validate --manifest <manifest>` | Team Manifest |
| `python3 scripts/validate_swarm.py <vault> --team-id <id> --run-id <id>` | artifacts وHuman Gate |
| `git diff --check` | المسافات والتنسيق |

## دورة تغيير قاعدة

ابدأ بتحديد المنطقة التي تنتمي إليها القاعدة. إذا كانت القاعدة تتعلق بالدليل أو الفرضيات، حدّث `SKILL.md` و`references/anti-drift-rules.md` وtaxonomy أو checklist عند الحاجة، ثم أضف حالة اختبار. إذا كانت القاعدة تخص native formats، حدّث `native-format-contract.md` وvalidator. إذا كانت تخص Swarm، لا تسمح بالمخرجات المشتركة قبل Human Gate.

بعد ذلك شغّل الاختبار المستهدف، ثم `pytest -q`، ثم native/audit على fixture، ثم فحص diff. لا تعتبر نجاح baseline في Benchmark نجاحاً لوكيل حر؛ يجب أن يظل `producer` واضحاً في النتائج.

## تطوير Benchmark

كل case pack يجب أن يمر عبر:

```bash
cd "Benchmark v1"
python tools/validate_case.py --all
python tools/sanitize_packets.py
python tools/build_run_vaults.py --run-id local-baseline
python tools/run_benchmark.py --run-id local-baseline --vaults-root results/runs/local-baseline --producer baseline --strict-native
python tools/aggregate_results.py --run-id local-baseline
```

لا تجعل `ground_truth.yaml` أو `designer_notes.md` متاحين لمسار الوكيل. عند تغيير metric، حدّث `docs/BENCHMARK_SPEC.md` و`docs/BENCHMARK_TRANSPARENCY.md` وrubric/fixtures، واذكر أثر التغيير على المقارنة التاريخية.

## تطوير Swarm Wrapper

ابدأ دائماً بـ `dry-run`. كل Team Manifest يثبت `case_id` و`team_id` وsource root وworker/timeout budgets. لا تستخدم `ask_bot` الداخلي كمنسق؛ الـ wrapper يملك fan-out والـ correlation والمهلة. العميل الحي لا يقبل إلا loopback، ويجب تعطيل computer وComposio للقضايا التدريبية.

لا تضف promotion تلقائياً. أي conflict أو consensus draft يبقى `pending-human-review`. إذا احتجت دعماً لـ fork/merge أو semantic agreement، أضف schema واختبارات وحاجزاً بشرياً قبل تعديل writer.

## CI

تعمل CI على Python 3.10 و3.11 و3.12. لا تحتاج CI إلى OpenMausBot حي أو secrets أو Docker؛ تستخدم `dry-run` وfake HTTP harness. فحوص native وBenchmark baseline اختيارية في job منفصل إذا توفرت الاعتماديات، لكن فشلها يجب أن يكون مرئياً لا مخفياً.

## ملاحظات الصيانة

لا تعدّل `Benchmark v1/results/` أو الملفات المولدة خارج غرض توثيقي واضح. لا تضف اعتماديات ثقيلة لعملية يمكن تنفيذها بمكتبة Python القياسية. حافظ على مخرجات JSON قابلة للاستهلاك الآلي، وعلى رسائل أخطاء تفيد المطور دون كشف أسرار أو محتوى قضية.
