# مسار إنتاج التقارير (Reporting Pipeline)

يُستخدم في **الوضع د — Reporting Mode**.  
**v0.3.0:** Claim Trace Matrix · Readiness-Checklist · حظر Court-File دون جاهزية.

## 1. قبل البدء

1. اقرأ `Investigation-Plan` و `Coverage-Ledger`.
2. عبّئ / حدّث `00-Scaffold/Readiness-Checklist.md` (قالب `assets/templates/Readiness-Checklist.md`).
3. تأكد من مرور Human Gate على الفرضيات والأدلة الجوهرية المستخدمة.
4. شغّل `audit_vault.py` وراجع الثغرات الحرجة (CoC، Counter، claim-trace، informant/wiretap).

## 2. Readiness Gate (بوابة الجاهزية)

قبل كتابة تقرير يُقصد اعتماده **أو أي Court-File**:

| الشرط | مطلوب؟ |
|-------|--------|
| حد أدنى من أدلة `verified` مرتبطة بالمراحل داخل النطاق | نعم |
| الفرضيات الجوهرية لها `supporting-notes` | نعم |
| كل Primary لها Counter (أو تبرير مسجّل) | نعم |
| سلسلة حفظ / source-provenance مكتملة للأدلة المستخدمة | نعم |
| لا فجوات حرجة مفتوحة في Ledger دون إعلان صريح داخل التقرير | نعم |
| **Claim Trace Matrix** في YAML التقرير (`claim-trace`) + جدول في الجسم | نعم (v0.3) |
| `readiness-passed: true` على Readiness-Checklist **و** التقرير المعتمد | نعم قبل Court-File |

إذا فشل شرط: إما أكمل العمل، أو اكتب التقرير كـ **مسودة** (`status: draft` / `pending-human-review`) مع `readiness-passed: false` ووسم الفجوات صراحة.  
**ممنوع:** `type: court-file` مع `readiness-passed: false` أو بلا claim-trace.

## 3. أنواع المخرجات

| المجلد | الاستخدام |
|--------|-----------|
| `06-Outputs/Case-Reports/` | التقرير التحقيقي الداخلي |
| `06-Outputs/Court-File/` | ما يُقدَّم للجهة القضائية (بعد readiness فقط) |
| `06-Outputs/Briefings/` | إحاطات قصيرة للفريق أو القيادة |
| `06-Outputs/Snapshots/` | نسخ مجمدة بتاريخ عند مراحل متقدمة |
| `06-Outputs/Press/` | بيانات عامة (إن وُجدت وصُرّح بها) |
| `06-Outputs/Recommendations/` | توصيات سلامة / تنظيمية |
| `06-Outputs/Cold-Case-Reports/` | تقارير القضايا الباردة أو المفتوحة |

## 4. Claim Trace Matrix (v0.3.0 — إلزامي قبل الاعتماد)

كل تقرير `case-report` / `court-file` / `cold-case-report` يُقصد اعتماده يجب أن يحمل:

```yaml
readiness-passed: false   # true فقط بعد اكتمال Readiness-Checklist
claim-trace:
  - claim-id: RC-001
    claim: "نص الادعاء الجوهري"
    evidence: ["[[EV-001]]"]
    support-level: moderate
```

| قاعدة | تفاصيل |
|-------|--------|
| لا ادعاء بلا دليل | كل صف claim-trace يحتاج evidence غير فارغ |
| الاتساق | نصوص الجدول في الجسم تطابق YAML |
| المسودة | يجوز claim-trace جزئي مع status: draft |
| المحكمة | Court-File بلا claim-trace → انتهاك حرج في audit |

القوالب: `assets/templates/Case-Report.md` · `Court-File.md` · `Readiness-Checklist.md`.

## 5. خطوات النثر

1. حدّد الجمهور (فريق / مدعي عام / محكمة / داخلي فقط).
2. اتبع ترتيب مراحل الخطة قدر الإمكان (Plan-Driven).
3. ابنِ **Claim Trace Matrix** قبل السرد الطويل.
4. اربط كل ادعاء جوهري بفرضية أو دليل عبر روابط + claim-trace.
5. أعلن الفجوات المتبقية بصراحة (لا تخفِها).
6. بعد المسودة: حدّث Coverage-Ledger + Review-Queue + Readiness-Checklist.
7. بعد الاعتماد: `readiness-passed: true` + Snapshot بتاريخ إن لزم.

## 6. ما لا يُفعل

- لا تلخّص أقساماً أو مراحل لم تُغطَّ بأدلة دون وسم.
- لا تقدّم فرضية Primary كحقيقة قاطعة دون ذكر Counter أو حدود الدعم.
- لا تُدرج أدلة بلا سلسلة حفظ (أو source-provenance للأرشيف) في ملف محكمة.
- لا تُصدر Court-File دون Readiness-Checklist ناجح و claim-trace.

## 7. بنية Probable Cause (v0.2.0 — قضايا تقنية / NTSB-style)

للتحقيقات في حوادث النقل والطيران والسلامة الصناعية يُفضَّل هذا الترتيب داخل Case-Report أو Court-File:

1. **Findings** — النتائج المؤكدة المدعومة بأدلة
2. **Probable Cause** — السبب المحتمل الرئيسي
3. **Contributing Factors** — العوامل المساهمة (بما فيها System-Failure / Regulatory-Gap / Safety-Culture)
4. **Safety Recommendations** — تُحفظ أيضاً كملاحظات منفصلة تحت `06-Outputs/Recommendations/`

لا تختلق Findings. إن بقي السبب مجهولاً استخدم `status: cause-unknown` وأعلن الفجوة.

## 8. تقارير Cold Case / Open Investigation (v0.2.0+)

عند `case-status: cold-case` أو `open-investigation`:
- استخدم قالب `Cold-Case-Report.md`
- أقسام إلزامية: ما نعرفه · ما لا نعرفه · الخيوط الحية · الفرضيات المتبقية · توصيات المرحلة التالية
- claim-trace للادعاءات الجوهرية حتى في التقارير المفتوحة
- راجع دورياً (quarterly) وسجّل في Changelog

## 9. المخرجات والهيكل

| المجلد | الاستخدام |
|--------|-----------|
| `00-Scaffold/Readiness-Checklist.md` | بوابة الجاهزية القابلة للتدقيق (v0.3) |
| `06-Outputs/Recommendations/` | توصيات سلامة / تنظيمية |
| `06-Outputs/Cold-Case-Reports/` | تقارير القضايا الباردة أو المفتوحة |
| `07-Cold-Case/` | خيوط حية + "ما نعرفه" أثناء المتابعة |
