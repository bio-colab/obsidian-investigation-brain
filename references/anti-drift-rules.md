# قواعد منع الانحراف (Anti-Drift) — الدماغ التحقيقي

هذه القواعد تحمي الـ vault من التوهان واختلاط الأدلة بالتخمين وتراكم الفوضى.

## 1. الفصل المناطقي غير قابل للتفاوض

| المنطقة | يُسمح | يُمنع |
|---------|-------|-------|
| `01-Evidence` | أدلة مثبتة + سجلات CoC | أي تخمين أو فرضية أو exploration |
| `03-Hypotheses` | فرضيات مع support-level | أدلة خام |
| `02b-Exploration` | أفكار حرة مؤقتة فقط | معاملة كـ verified |
| `06-Outputs` | تقارير ومسودات | أدلة أصلية |

أي نقل بين المناطق يحتاج سبباً مكتوباً في Changelog أو Promotion-Log.

## 2. لا اختلاق

- لا تُنشئ أسماء شهود أو أدلة أو نتائج فحوصات من العدم.
- أي معلومة بلا مصدر موثق → Hypotheses أو Exploration أو تُرفض.
- الوكيل والبشر ملزمون بنفس القاعدة.

## 3. سلسلة الحفظ والفرضيات المضادة

- كل دليل جديد → سجل Chain-of-Custody فوراً.
- كل Primary → Counter مرتبط (أو تبرير مسجّل لغيابه).
- الرفض يحتاج سبب + تاريخ.

## 4. الأسماء الصريحة والروابط الحية

- استخدم أسماء ملفات واضحة (`EV-001-knife.md` أفضل من `note1.md`).
- حافظ على الروابط `[[...]]` بين الأدلة والكيانات والفرضيات والأحداث.
- لا تحذف ملاحظات مرفوضة — غيّر `status` إلى `rejected` أو `deprecated`.

## 5. Scope و Changelog

- أي توسيع أو تضييق للنطاق يُسجَّل في Case-Scope + Changelog مع السبب.
- قرارات رفض الفرضيات والترقيات من Exploration تُسجَّل.

## 6. Human Gate

- لا تتجاوز `pending-human-review` للمحتوى الحرج.
- التقارير النهائية وملفات المحكمة تحتاج مراجعة بشرية صريحة.

## 7. العرض ≠ الحقيقة

- Canvas و Dashboard و Graph أدوات عمل.
- الاعتماد النهائي يكون على الملفات + YAML + Ledger + CoC فقط.

## 8. الخصوصية

- القضايا الحقيقية الحساسة تبقى محلية ومشفرة.
- لا ترفع محتوى حساساً إلى مستودعات عامة أو مشتركة غير آمنة.

## 9. قواعد v0.2.0 الإضافية

- **أرشيف vs تشغيلي:** لا تفرض CoC التشغيلي على وثائق NARA/FBI Vault/NTSB المنشورة؛ استخدم source-provenance.
- **Group-Entity:** لا تختلق أسماء لأفراد غير مسمّين؛ استخدم group-entity مع estimated-count.
- **Cold Case:** لا تعامل قضية مفتوحة/باردة كقضية مغلقة؛ فعّل case-status وCold-Case-Report.
- **Probable Cause:** في التقارير التقنية لا تختلق Findings؛ أعلن Contributing Factors وRecommendations بشكل منفصل.
- **Vehicle متخصص:** سفن وطائرات تستخدم vehicle-class + الحقول المتخصصة (IMO / N-number).
- **Informant / Wiretap:** لا ترفع إلى verified دون تقييم مصداقية / تفويض قانوني موثّق.

## 10. قواعد v0.3.0 الإضافية

- **Claim Trace:** كل تقرير معتمد / Court-File يحمل `claim-trace` (ادعاء → أدلة → support-level).
- **Readiness-Checklist:** ملف `00-Scaffold/Readiness-Checklist.md`؛ `readiness-passed: true` فقط بعد اكتمال البوابات.
- **Court-File:** ممنوع مع `readiness-passed: false` أو بلا claim-trace (critical في audit).
- **Counter substantive:** رابط Counter وحده لا يكفي؛ جسم الفرضية المضادة يجب أن يكون مضموناً (حد أدنى من النص).
- **Group-Entity:** عند group-entity للضحايا بلا `named-individuals`، لا تُنشئ Person بأسماء ضحايا فردية غير موجودة في الحزمة.
- **Series-Linkage (v0.3.1):** لا تدمج حوادث في سلسلة دون inclusion-criteria مكتوبة؛ احتفظ بـ peripheral و cluster counter.
- **Enterprise-Map (v0.3.1):** لا ترفع مشروع إجرامي إلى verified من تدفق مالي وحده دون predicates مدعومة وحدود صريحة.
- **Ledger gaps:** فضّل `gaps: [{id, description, phase_id, status}]` في Coverage-Ledger.
