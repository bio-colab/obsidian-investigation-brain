# الشجرة المعيارية لمجلدات Vault القضية التحقيقية

هذه الشجرة إلزامية في وضع البناء الأولي (Scaffold Mode). يمكن توسيعها لاحقاً لكن لا تُحذف المناطق الأساسية ولا تُعاد تسميتها دون تسجيل في Changelog.

**v0.1.0:** Chain of Custody · Counter-Hypotheses · Timeline-first · Human Gate · Visual Protocols.

```
Case-Vault-XXXX/
├── 00-Scaffold/                              # الهيكل فقط — لا معرفة تحقيقية متحققة هنا
│   ├── AGENTS.md                             # تعليمات صريحة لأي وكيل يقرأ الـ vault
│   ├── Case-Scope.md                         # حدود النطاق (داخل / خارج) — أي تغيير يُسجَّل مع السبب
│   ├── Investigation-Plan.md                 # المراحل + الأهداف + الأولويات
│   ├── Team-Roles.md                         # صلاحيات كل محقق + من يراجع ماذا
│   ├── Review-Queue.md                       # MOC بوابة المراجعة البشرية (pending-human-review)
│   ├── Coverage-Ledger.md                    # مراحل التحقيق × فجوات الأدلة × الفرضيات
│   ├── Dashboard.md                          # لوحة قيادة تشغيلية (فجوات + قوة الأدلة + فرضيات)
│   ├── Visual/
│   │   ├── README-Visual.md
│   │   ├── Graph-Setup.md                    # Hide queries + مجموعات الألوان + Local Graph
│   │   ├── Canvas-Protocol.md                # بروتوكول التثبيت (اللوحة ≠ Evidence)
│   │   └── Canvases/                         # بروتوكولات عمل لا زينة
│   │       ├── 01-Evidence-Board.canvas      # لوحة الخيوط الكلاسيكية
│   │       ├── 02-Crime-Scene-Map.canvas
│   │       ├── 03-Timeline-Canvas.canvas
│   │       ├── 04-Suspect-Profile.canvas
│   │       └── 05-Link-Analysis.canvas
│   └── Meta/
│       ├── Vault-Philosophy.md
│       ├── Changelog.md                      # سجل التغييرات الكبرى + قرارات النطاق + ترقيات + رفض
│       └── (Milestones/)
│
├── 01-Evidence/                              # محتوى متحقق فقط (بعد Human Gate عند الحاجة)
│   ├── Physical/                             # بصمات، DNA، أسلحة، آثار، أجسام
│   ├── Digital/                              # هواتف، كاميرات، حسابات، سجلات رقمية، hash
│   ├── Testimonial/                          # إفادات شهود (مع تاريخ الجلسة + ظروف الإدلاء)
│   ├── Documentary/                          # مستندات، سجلات بنكية، عقود، مراسلات
│   └── Chain-of-Custody/                     # سجل إلزامي لكل دليل (جامع، وقت، مكان، حالة، شهود)
│
├── 02-Entities/
│   ├── Persons/
│   │   ├── Victims/
│   │   ├── Suspects/
│   │   ├── Witnesses/
│   │   └── Persons-of-Interest/
│   ├── Locations/
│   ├── Vehicles/
│   ├── Organizations/
│   └── Objects/                              # أدوات، مقتنيات، أدلة مادية مرتبطة بشخص
│
├── 03-Hypotheses/                            # سلسلة الإثبات التحقيقية
│   ├── Primary/                              # الفرضيات الرئيسية (مع support-level + Counter إلزامي)
│   ├── Alternative/                          # فرضيات بديلة معقولة
│   ├── Counter/                              # فرضيات مضادة — مقاومة التحيز التأكيدي
│   └── Rejected/                             # مع سبب الرفض الصريح + تاريخ الرفض
│
├── 04-Timeline/
│   ├── Master-Timeline.md                    # الخط الزمني الموحد للقضية
│   ├── Events/                               # أحداث فردية (timestamp + مصدر + روابط)
│   ├── Alibis/                               # حجج الغياب المرتبطة بأشخاص وأحداث
│   └── Contradictions/                       # تناقضات بين الإفادات أو الأدلة
│
├── 05-Analysis/                              # تحليلات (status يحدد إن كانت verified أو draft)
│   ├── Modus-Operandi/
│   ├── Motives/
│   ├── Behavioral-Patterns/
│   └── Link-Charts/
│
├── 02b-Exploration/                          # منطقة استكشاف مضبوطة (اختيارية/مؤقتة)
│   ├── Sandbox/                              # أفكار حرة status: exploration فقط
│   └── Promotion-Log/                        # سجل محاولات الترقية
│
├── 06-Outputs/                               # مخرجات قابلة للتصدير — ليست تلقائياً verified
│   ├── Case-Reports/                         # التقارير التحقيقية
│   ├── Court-File/                           # ما يُقدَّم للمحكمة
│   ├── Briefings/                            # إحاطات داخلية
│   ├── Snapshots/                            # نسخ مجمدة من التقارير في مراحل متقدمة
│   └── Press/                                # بيانات صحفية (إن وُجدت)
│
└── 90-Reference-Sources/          # مراجع عامة / أرشيف عام (اختياري)
├── 99-Attachments/                           # ملفات مرفقة (صور، تسجيلات، مستندات خام)
    ├── Images/
    ├── Audio-Video/
    ├── Documents/
    └── Raw-Exports/
```

## قواعد التسمية والمناطق

- استخدم أسماء إنجليزية للمجلدات الرئيسية.
- **`01-Evidence`**: منطقة Verified فقط. لا تخمين هنا.
- **`03-Hypotheses/Primary`**: كل فرضية رئيسية يجب أن ترتبط بفرضية مضادة في `Counter/`.
- **`01-Evidence/Chain-of-Custody`**: إلزامي. كل دليل جديد يحصل على سجل فوراً.
- **`02b-Exploration`**: كل ملاحظة فيها تحمل `status: exploration`. لا تُعامل كـ Evidence أبداً.
- **بروتوكول الترقية من Exploration → Evidence أو Hypothesis**:
  1. توثيق سبب الترقية في Changelog أو Promotion-Log.
  2. ربط بدليل حقيقي داخل الـ vault.
  3. مرور من Human Gate (`pending-human-review` ثم إقرار بشري).
  4. نقل الملف إلى المجلد المناسب وتغيير `status`.
- **Review-Queue**: MOC في Scaffold يسرد كل الملاحظات ذات `status: pending-human-review`.
- **Coverage-Ledger**: الملف الحي للتغطية — مراحل الخطة × حالة الأدلة × الفرضيات.
- أي مجلد جديد يُضاف يُصنَّف تحت إحدى المناطق أو يُوثَّق في Meta/Changelog.md.
