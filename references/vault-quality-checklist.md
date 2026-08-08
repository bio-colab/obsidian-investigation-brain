# قائمة تدقيق جودة الـ Vault التحقيقي

استخدم هذه القائمة يدوياً أو مع `scripts/audit_vault.py`.

## أ. الهيكل الأساسي

- [ ] `00-Scaffold/AGENTS.md` موجود ومحدّث
- [ ] `00-Scaffold/Case-Scope.md` مكتوب (داخل/خارج النطاق)
- [ ] `00-Scaffold/Investigation-Plan.md` موجود
- [ ] `00-Scaffold/Coverage-Ledger.md` موجود ويُحدَّث
- [ ] `00-Scaffold/Review-Queue.md` موجود
- [ ] `00-Scaffold/Readiness-Checklist.md` موجود (v0.3)
- [ ] `00-Scaffold/Team-Roles.md` (إن وُجد فريق)

## ب. منطقة Evidence

- [ ] لا يوجد محتوى `status: exploration` داخل `01-Evidence`
- [ ] كل دليل له `type` صحيح (physical / digital / testimonial / documentary)
- [ ] كل دليل له سجل في `Chain-of-Custody/` مرتبط
- [ ] الأدلة الحساسة تحمل `pending-human-review` حتى الاعتماد
- [ ] المرفقات في `99-Attachments` وليس مكررة داخل Evidence دون رابط

## ج. الفرضيات ومقاومة التحيز

- [ ] كل فرضية `hypothesis-kind: primary` لها `counter-hypothesis` مرتبط
- [ ] الفرضيات ذات `support-level: strong/conclusive` لها `supporting-notes` غير فارغة
- [ ] الفرضيات المرفوضة في `Rejected/` مع سبب وتاريخ
- [ ] لا اعتماد لفرضية قوية دون مرور Human Gate

## د. الخط الزمني

- [ ] يوجد `Master-Timeline.md` أو ما يعادله
- [ ] الأحداث المهمة لها ملاحظات `timeline-event` مع `timestamp` و`source`
- [ ] التناقضات المفتوحة موثّقة كـ `contradiction`
- [ ] Alibis مرتبطة بأشخاص وفترات زمنية

## هـ. Human Gate و Review-Queue و Readiness (v0.3)

- [ ] كل ملاحظة `pending-human-review` ظاهرة في Review-Queue
- [ ] القرارات (موافقة/رفض/إعادة) مسجّلة
- [ ] التقارير النهائية لم تُعتمد دون Macro-Review
- [ ] التقارير المعتمدة تحمل `claim-trace` غير فارغ
- [ ] لا Court-File مع `readiness-passed: false`
- [ ] Informant/wiretap ليسا verified بلا مصداقية/تفويض
- [ ] لا أسماء ضحايا مخترعة مع group-entity فارغ named-individuals

## و. Gap Intelligence (أسئلة سريعة)

1. هل توجد مرحلة في الخطة بلا أدلة كافية؟
2. هل توجد فرضية Primary بلا Counter؟
3. هل توجد أدلة بلا سلسلة حفظ؟
4. هل توجد فترات زمنية فارغة حرجة؟
5. هل توجد تناقضات مفتوحة دون خطة حل؟
6. هل Coverage-Ledger يحمل `gaps:` منظمة (v0.3.1)؟
7. جريمة منظمة: هل يوجد Enterprise-Map عند الحاجة؟
8. سلسلة جرائم: هل يوجد Series-Linkage عند الحاجة؟

## ز. التشغيل الآلي

```bash
python3 scripts/audit_vault.py /path/to/case-vault
python3 scripts/audit_vault.py /path/to/case-vault --md audit-report.md
python3 scripts/audit_vault.py /path/to/case-vault --json audit.json --strict
```

- Exit 0 = لا حرج
- Exit 1 = توجد انتهاكات critical (أو major مع --strict)
- Exit 2 = خطأ تشغيل
