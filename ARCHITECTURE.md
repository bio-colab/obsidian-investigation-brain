# 🏗️ Investigation Brain Architecture

## الغرض

هذا المستند هو **خريطة المعمارية الموحدة** للمشروع. يشرح كيف ترتبط المهارة، الـ vault، التدقيق، الأدوات، والـ Swarm، لكنه لا يستبدل العقد التفصيلية في `SKILL.md` أو `references/`. عند التعارض، تكون القاعدة الأشد صرامة في `SKILL.md` و`anti-drift-rules.md` هي الحاكمة.

## الصورة العامة

```text
طلب المستخدم / خطة القضية
          │
          ▼
┌──────────────────────────────────────────┐
│ 00-Scaffold — النطاق والخطة والبوابات     │
└────────────────────┬─────────────────────┘
                     │ source-bounded work
                     ▼
┌──────────────────────────────────────────┐
│ 01-Evidence — المصدر الموثق وCoC          │
└────────────────────┬─────────────────────┘
                     │ claims, entities, events
                     ▼
┌──────────────────────────────────────────┐
│ 03-Hypotheses + 05-Analysis — الاستدلال   │
└────────────────────┬─────────────────────┘
                     │ drafts and tools only
                     ▼
┌──────────────────────────────────────────┐
│ 08-Tooling + case-logs — التشغيل والتدقيق  │
└────────────────────┬─────────────────────┘
                     │ human review / readiness
                     ▼
┌──────────────────────────────────────────┐
│ 06-Outputs — التقارير والمخرجات المعتمدة   │
└──────────────────────────────────────────┘
```

## الطبقات الأربع العملية

### 1. Scaffold Layer — `00-Scaffold/`

يحتوي على Case Scope وInvestigation Plan وTeam Roles وCoverage Ledger وReview Queue وReadiness Checklist وAGENTS. هذه الطبقة لا تمنح أي ادعاء صفة Evidence؛ وظيفتها تثبيت السؤال والنطاق والبوابات ومسؤوليات الفريق.

### 2. Evidence Layer — `01-Evidence/`

هذه هي منطقة الحقيقة المصدرية داخل القضية. كل دليل تشغيلي يحتاج Chain of Custody، وكل مصدر أرشيفي/عام يحتاج `source-provenance`. لا يدخل إليها نص مولد من وكيل أو نتيجة أداة تلقائياً، حتى لو اتفق عدة وكلاء عليها.

### 3. Analysis Layer — `03-Hypotheses/` و`05-Analysis/`

تحتوي الفرضيات الأساسية والبديلة والمضادة والمرفوضة، والتحليل الزمني والسلوكي والتقني وسلاسل الارتباط وخرائط المؤسسات. كل فرضية Primary تحتاج Counter-Hypothesis ومراجع دعم؛ كل تحليل آلي يبقى draft أو exploration أو pending-human-review.

### 4. Tooling Layer — `08-Tooling/` و`case-logs/`

تضم الأدوات المؤقتة وmanifests وaudits وfixtures وruns، بالإضافة إلى decision memory وruntime events وSwarm proposals. هذه الطبقة قابلة لإعادة التدقيق لكنها ليست Evidence. التنفيذ الذاتي fail-closed عند غياب sandbox، وSwarm Wrapper لا يملك promotion API.

## المبادئ الحاكمة

| المبدأ | المعنى التشغيلي |
|---|---|
| Evidence ≠ hypothesis | لا يُنقل التخمين إلى Evidence لتجميل النتيجة. |
| Provenance before promotion | لا ترقية دون مصدر وCoC أو source-provenance وHuman Gate. |
| Counter-Hypothesis | لا Primary بلا بديل مضاد substantive. |
| Timeline-first | الادعاءات الزمنية ترتبط بأحداث ومصادر، لا بسرد حر فقط. |
| Human Gate | القرار البشري ظاهر وقابل للتدقيق، لا موافقة ضمنية. |
| Native format ≠ epistemic validity | صحة Markdown/Canvas/Bases لا تثبت صحة المحتوى. |
| Tool output ≠ evidence | نتيجة الأداة Analysis حتى تمر بالمراجعة. |
| Baseline ≠ agent | نجاح مولد baseline يثبت قابلية التعبير عن البروتوكول، لا قدرة وكيل حر. |
| Local and bounded | القضايا الحساسة محلية، وpaths وnetwork وwrites محدودة. |

## القواعد الصارمة

القواعد التفصيلية في [`references/anti-drift-rules.md`](references/anti-drift-rules.md)، وخلاصتها أن المشروع يمنع اختلاق الأدلة والكيانات، يمنع Court-File دون readiness وclaim-trace، يطلب CoC/provenance، ويُلزم بتسجيل الفجوات والتناقضات وCounter-Hypotheses. لا يحق للوكيل أو الأداة تغيير `status` أو الكتابة إلى Evidence تلقائياً.

## مسار البيانات

1. يبدأ العمل من نطاق وخطة ومصادر مسموحة في `00-Scaffold`.
2. تُحفظ المصادر والدلائل في `01-Evidence` بعد التوثيق فقط.
3. تُشتق منها الكيانات والأحداث والفرضيات والتحليلات في المناطق المخصصة.
4. تنفذ الأدوات المؤقتة داخل `08-Tooling`، وتسجل الهاشات والأحداث في `case-logs`.
5. يكتب Swarm Wrapper proposals وconflicts وconsensus drafts داخل namespace مستقل.
6. يراجع الإنسان النتائج، ثم تُحدّث Readiness وClaim Trace قبل `06-Outputs`.
7. يشغّل `validate_obsidian_native.py` للصياغة، ثم `audit_vault.py` للسلامة المنهجية، ثم `validate_swarm.py` عند وجود Swarm run.

## التكاملات المتاحة

| التكامل | دوره | حدوده |
|---|---|---|
| [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills) | إرشادات Obsidian Markdown وCanvas وBases وCLI | لا يقرر صحة الدليل أو منهجية التحقيق؛ يعمل بالتوازي مع هذه المهارة. |
| ARC-style self-tooling | Tool Factory وsandbox وaudit وdecision memory مستلهمة من نمط الأدوات المؤقتة | لا يمنح الكود المولد صلاحية Evidence أو network تلقائياً. |
| [OpenMausBot](https://github.com/milind-soni/OpenMausBot) | orchestrator محلي اختياري، roster وdrivers وSSE وbot threads | تواصل bot-to-bot الحالي ليس بروتوكول consensus؛ Swarm Wrapper يفرض schemas وbudgets وHuman Gate. |
| Benchmark v1 | قياس regression للـ vault والمقاييس الاثني عشر | لا يمثل حكماً بشرياً أو امتثالاً قانونياً، ولا يخلط baseline بالوكيل الحر. |

## أدوات الدخول السريعة

```bash
# صياغة Obsidian
python3 scripts/validate_obsidian_native.py /path/to/vault --strict

# تدقيق منهجي
python3 scripts/audit_vault.py /path/to/vault --strict --native

# أداة تحليل مؤقتة
python3 scripts/tool_factory.py create /path/to/vault --tool-id TOOL-001 --kind analyzer --question "..."

# Swarm تدريبي
python3 swarm-wrapper/run.py run \
  --manifest swarm-wrapper/examples/team-manifest.yaml \
  --vault-root /path/to/training-vault \
  --run-id RUN-001
python3 scripts/validate_swarm.py /path/to/training-vault \
  --team-id TEAM-DEMO-001 --run-id RUN-001
```

## أين تبدأ؟

| إذا كنت... | ابدأ من... |
|---|---|
| محققاً أو مستخدماً جديداً | `README.md` ثم `references/guide-for-investigator.md` |
| تبني vault قضية | `SKILL.md` ثم `references/folder-structure.md` |
| تدقق الجودة | `references/vault-quality-checklist.md` ثم `scripts/audit_vault.py` |
| تضيف قالباً أو صيغة | `references/native-format-contract.md` و`OBSIDIAN_NATIVE_STRATEGY.md` |
| تضيف أداة مؤقتة | `references/self-tooling-protocol.md` ثم `scripts/tool_factory.py` |
| تختبر Swarm | `docs/INVESTIGATION_SWARM_MVP.md` ثم `swarm-wrapper/README.md` |
| تطور المشروع | `DEVELOPMENT.md` و`CONTRIBUTING.md` |
| تفسر Benchmark | `docs/BENCHMARK_TRANSPARENCY.md` و`Benchmark v1/docs/BENCHMARK_SPEC.md` |

## حدود مهمة

هذا المشروع أداة تنظيم واستدلال قابلة للتدقيق، وليس بديلاً عن محقق أو خبير قانوني أو إجراء قضائي. لا تُستخدم fixtures العامة لتدريب قضية حقيقية دون فصل واضح، ولا تُرفع بيانات حساسة إلى مستودع عام أو تكامل خارجي.
