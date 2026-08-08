---
type: canvas-protocol
status: verified
created: {{date}}
updated: {{date}}
tags: [visual, protocol]
---

# بروتوكول Canvas التحقيقي

## المبدأ
اللوحة أداة تفكير وترتيب واكتشاف فجوات.  
**الحقيقة** تبقى في الملاحظات + YAML + Coverage-Ledger + Chain-of-Custody.

## القواعد الخمس

1. **اللوحة ≠ Evidence**  
   لا تعتبر أي بطاقة على Canvas دليلاً معتمداً حتى تُنشأ/تُحدَّث ملاحظة حقيقية في `01-Evidence` أو `03-Hypotheses`.

2. **العقد الصلبة فقط من المناطق الصحيحة**  
   - أدلة ← `01-Evidence`  
   - أشخاص/مواقع ← `02-Entities`  
   - فرضيات ← `03-Hypotheses`  
   - أحداث ← `04-Timeline`

3. **بعد كل جلسة تخطيط**  
   حدّث:
   - Coverage-Ledger (إن تغيّرت تغطية مرحلة)
   - الملاحظات الأصلية (روابط، status)
   - Changelog إن كان قراراً هيكلياً

4. **الألوان والاتفاقيات**  
   - Primary Hypothesis → لون مميز  
   - Counter → لون مختلف  
   - Rejected → باهت أو إطار متقطع  
   - Evidence قوي → إطار واضح

5. **لا حقول frontmatter جديدة**  
   الاستعلامات والفلاتر تعتمد فقط على الحقول المعتمدة في taxonomy.

## استخدام كل لوحة

| اللوحة | متى تستخدمها | ماذا تثبّت بعدها |
|--------|--------------|------------------|
| Evidence Board | ربط أشخاص ↔ أدلة ↔ أشخاص | روابط في الملاحظات + Ledger |
| Crime Scene Map | ترتيب مواقع وأدلة موضعية | تحديث Location + Evidence |
| Timeline Canvas | رؤية التسلسل والتناقضات | تحديث Events + Contradictions |
| Suspect Profile | تجميع دافع/فرصة/وسيلة لمشتبه | تحديث Person + Hypotheses |
| Link Analysis | شبكة علاقات أوسع | تحديث Entities + Analysis |

## بروتوكول «شاهد → ثبّت»
1. اكتشف فجوة أو علاقة على اللوحة.
2. ارجع إلى الملاحظة الأصلية أو أنشئ واحدة.
3. حدّث YAML والروابط.
4. حدّث Ledger إن لزم.
5. لا تعتمد على اللوحة وحدها في التقرير.
