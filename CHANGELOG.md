# Changelog — obsidian-investigation-brain

## Unreleased — 2026-08-23

### أضيف — Gap Intelligence تنفيذي في audit_vault (v0.4.3 rules)

- **Coverage Intelligence:** يقارن `audit_vault.py` مراحل Investigation-Plan المرقمة بصفوف Coverage-Ledger ويصدر `COVERAGE_LEDGER_EMPTY` / `COVERAGE_LEDGER_LOW` / `COVERAGE_LEDGER_PARTIAL` مع `coverage_intelligence` في JSON (% مراحل الخطة التي لها صف).
- **HYPOTHESIS_STRONG_ON_CONTRADICTION / HYPOTHESIS_ON_CONTRADICTION:** فرضية strong/conclusive تعتمد على دليل داخل تناقض مفتوح تُرفع major، وغيرها minor.
- **CONTRADICTION_UNLINKED:** تناقض بلا `between` مرتبط يُعلن minor بدل أن يمر صامتاً.
- **CONCLUSIVE_NEEDS_MULTIPLE_SUPPORT:** support-level conclusive يتطلب ≥2 supporting-notes وفق تعريف SKILL («أدلة قاطعة متعددة ومستقلة»).

### دُقق على قضية ثانية — عقد `undermines` للتناقضات

- اختبار القواعد أعلاه على حالة قاتل متسلسل حقيقية (هواسونغ) كشف إنذاراً كاذباً دلالياً: فرضية تستند إلى الطرف «الكاسح» داخل تناقض كانت تُلوّث لأن `between` يضم طرفي الصراع معاً.
- العقد الجديد: حقل `undermines` في frontmatter التناقض يسمّي الأطراف التي يضعفها فعلاً، وعند وجوده يسبق `between` في حساب الاستهداف؛ الفرضيات المرفوضة/المهجورة تُستثنى من القاعدة أصلاً لأن استشهادها بأدلة منهارة مشروع توثيقياً.
- تغطيتان جديدتان للاختبار: أسبقية `undermines` (تنقلب النتيجة عند قلب الطرف المستهدف)، واستثناء hypotheses المرفوضة.

### أصلح — تحصينات عامة (post-audit hardening)

- UTF-8 إجباري لمخرجات كل CLIs — إنهاء انهيارات cp1252 على ويندوز مع المحتوى العربي.
- حجب redirects خارج loopback في OpenMausBot client (ثغرة SSRF pivot).
- normpath على `writes-to` في التدقيق — مسارات مثل `08-Tooling/../../99-Attachments` تصبح critical.
- host mode يستخدم مسارات المضيف الحقيقية؛ قراءة manifest مرة واحدة (TOCTOU)؛ hashes قبل/بعد لكل write target.
- ترتيب Tool-Audits بالطابع الزمني في tools-review؛ تهريب pipes/newlines في decisions وسجلات Swarm؛ fences ديناميكية ضد كسر code blocks.
- validate_swarm يقبل CRLF frontmatter؛ تعقيم proposal_id/claim_id الواردة من الوكلاء.
- اختبارات انحدار جديدة لكل ما سبق (41 اختباراً) وحارس skip لاختبار symlink عند غياب الصلاحية.

### P3 — استخراج Benchmark إلى مستودع مستقل

- نُقل Benchmark v1 إلى [مستودع مستقل](https://github.com/bio-colab/obsidian-investigation-brain-benchmark) خاص وقابل لإعادة التشغيل، مع أدواته وحزمه واختباراته وCI منفصلة.
- أزيلت حزم القضايا ونتائج التشغيل من core؛ بقيت وثيقة الشفافية وروابط المواصفات، وبقيت اختبارات native/tooling ضمن core.
- لا يستدعي CI الأساسي Benchmark؛ التوزيع المستقل يفحص بيئته وcase packs وRuff وpytest وPython compilation بصورة مستقلة.

## 0.4.2 — 2026-08-13

### أضيف — Bounded Investigation Swarm MVP

- `swarm-wrapper/models.py` يعرّف Team Manifest وAgent Spec وProposal وClaim وConflict وHuman Gate.
- `swarm-wrapper/orchestrator.py` ينفذ fan-out محدوداً في `dry-run` أو عبر OpenMausBot loopback، مع source snapshot hash وtimeouts وfailures واضحة.
- `swarm-wrapper/vault.py` يكتب proposals وconflicts وconsensus drafts وHuman Gates حصراً في `08-Tooling/Swarm/`، ولا يملك promotion API.
- `scripts/validate_swarm.py` يدقق حدود المخرجات وrun identity وJSONL وHuman Gate دون لمس Evidence.
- أضيف مثال manifest وقضية تدريبية واختبارات تغطي fan-out وconflicts وmissing bot ids ومحاولات الهروب من case-root.
- أضيفت وثيقة `docs/INVESTIGATION_SWARM_MVP.md` وربطت الطبقة في README وSKILL وقائمة الإصدار.

> اتفاق الوكلاء لا يصنع دليلاً مستقلاً. كل المخرجات Proposal/Analysis حتى يقرر المحقق البشري خلاف ذلك ضمن بروتوكول منفصل.

---

## 0.4.1 — 2026-08-13

### أضيف — Dynamic Tool Factory + External Decision Memory

- `scripts/tool_factory.py` ينشئ scaffold صغيراً لكل سؤال تحليلي مع manifest وaudit، دون تنفيذ أو استدعاء نموذج، لتطبيق build-small/discard-early.
- `scripts/case_memory.py` يضيف أحداثاً مهيكلة إلى `case-logs/session.jsonl` ويولد `memory-snapshot.md` للاستئناف دون حفظ سلسلة التفكير السرية أو كل أوامر shell.
- `case_tooling.py` يربط تشغيل الأدوات بسجل الجلسة، ويدعم snapshot أولياً عند init.
- `audit_vault.py` يفحص JSONL وصحة snapshot عند تفعيل tooling، ويبلغ events وinvalid lines وsnapshot presence دون كسر vaults القديمة التي لا تستخدم الطبقة.
- baseline builder وAgent Run Protocol وREADME وSKILL وقائمة الجودة محدثة لتطبيق المسار الجديد.
- أضيفت اختبارات factory وdecision memory، وارتفعت حزمة regression إلى 10 اختبارات.

> الذاكرة الجديدة تسجل قرارات وملاحظات قابلة للمراجعة، لا chain-of-thought خاماً. والأداة المؤقتة تبقى Analysis/Exploration حتى Human Gate.

---

## 0.4.0 — 2026-08-13

### أضيف — Surgical Integration

**Native Formats**
- `references/native-format-contract.md` يربط Obsidian Markdown وJSON Canvas وBases وCLI بعقد التحقيق.
- `scripts/validate_obsidian_native.py` يفحص frontmatter وwikilinks وCanvas JSON وBases YAML.
- baseline vaults تنشئ Investigation Index بصيغة `.base` وCanvas بروتوكولياً صالحاً.

**Self-Tooling**
- مساحة `08-Tooling/` و`case-logs/` للأدوات المؤقتة، manifests، audits، fixtures، runs، والجلسات.
- `scripts/case_tooling.py` لإنشاء workspace والتحقق من manifests وتشغيل الأدوات داخل Docker/Podman/bwrap عند توفره.
- التنفيذ fail-closed عند غياب backend عازل؛ `--allow-host` مطلوب صراحةً للتطوير المحلي.
- hashes وcommand digest وexit code وstdout/stderr مختصر تُسجل في `case-logs/tool-runs.jsonl` و`08-Tooling/Audits/`.
- `scripts/tools-review.py` للـ curation دون حذف أو promotion تلقائي.

**Audit / Benchmark / Docs**
- `audit_vault.py` يعرف 07-Cold-Case و08-Tooling، ويفحص manifest write boundaries ووجود Tool-Audit.
- Benchmark config/parser ومجرى agent protocol محدثة إلى skill target 0.4.0.
- أضيفت قوالب Tool-Manifest وTool-Audit وCase-Log وSimulation-Run.
- أضيفت اختبارات native validator وmanifest safety وfail-closed executor.

> لا تمنح الطبقة الجديدة أي أداة حق الكتابة إلى Evidence أو تغيير status تلقائياً؛ تبقى Human Gate وChain-of-Custody وClaim Trace هي الحواجز الحاكمة.

---

## 0.3.1 — 2026-08-08

### أضيف (P1 من خطة الإصلاح / البنchmark + شفافية الإصدار)

**Skill**
- قوالب **Series-Linkage** و **Enterprise-Map**
- **Coverage-Ledger** مع `gaps:` منظمة (id / description / phase_id / status)
- تحديث taxonomy · folder-structure · guide-for-investigator · anti-drift · yaml-standards · SKILL 0.3.1
- `audit_vault.py`: تنبيه minor عند غياب `gaps:` المنظمة (`LEDGER_GAPS_UNSTRUCTURED`)

**Benchmark**
- `docs/AGENT_RUN_PROTOCOL.md` — بروتوكول وكيل حر
- `tools/prepare_agent_run.py` — تجهيز agent_input بلا GT
- `score_vault` / `run_benchmark`: hard_fail حسب `producer` (agent on / baseline off)
- **إثراء كامل لحزم ORG/SK 021–030** (جداول، حدود، TRAP notes) — انظر [`PACKET_ENRICHMENT_LOG.md`](https://github.com/bio-colab/obsidian-investigation-brain-benchmark/blob/main/docs/PACKET_ENRICHMENT_LOG.md)
- **شفافية الإصدار:** `docs/BENCHMARK_TRANSPARENCY.md` — ماذا قيس، حدود baseline vs agent، وأثر البنchmark على 0.2→0.3.1

---

## 0.3.0 — 2026-08-08

### أضيف / أصلح (من Investigation Benchmark v1 + خطة الإصلاح)

**Critical**
- **Claim Trace Matrix** إلزامي للتقارير المعتمدة و Court-File (`claim-trace` في YAML + جدول)
- قالب **Readiness-Checklist** + حقل `readiness-passed` على التقارير
- قالب **Case-Report** و **Court-File** محدّثان للجاهزية
- **حظر Court-File** دون readiness (audit: `COURT_WITHOUT_READINESS`, `COURT_NO_CLAIM_TRACE`)
- `audit_vault.py` v0.3:
  - `INFORMANT_VERIFIED_NO_CRED`
  - `WIRETAP_NO_AUTH`
  - `GROUP_VICTIM_NAME_WITH_EMPTY_GROUP`
  - `PRIMARY_COUNTER_THIN`
  - `REPORT_NO_CLAIM_TRACE` / `CLAIM_TRACE_NO_EVIDENCE`
  - إضافة `informant-testimony` إلى EVIDENCE_TYPES

**Major**
- تحديث reporting-pipeline · anti-drift · vault-quality-checklist · taxonomy · yaml-standards · folder-structure · SKILL.md
- بنchmark: `sanitize_packets.py` (إزالة تسرّب Truth band من BRIEF) · وسم `producer` في score/run/aggregate

**مبدأ**
كل إصلاح يجيب: هل يزيد قدرة المحقق على الدفاع عن سلامة الأدلة ومسار الاستدلال أمام جهة إشراف أو محكمة؟

---

## 0.2.0 — 2026-08-08

### أضيف / أصلح (من بنشماركين مستقلين على 20 قضية مشهورة)

**Critical**
- **source-provenance** كبديل منطقي لـ Chain-of-Custody للمصادر الأرشيفية/العامة (NARA, FBI Vault, NTSB…)
- تحديث `audit_vault.py` لتجنب false-positive على المصادر الأرشيفية
- أنواع `data-analysis` / محاكاة تقنية + مجلد `Data-Analysis/` و`Technical-Analysis/`
- كيانات `System-Failures` و`Regulatory-Gaps`
- سير عمل **Cold Case / Open Investigation** (`case-status`, مجلد `07-Cold-Case/`, قالب Cold-Case-Report)

**Major**
- طبقة **L-Archival** و**L-Technical** في Evidence Spectrum
- توسيع **Vehicle** لدعم Vessel (IMO, flag-state) وAircraft (N-number, type-certificate)
- قالب **Group-Entity** للضحايا/الركاب المتعددين
- قوالب **Financial-Record**, **Wiretap-Evidence**, **Informant-Testimony**
- بنية **Probable Cause + Contributing Factors + Safety Recommendations** في Reporting Pipeline
- مجلد `06-Outputs/Recommendations/`
- حقول `era` / `period` / `severity` في Timeline
- `source-credibility` و`credibility-assessment` للمخبرين والشهادات
- `status: cause-unknown` + بروتوكول الفجوة المفتوحة
- أدوار Person إضافية: crew, passenger, missing-person, informant + legal-status

**ملفات معدّلة**
- SKILL.md, folder-structure, note-types-taxonomy, yaml-frontmatter-standards
- anti-drift-rules, reporting-pipeline, audit_vault.py
- قوالب جديدة: Source-Provenance, Group-Entity, Financial-Record, Wiretap-Evidence, Informant-Testimony, Data-Analysis, Cold-Case-Report
- Vehicle.md موسّع

### مبدأ
كل إصلاح يجيب: هل يزيد قدرة المحقق على الدفاع عن سلامة الأدلة ومسار الاستدلال أمام جهة إشراف أو محكمة؟

---

## 0.1.2 — 2026-08-08

### أصلح / حسّن (عامة — من تجربة Osage)
- قالب **Organization.md** مع `org-kind` وأدوار الجهة
- حقل **relationships** في قالب Person + دور `investigator`
- دليل المحقق: قسم العلاقات والمنظمات + عدم اختلاق أسماء عند النطاق الأوسع
- taxonomy و yaml-standards محدّثان
- إرشاد ربط Link-Analysis canvas بالكيانات في Visual-README

## 0.1.1 — 2026-08-08

### أصلح / حسّن (عامة — مستفادة من تجربة vault تدريبي)
- **S1:** إضافة منطقة `90-Reference-Sources` إلى `ZONES` في `audit_vault.py`
- **S2:** توحيد frontmatter للقوالب البصرية (`visual-doc`)
- **S3:** حقل `support-history` + `superseded-by` في قالب Hypothesis
- **S4:** قالب `Analysis.md` جديد + ربط أوضح في `Timeline-Event`
- **S5:** فقرة في دليل المحقق: مصادر أرشيفية عامة مقابل أدلة تشغيلية
- **S6:** إصلاح مسارات روابط Canvas في قالب Dashboard
- تحديث taxonomy و yaml-standards و folder-structure

## 0.1.0 — 2026-08-08

### أضيف
- SKILL.md كاملاً + شجرة المجلدات + قوالب + Canvas + audit_vault.py + Reporting
- مبني على obsidian-research-brain v1.1.9
