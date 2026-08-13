# الطبقة البصرية التحقيقية — دستور + أدوات

**الوظيفة:** جعل جوهر المهارة (مناطق · status · Ledger · Chain-of-Custody · Hypotheses) **مرئياً** للمحقق دون استبدال الملفات كمصدر حقيقة.

---

## 1. مبدأ غير قابل للتفاوض

| الطبقة | ماذا تمثّل |
|--------|------------|
| **الملفات + YAML + Coverage-Ledger + Chain-of-Custody** | الحقيقة التشغيلية والتحقيقية |
| **Dashboard / Graph / Canvas** | **نظّارات** — عرض وملاحة وتفكير فقط |

- العرض البصري **لا** يضع معرفة في `01-Evidence`.
- ما يُرى على لوحة أو Canvas **لا** يغني عن `status` و`type` في frontmatter.
- **لا تُضف حقول frontmatter جديدة** لمجرد تجميل اللوحة.
- عمود حالة الأدلة يعيش في **Coverage-Ledger** — اللوحة تربط ولا تخترع.

---

## 2. خريطة الأدوات

| أداة | دورها في التحقيق |
|------|------------------|
| **Dashboard** | بوابة يومية: فجوات، فرضيات بلا Counter، أدلة بلا سلسلة حفظ، طابور المراجعة |
| **Dataview** | جداول حية من `type` / `status` / `hypothesis-kind` / `support-level` |
| **Graph** | شبكة العلاقات بين الأشخاص والأدلة والفرضيات والأحداث |
| **Canvas** | لوحات عمل: Evidence Board · Crime Scene · Timeline · Suspect Profile · Link Analysis · Native Format Protocol |
| **Excalidraw + Image Toolkit + Leaflet** (إضافات موصى بها) | تعليق على الصور، تكبير، خرائط جغرافية |

---

## 3. قواعد المناطق على الشاشة

| مجلد | يظهر كـ | ملاحظة بصرية |
|------|---------|--------------|
| `01-Evidence` | أدلة معتمدة | مركز Graph المفيد + لون مميز |
| `02-Entities` | كيانات | عقد رئيسية في الشبكة |
| `03-Hypotheses` | فرضيات | Primary بلون، Counter بلون مختلف، Rejected باهت |
| `04-Timeline` | أحداث | محور زمني |
| `05-Analysis` | تحليلات | حسب status |
| `02b-Exploration` | استكشاف | لا يُخلط لونياً مع Evidence |
| `08-Tooling` | أدوات ونتائج تحليلية | لا يُعرض كEvidence؛ يفضّل تجميعه منفصلاً |
| `case-logs` | سجل تشغيل | لا يُستخدم كبديل عن Chain-of-Custody |
| `00-Scaffold` | هيكل + لوحة | يُخفى من Graph الافتراضي |
| `99-Attachments` | مرفقات | يُخفى من Graph العام (ضوضاء) |

### Graph — الفلتر الافتراضي

```text
-path:99-Attachments -path:00-Scaffold
```

**مجموعات ألوان مقترحة (Groups بـ path):**

| Group | Query |
|-------|--------|
| Evidence | `path:01-Evidence` |
| Entities | `path:02-Entities` |
| Hypotheses | `path:03-Hypotheses` |
| Timeline | `path:04-Timeline` |
| Analysis | `path:05-Analysis` |
| Exploration | `path:02b-Exploration` |

التفاصيل في قالب `Graph-Setup.md`.

---

## 4. خمسة Canvas كبروتوكولات عمل

| الملف | الوظيفة |
|-------|---------|
| `01-Evidence-Board.canvas` | لوحة الخيوط الكلاسيكية (شخص ↔ دليل ↔ شخص) |
| `02-Crime-Scene-Map.canvas` | خريطة مسرح الجريمة + مواقع الأدلة |
| `03-Timeline-Canvas.canvas` | عرض بصري للخط الزمني والتناقضات |
| `04-Suspect-Profile.canvas` | ملف المشتبه (دافع + فرصة + وسيلة + سوابق) |
| `05-Link-Analysis.canvas` | شبكة علاقات موسّعة |

**بروتوكول كامل:** `Canvas-Protocol.md`.

**Canvas Native Format:** استخدم `assets/templates/canvases/Native-Format-Protocol.canvas` كنقطة بداية. يجب أن تكون IDs فريدة وأن تشير edges إلى nodes موجودة، وتُفحص JSON عبر `scripts/validate_obsidian_native.py`.

**Tool relation:** يمكن لعقدة Canvas أن تشير إلى `08-Tooling/Runs/` أو `05-Analysis/`، لكن لا تُنقل نتيجة الأداة إلى Evidence من خلال الرسم.

**قواعد Canvas:**
- اللوحة ≠ Evidence. ما على اللوحة تفكير حتى يُثبَّت في ملاحظة + YAML.
- Evidence Board: العقد الصلبة من `01-Evidence` و`02-Entities` فقط.
- بعد التخطيط على اللوحة: حدّث Coverage-Ledger و/أو الملاحظات الأصلية.
- لا حقول frontmatter جديدة من أجل Canvas.

---

## 5. بروتوكول «شاهد → ثبّت»

```
عرض / ترتيب / اكتشاف فجوة على Dashboard أو Graph أو Canvas
        ↓
تحديث الحقيقة: ملاحظة + YAML و/أو Coverage-Ledger و/أو Chain-of-Custody
        ↓
لا تعتمد على البطاقة البصرية وحدها في الاعتماد أو التقرير
```

---

## 6. إضافات أوبسيديان الموصى بها (حزمة التحقيق)

| الإضافة | الفائدة |
|---------|---------|
| **Dataview** | جداول ولوحات حية |
| **Image Toolkit** | تكبير وتدقيق الصور |
| **Excalidraw** | تعليق على الصور + رسوم |
| **Leaflet** أو **Map View** | خرائط جغرافية بعلامات |
| **Canvas Picture in Picture** | خلفيات شفافة في Canvas (اختياري) |

---

## 7. ما يُنشأ في الوضع أ (Scaffold)

```
00-Scaffold/
├── Investigation-Index.base
├── Dashboard.md
└── Visual/
    ├── README-Visual.md
    ├── Graph-Setup.md
    ├── Canvas-Protocol.md
    └── Canvases/
        ├── 01-Evidence-Board.canvas
        ├── 02-Crime-Scene-Map.canvas
        ├── 03-Timeline-Canvas.canvas
        ├── 04-Suspect-Profile.canvas
        ├── 05-Link-Analysis.canvas
        └── Native-Format-Protocol.canvas
08-Tooling/
├── Active/
├── Library/
├── Archive/
├── Manifests/
├── Audits/
├── Fixtures/
└── Runs/
case-logs/
├── session.jsonl
├── tool-runs.jsonl
└── decisions.md
```
