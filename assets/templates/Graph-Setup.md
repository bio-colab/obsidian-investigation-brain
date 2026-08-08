---
type: visual-doc
status: verified
created: {{date}}
updated: {{date}}
tags: [visual]
---

# إعداد Graph View التحقيقي

## الفلتر الافتراضي (Hide الضوضاء)

انسخ في فلتر Graph:

```text
-path:99-Attachments -path:00-Scaffold
```

هذا يخفي المرفقات والهيكل ويبقي الشبكة التحقيقية واضحة.

## مجموعات الألوان المقترحة (Groups)

أنشئ Groups في إعدادات Graph باستخدام `path:` فقط:

| اسم المجموعة | Query | لون مقترح |
|--------------|-------|-----------|
| Evidence | `path:01-Evidence` | أخضر / أزرق داكن |
| Entities | `path:02-Entities` | برتقالي |
| Hypotheses | `path:03-Hypotheses` | بنفسجي |
| Timeline | `path:04-Timeline` | أصفر / ذهبي |
| Analysis | `path:05-Analysis` | رمادي مزرق |
| Exploration | `path:02b-Exploration` | رمادي فاتح |

## مشاهدات مفيدة

**A — شبكة القضية الكاملة**  
الفلتر أعلاه + كل المجموعات مفعّلة.

**B — التركيز على فرضية**  
افتح Local Graph على ملاحظة Hypothesis محددة.

**C — التركيز على شخص**  
Local Graph على ملاحظة Person → يظهر الأدلة والأحداث والفرضيات المرتبطة.

**D — إخفاء المرفوض**  
أضف يدوياً استبعاد ملاحظات `status: rejected` عبر البحث أو الإضافات إن لزم.

## نصائح
- لا تعتمد على Graph وحده لإثبات علاقة. العلاقة الحقيقية = رابط داخل الملاحظة + YAML.
- بعد إضافة روابط كثيرة، أعد تحميل Graph.
- احفظ Workspace أو Bookmark لهذا الإعداد إن أمكن.
