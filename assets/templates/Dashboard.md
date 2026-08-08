---
type: dashboard
status: verified
created: {{date}}
updated: {{date}}
tags: [dashboard, visual]
---

# لوحة القيادة التحقيقية

> الحقيقة في الملفات + YAML + Ledger. هذه اللوحة عرض تشغيلي فقط.

## 1. حالة سريعة

- **القضية:** 
- **آخر تحديث للـ Ledger:** 
- **ملاحظات قيد المراجعة (Human Gate):** انظر [[Review-Queue]]

## 2. فجوات حرجة (Gap Intelligence)

- [ ] مراحل بلا أدلة كافية
- [ ] فرضيات Primary بلا Counter
- [ ] أدلة بلا Chain-of-Custody
- [ ] فترات زمنية فارغة
- [ ] تناقضات مفتوحة

> حدّث من [[Coverage-Ledger]]

## 3. استعلامات Dataview مقترحة

**كل الفرضيات:**
```dataview
TABLE hypothesis-kind, support-level, status, counter-hypothesis
FROM "03-Hypotheses"
WHERE type = "hypothesis"
SORT support-level DESC
```

**أدلة بانتظار المراجعة:**
```dataview
LIST
FROM "01-Evidence"
WHERE status = "pending-human-review"
```

**فرضيات Primary:**
```dataview
TABLE support-level, status, counter-hypothesis
FROM "03-Hypotheses/Primary"
WHERE type = "hypothesis"
```

## 4. اختصارات بصرية

> بعد نسخ ملفات Canvas من `assets/templates/canvases/` إلى `00-Scaffold/Visual/Canvases/` داخل vault القضية، استخدم الروابط التالية (عدّل المسار إن لزم):

- [[00-Scaffold/Visual/Canvases/01-Evidence-Board]] — لوحة الخيوط
- [[00-Scaffold/Visual/Canvases/03-Timeline-Canvas]] — الخط الزمني البصري
- [[00-Scaffold/Visual/Canvases/04-Suspect-Profile]] — ملف المشتبه
- [[00-Scaffold/Visual/Canvases/05-Link-Analysis]] — تحليل الروابط
- [[Coverage-Ledger]] — جدول التغطية
- [[Review-Queue]] — طابور المراجعة
- [[Master-Timeline]] — الخط الزمني النصي

## 5. ملاحظات اليوم
- 
