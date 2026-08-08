# مِحَكّ الدماغ التحقيقي — `obsidian-investigation-brain`

مهارة (Skill) لبناء وإدارة **vault أوبسيديان** كمرجع تحقيقي موثوق مضاد للانحراف والتحيز.

**الإصدار:** 0.1.2  
**مبني على:** [Obsidian Research Brain Skill](https://github.com/bio-colab/obsidian-research-brain-skill) (v1.1.9)

---

## لماذا هذه المهارة؟

التحقيق الطويل ينزلق بسهولة إلى:
- اختلاط الأدلة بالتخمين
- تحيز تأكيدي (البحث فقط عما يدعم الفرضية المفضلة)
- فقدان سلسلة حفظ الأدلة
- خط زمني مبعثر
- تقارير تتجاهل الفجوات

هذه المهارة تفرض وعاءً منظماً، وسلسلة إثبات قابلة للدفاع، ومقاومة صريحة للتحيز، دون استبدال الحكم المهني للمحقق.

---

## الميزات الرئيسية

- **أربعة أوضاع:** Scaffold · Management · Audit · Reporting
- فصل صارم بين Evidence والفرضيات ومنطقة الاستكشاف
- **سلسلة حفظ أدلة (Chain of Custody)** إلزامية
- **Counter-Hypothesis** إلزامي لكل فرضية رئيسية
- **Timeline-first**
- **Human Gate** + Review-Queue
- **Gap Intelligence** تحقيقي
- Canvas كبروتوكولات عمل (Evidence Board · Crime Scene · Timeline · Suspect Profile · Link Analysis)
- سكريبت تدقيق آلي (`audit_vault.py`)

---

## Quick Start

1. فعّل المهارة واطلب بناء vault قضية من: رقم/اسم القضية + النطاق + خطة التحقيق (أو المراحل) + أدوار الفريق إن وُجدت.
2. الوكيل يعمل بـ **الوضع أ (Scaffold)**.
3. أضف الأدلة والكيانات والفرضيات في **الوضع ب** — Evidence فقط بأدلة حقيقية + سلسلة حفظ + Human Gate عند الحاجة.
4. للتدقيق: **الوضع ج** أو شغّل `scripts/audit_vault.py`.
5. لإنتاج تقرير: **الوضع د (Reporting)**.

**دليل مبسّط للمحقق:** [`references/guide-for-investigator.md`](references/guide-for-investigator.md)

---

## هيكل المستودع

```
obsidian-investigation-brain/
├── SKILL.md                          # تعريف المهارة والسلوك
├── README.md
├── CHANGELOG.md
├── references/
│   ├── folder-structure.md
│   ├── note-types-taxonomy.md
│   ├── yaml-frontmatter-standards.md
│   ├── agents-instructions-template.md
│   ├── anti-drift-rules.md
│   ├── vault-quality-checklist.md
│   ├── visual-investigation-layer.md
│   ├── reporting-pipeline.md
│   └── guide-for-investigator.md     # دليل المستخدم غير التقني
├── assets/templates/                 # قوالب الملاحظات + Canvas
│   └── canvases/                     # 5 لوحات بروتوكولية
└── scripts/
    └── audit_vault.py                # تدقيق حتمي
```

---

## الأوضاع الأربعة

| الوضع | متى |
|-------|-----|
| **أ — Scaffold** | بناء vault قضية من الصفر |
| **ب — Management** | إضافة أدلة، كيانات، فرضيات، أحداث |
| **ج — Audit** | فحص سلسلة الحفظ، Counter، الفجوات |
| **د — Reporting** | تقرير قضية أو ملف محكمة |

---

## تحذيرات مهمة

- استخدم قضايا عامة أو تدريبية (مثل ملفات FBI Vault العامة) عند المشاركة أو النشر.
- القضايا الحقيقية الحساسة تبقى **محلية ومشفرة**.
- هذه أداة مساعدة للمحقق وليست بديلاً عن الإجراءات الرسمية أو الحكم القضائي.
- لا تُستخدم لاختلاق أدلة أو شهادات.

---

## التوافق

- أوبسيديان (محلي أولاً)
- إضافات موصى بها للطبقة البصرية: Dataview، Image Toolkit، Excalidraw، Leaflet / Map View
- يعمل مع وكلاء الذكاء الاصطناعي عبر تعليمات `AGENTS.md` داخل كل vault
