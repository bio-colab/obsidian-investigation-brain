# Changelog — obsidian-investigation-brain

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
- **إثراء كامل لحزم ORG/SK 021–030** (جداول، حدود، TRAP notes) — انظر `Benchmark v1/docs/PACKET_ENRICHMENT_LOG.md`
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
