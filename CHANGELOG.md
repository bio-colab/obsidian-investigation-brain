# Changelog — obsidian-investigation-brain

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
