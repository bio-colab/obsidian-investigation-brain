# Native Formats وSelf-Tooling Integration

## الملخص

يضيف الإصدار 0.4.0 طبقة تكاملية فوق Investigation Brain من دون تغيير مبدأ الفصل بين الدليل والفرضية. طبقة Obsidian الأصلية تهتم بصحة Markdown وJSON Canvas وBases وCLI؛ طبقة Investigation Brain تحكم provenance وChain-of-Custody وCounter-Hypothesis وHuman Gate؛ وطبقة Self-Tooling تسمح للوكيل ببناء أدوات صغيرة وقت الحاجة داخل مساحة قضية مقيدة.

> الأداة تنتج مساراً قابلاً لإعادة التشغيل، لا حقيقةً جديدة. المصدر يبقى هو Evidence، والنتيجة الآلية تبقى Analysis أو Exploration إلى أن تُراجع بشرياً.

## معمارية الطبقات

| الطبقة | المكوّنات | مخرجاتها | الحاجز |
|---|---|---|---|
| Obsidian Native Formats | Markdown، frontmatter، wikilinks، Canvas، Bases، CLI اختياري | ملفات قابلة للعرض والتحرير | `validate_obsidian_native.py` |
| Investigation Brain | Evidence، CoC، Hypotheses، Timeline، Ledger، Reports | معرفة منظمة قابلة للتدقيق | `audit_vault.py` + Human Gate |
| ARC-style Self-Tooling | parsers، anomaly detectors، linkers، graph analyzers، simulators | Analysis/Exploration وtool traces | `case_tooling.py` + Tool-Audit |

## دورة تشغيل الأداة

يبدأ الوكيل بسؤال تحليلي محدد ومدخلات معلنة. إذا لم تكفِ الأدوات الموجودة، ينشئ ملفاً داخل `08-Tooling/Active/`، ثم يكتب manifest يحدد runtime وentrypoint وinputs وwrites-to وnetwork. قبل التشغيل، يفحص `case_tooling.py validate` manifest ويمنع أي مسار خارج case-root أو خارج مناطق الكتابة المسموحة.

بعد ذلك تُنفذ الأداة داخل Docker أو Podman أو bubblewrap مع شبكة مغلقة وcase-root للقراءة فقط، ولا تُفتح للكتابة إلا المسارات المعلنة. إذا لم يتوفر backend عازل، يسجل executor حدث `tool.run.skipped` ويخرج بحالة واضحة بدلاً من تنفيذ الكود على المضيف. يمكن استخدام `--allow-host` فقط في تطوير محلي مقصود، وليس في تشغيل قضية أو Benchmark.

يسجل التشغيل command digest وhashes للمدخلات والمخرجات وexit code وملخص stdout/stderr في `case-logs/tool-runs.jsonl`، ويكتب audit JSON في `08-Tooling/Audits/`. إذا كان الناتج تنبؤياً أو سيغيّر قراراً تحليلياً، تنشأ `Simulation-Run` قبل الالتزام. لا تُرقّى الأداة إلى Library ولا تُستخدم في تقرير معتمد دون Human Gate.

## مناطق الكتابة

| المسار | الاستخدام | الحالة المعرفية |
|---|---|---|
| `08-Tooling/Active/` | كود القضية قيد التجربة | draft |
| `08-Tooling/Fixtures/` | fixtures صغيرة وغير حساسة | test input |
| `08-Tooling/Runs/` | stdout المهيكل، نتائج parsing، simulation artifacts | analysis/exploration |
| `05-Analysis/` | تحليل راجع بشرياً ومربوط بالمصدر | analysis |
| `02b-Exploration/` | ملاحظات مؤقتة أو فرضيات استكشافية | exploration |
| `01-Evidence/` | المصدر أو الدليل الأصلي فقط | verified/pending review |

## التشغيل

```bash
# إنشاء بنية القضية
python3 scripts/case_tooling.py init /path/to/case-vault --session-id SESSION-001

# فحص الصيغ الأصلية
python3 scripts/validate_obsidian_native.py /path/to/case-vault --strict

# فحص manifest Markdown أو YAML
python3 scripts/case_tooling.py validate /path/to/case-vault 08-Tooling/Manifests/TOOL-001.md

# تشغيل مع fail-closed تلقائي
python3 scripts/case_tooling.py run /path/to/case-vault \
  --manifest 08-Tooling/Manifests/TOOL-001.md \
  --backend auto --run-id RUN-001

# مراجعة curation دون نقل تلقائي
python3 scripts/tools-review.py /path/to/case-vault

# ترقية أو أرشفة صريحة بعد Human Gate
python3 scripts/tools-review.py /path/to/case-vault --promote 08-Tooling/Active/tool.py
python3 scripts/tools-review.py /path/to/case-vault --archive 08-Tooling/Active/failed-tool.py

# التدقيق المعرفي
python3 scripts/audit_vault.py /path/to/case-vault --strict
```

## حدود قانونية ومنهجية

يجب أن يكون واضحاً في كل تقرير أن الأداة قد تكون مولدة آلياً، وأن version وsource-hash وrun-id وinput/output hashes متاحة للمراجعة. لا يكفي أن تكون النتيجة معقولة أو أن الاختبار مرّ؛ يجب أن يبقى المصدر الأصلي قابلاً للفحص، وأن تُعلن القيود والافتراضات والحالات الفاشلة. لا يجوز حذف أداة أو log مؤثر تلقائياً، لأن أثره قد يكون مطلوباً لإعادة بناء القرار.

## مراجع التصميم

يستند تصميم Native Formats إلى صيغ Obsidian ومهارات `kepano/obsidian-skills` [1] [2] [3] [4]. ويستند تصميم الذاكرة الخارجية والـ actuator والسجلات والعزل إلى مبادئ `jerber/arc-code` [5] [6] [7] [8].

## References

[1]: https://github.com/kepano/obsidian-skills "kepano/obsidian-skills"
[2]: https://github.com/kepano/obsidian-skills/blob/main/skills/obsidian-markdown/SKILL.md "Obsidian Markdown Skill"
[3]: https://github.com/kepano/obsidian-skills/blob/main/skills/json-canvas/SKILL.md "JSON Canvas Skill"
[4]: https://github.com/kepano/obsidian-skills/blob/main/skills/obsidian-bases/SKILL.md "Obsidian Bases Skill"
[5]: https://github.com/jerber/arc-code "jerber/arc-code"
[6]: https://github.com/jerber/arc-code/blob/main/PROMPT.md "arc-code PROMPT"
[7]: https://github.com/jerber/arc-code/blob/main/act.py "arc-code actuator"
[8]: https://github.com/jerber/arc-code/blob/main/rig/README.md "arc-code rig and sandboxing"
