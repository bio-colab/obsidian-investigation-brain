# شفافية البنchmark وأثره على المهارة

**المستند:** جزء من إصدارة `obsidian-investigation-brain` **v0.4.2**
**الغرض:** الإفصاح الصريح عما قيس، وكيف قيس، وما الذي تغيّر في المهارة بسببه — حتى لا تُقرأ درجات عالية كدليل زائف على اكتمال الوكيل الحر.

---

## 1) ماذا يوجد في هذا المستودع؟

| المكوّن | الموقع | الدور |
|---------|--------|--------|
| المهارة (Skill) | `SKILL.md` + `references/` + `assets/templates/` + `scripts/audit_vault.py` | بروتوكول بناء/تدقيق vault تحقيقي |
| حزام البنchmark | [المستودع المستقل](https://github.com/bio-colab/obsidian-investigation-brain-benchmark) | حزم قضايا + مقيّم + تشغيلات |
| خطة الإصلاح | [`REFORM_PLAN_FROM_BENCHMARK.md`](https://github.com/bio-colab/obsidian-investigation-brain-benchmark/blob/main/docs/REFORM_PLAN_FROM_BENCHMARK.md) | تحويل نتائج القياس إلى backlog |
| بروتوكول الوكيل | [`AGENT_RUN_PROTOCOL.md`](https://github.com/bio-colab/obsidian-investigation-brain-benchmark/blob/main/docs/AGENT_RUN_PROTOCOL.md) | مسار agent منفصل عن baseline |

---

## 2) نطاق البنchmark v1

### 2.1 الكوربس

- **30** حزمة `CASE-*` صالحة للتحقق (`validate_case.py`).
- منها **10** مركّزة: **5 جريمة منظمة (021–025)** + **5 نمط تسلسلي (026–030)**، مع **إثراء نصوص المصادر** (جداول، حدود، TRAP notes).
- الحزم **تاريخية عامة منزوعة الحساسية** أو **خيالية تدريبية** — ليست ملفات قضايا تشغيلية حقيقية.

### 2.2 المقاييس (12)

Evidence coverage · Source provenance · Hypothesis coverage · Counter quality · Timeline · Contradiction · Missing-evidence · False inference · Confirmation-bias · Report traceability · Readiness-gate · Conclusion calibration  

التعاريف: [`BENCHMARK_SPEC.md`](https://github.com/bio-colab/obsidian-investigation-brain-benchmark/blob/main/docs/BENCHMARK_SPEC.md)، والأوزان والصيغ التنفيذية: [`scoring.yaml`](https://github.com/bio-colab/obsidian-investigation-brain-benchmark/blob/main/rubrics/scoring.yaml).

#### 2.2.1 المنهجية التنفيذية والأوزان

الدرجة الكلية ليست متوسطاً غير موزون؛ هي مجموع موزون لمقاييس M01–M12 بعد حساب كل metric وفق rubric الخاص به. المقاييس الموسومة **inverted** تقيس إخفاقاً أو مخالفة، لذلك تُحوّل إلى مساهمة جودة عكسية قبل الجمع. لا تُفترض مساواة المقاييس ولا تُخلط نتائج `baseline` و`agent`.

| المعرّف | المقياس | الوزن | اتجاه القياس |
|---|---|---:|---|
| M01 | `evidence_coverage` | 0.12 | أعلى أفضل |
| M02 | `source_provenance_completeness` | 0.10 | أعلى أفضل |
| M03 | `hypothesis_coverage` | 0.10 | أعلى أفضل |
| M04 | `counter_hypothesis_quality` | 0.10 | أعلى أفضل |
| M05 | `timeline_reconstruction` | 0.10 | أعلى أفضل |
| M06 | `contradiction_detection` | 0.08 | أعلى أفضل |
| M07 | `missing_evidence_detection` | 0.08 | أعلى أفضل |
| M08 | `false_inference_rate` | 0.08 | **معكوس**: المعدل الأقل أفضل |
| M09 | `confirmation_bias_resistance` | 0.08 | أعلى أفضل |
| M10 | `report_traceability` | 0.06 | أعلى أفضل |
| M11 | `readiness_gate_violations` | 0.05 | **معكوس**: المخالفات الأقل أفضل |
| M12 | `final_conclusion_calibration` | 0.05 | أعلى أفضل |

مجموع الأوزان **1.00**. يحفظ المشغّل درجات metrics الفردية، ودرجة المكوّن الموزونة، والـ producer، وcase/run identifiers حتى يمكن إعادة الحساب ومراجعة سبب التغير. تفاصيل matching وrubrics وground truth لا تُستنتج من هذا الجدول؛ المرجع التنفيذي هو `BENCHMARK_SPEC.md` و`scoring.yaml`.

### 2.3 مسارات الإنتاج (مهم للشفافية)

| Producer | المعنى | ماذا يثبت؟ |
|----------|--------|------------|
| **baseline** | `build_run_vaults.py` يبني vault منضبطاً من الحزمة | أن **البروتوكول قابل للتعبير** هيكلياً (انحدار/regression) |
| **agent** | نموذج/وكيل يقرأ `source_packet` فقط | القدرة الحقيقية على الالتزام بالمهارة |
| **adversarial** | vault متعمد السوء | حساسية المقيّم و`audit_vault` |

**تحذير صريح:** درجات baseline القريبة من **1.0** لا تعني أن أي وكيل حر سينجح بنفس المستوى.  
التقارير التي تخلط الاثنين مضلّلة.

---

## 2.4 Integrity gates وصحة المدخلات

قبل تفسير الدرجة، يجب أن يمر run من حواجز السلامة التي تمنع احتساب artifact غير صالح كنجاح. يشمل ذلك `validate_case.py` للحزم، و`validate_obsidian_native.py` لصحة Markdown/YAML وCanvas وBases، ثم `audit_vault.py` للقواعد المنهجية. عند استخدام Swarm، يضاف `validate_swarm.py` للتحقق من Team/Run artifacts ووجود Human Gate. فشل الحاجز يجعل النتيجة غير صالحة للتفسير كنجاح، حتى لو أنتج evaluator رقماً.

هذه الحواجز **integrity checks وليست metric جديدة**؛ لا تغيّر أوزان M01–M12 ولا تضيف نقاطاً. في الوضع الصارم (`--strict` أو `--native`) تكون أخطاء الصياغة والتحذيرات المحددة سبباً للفشل المبكر، ويجب تسجيل الحالة في مخرجات run بدلاً من إخفائها.

---

## 3) التشغيلات المسجّلة (ملخص)

| Run ID | N | Producer | Mean (تقريبي) | محتوى |
|--------|---|----------|---------------|--------|
| `run-5a` | 5 | baseline | ~0.98 | متنوعة (warehouse, payroll, Hudson, Cooper, labgap) |
| `run-5b` | 5 | baseline | ~1.00 | حافة (informant, zodiac, TWA, Titanic, aviation) |
| `run-org-sk` | 10 | baseline | ~1.00 | ORG 021–025 + SK 026–030 |
| `run-v03-smoke` / `run-v031-p1` | 2–5 | baseline | ~1.00 | تحقق بعد إصلاحات 0.3.x |
| Fixtures good/bad | — | synthetic | good ≫ bad | وحدة المقيّم |

المخرجات التفصيلية تُحفظ محلياً تحت `results/runs/` في مستودع Benchmark المستقل، ولا تُحفظ داخل core. قد تُستثنى بعض مجلدات النتائج من النشر؛ المنهجية تبقى موثّقة هنا.

### 3.1 إشارات كمية مفيدة (حتى مع سقف baseline)

- **M10 report_traceability** كان أضعف محور مبكر (صياغة ادّعاءات التقرير vs GT).
- **M08 false inference** أظهر إيجابيات كاذبة عند عبارات «لا تدّعِ X» → أُصلحت نافذة النفي في المقيّم + صياغة الحزم.
- **audit** على fixture سيئ يلتقط بعد 0.3.0: Court بلا readiness، بلا claim-trace، Primary بلا Counter.

---

## 4) أثر البنchmark على المهارة (سلسلة سببية)

كل صف يجيب: *هل يقوّي الدفاع عن سلامة الأدلة/الاستدلال أمام إشراف أو محكمة؟*

| إصدار | ما دفعه البنchmark / الضغط | ماذا أُضيف أو أُصلح في المهارة |
|--------|---------------------------|--------------------------------|
| **0.2.0** | بنشماركات سابقة (~20 قضية مشهورة) + أرشيف/NTSB/cold | source-provenance، cold-case، group-entity، L-Archival/Technical، informant/wiretap/financial، probable cause |
| **0.3.0** | Benchmark v1: M10، Court readiness، informant traps، group invent-names، تسرّب truth band | **Claim Trace Matrix**، **Readiness-Checklist**، قوالب Case-Report/Court-File، قواعد audit الحرجة، تنظيف BRIEF |
| **0.3.1** | ضغط ORG/SK + حاجة مسار agent شفاف | **Series-Linkage**، **Enterprise-Map**، `gaps:` منظمة في Ledger، بروتوكول agent + hard_fail حسب producer، إثراء حزم 021–030 |

### 4.1 أكواد audit الجديدة ذات الصلة (v0.3+)

- `INFORMANT_VERIFIED_NO_CRED`
- `WIRETAP_NO_AUTH`
- `GROUP_VICTIM_NAME_WITH_EMPTY_GROUP`
- `COURT_WITHOUT_READINESS` / `COURT_NO_CLAIM_TRACE`
- `REPORT_NO_CLAIM_TRACE` / `CLAIM_TRACE_NO_EVIDENCE`
- `PRIMARY_COUNTER_THIN`
- `LEDGER_GAPS_UNSTRUCTURED` (minor)

### 4.2 قوالب مدفوعة بالضغط

- `Readiness-Checklist.md` · `Case-Report.md` · `Court-File.md`
- `Series-Linkage.md` · `Enterprise-Map.md`
- Coverage-Ledger بـ YAML `gaps:[]`

---

## 5) حدود معروفة (لا نخفيها)

1. **سقف baseline:** المنتج المنضبط يعرف كيف يمرّ على المقيّس؛ ليس اختبار تعميم للنماذج.  
2. **إثراء الحزم:** 021–030 مُثرَاة بنصوص تدريبية أعمق؛ بقية 001–020 ما زالت أخف في بعض الملفات.  
3. **تشغيل agent الحر داخل هذا الإصدار:** البروتوكول والأدوات جاهزة؛ **جدول درجات agent عام ليس جزءاً إلزامياً من هذا الإصدار** حتى يُنفَّذ ويُنشر بشفافية لاحقة.  
4. **المقيّس تقريبي:** تشابه نصي + YAML؛ ليس حكماً قضائياً بشرياً.  
5. **لا ادعاء امتثال قانوني:** المهارة أداة تنظيم vault، لا بديل عن الإجراءات الرسمية.

---

## 6) كيف تعيد إنتاج القياس؟

```powershell
git clone https://github.com/bio-colab/obsidian-investigation-brain-benchmark.git benchmark
cd benchmark
python3 -m pip install -r requirements-dev.txt
python tools/check_environment.py
python tools/validate_case.py --all
python tools/sanitize_packets.py          # لا تسرّب Truth band
python tools/build_run_vaults.py --preset org-sk --run-id repro-baseline
python tools/run_benchmark.py --run-id repro-baseline --vaults-root results/runs/repro-baseline --producer baseline --only CASE-ORG-RICO-SHELL-023 CASE-SK-FICT-CORRIDOR-030
python tools/aggregate_results.py --run-id repro-baseline

# مسار وكيل (بعد أن يبني vault)
python tools/prepare_agent_run.py --run-id agent-01 --cases CASE-ORG-RICO-SHELL-023
# ... agent writes results/runs/agent-01/CASE-.../vault ...
python tools/run_benchmark.py --run-id agent-01 --vaults-root results/runs/agent-01 --producer agent --only CASE-ORG-RICO-SHELL-023
```

Skill audit من checkout core:

```powershell
cd ../obsidian-investigation-brain
python3 scripts/audit_vault.py path/to/vault --strict
```

---

## 7) سياسة النشر والخصوصية

- لا ترفع vaults قضايا حقيقية حسّاسة.
- حزم `cases/` في مستودع Benchmark المستقل مصممة للتدريب العام/الخيالي.
- `designer_notes.md` و `ground_truth.yaml` **ليست** لمدخلات الوكيل؛ للتصميم والتحكيم فقط.

---

## 8) سجل وثائق مرتبطة

| وثيقة | محتوى |
|-------|--------|
| `CHANGELOG.md` | 0.2.0 → 0.3.0 → 0.3.1 → 0.4.0 → 0.4.1 → 0.4.2 |
| [`BENCHMARK_SPEC.md`](https://github.com/bio-colab/obsidian-investigation-brain-benchmark/blob/main/docs/BENCHMARK_SPEC.md) | تعريف المقاييس |
| [`REFORM_PLAN_FROM_BENCHMARK.md`](https://github.com/bio-colab/obsidian-investigation-brain-benchmark/blob/main/docs/REFORM_PLAN_FROM_BENCHMARK.md) | خطة P0/P1 وحالة التنفيذ |
| [`AGENT_RUN_PROTOCOL.md`](https://github.com/bio-colab/obsidian-investigation-brain-benchmark/blob/main/docs/AGENT_RUN_PROTOCOL.md) | بروتوكول agent |
| `docs/REFORM_PLAN_v0.3.md` | مؤشر مختصر |
| `ARCHITECTURE.md` | خريطة الطبقات والتكاملات |
| `OBSIDIAN_NATIVE_STRATEGY.md` | استراتيجية Dataview/Bases وnative validation |

---

## 9) خلاصة جملة واحدة

> هذا الإصدار يوثّق أن **المهارة تطورت تحت ضغط بنشمارك منظم** (هيكل، provenance، claim-trace، readiness، ORG/serial)، وأن **الدرجات العالية المنشورة هنا — إن وُجدت — يجب أن تُوسم بـ producer=baseline أو agent**؛ والخلط بينهما يُعتبر خطأ منهجي في قراءة الجودة.
