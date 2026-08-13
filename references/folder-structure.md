# الشجرة المعيارية لمجلدات Vault القضية التحقيقية

هذه الشجرة إلزامية في وضع البناء الأولي (Scaffold Mode). يمكن توسيعها لاحقاً لكن لا تُحذف المناطق الأساسية ولا تُعاد تسميتها دون تسجيل في Changelog.

**v0.2.0:** source-provenance · Technical-Analysis · System-Failures · Cold-Case · Probable-Cause · Group-Entity · Vessel/Aircraft · Financial/Wiretap/Informant.

```
Case-Vault-XXXX/
├── 00-Scaffold/                              # الهيكل فقط — لا معرفة تحقيقية متحققة هنا
│   ├── AGENTS.md
│   ├── Case-Scope.md                         # + cold-since / case-status عند الحاجة
│   ├── Investigation-Plan.md
│   ├── Team-Roles.md
│   ├── Review-Queue.md
│   ├── Readiness-Checklist.md            # v0.3.0 — بوابة جاهزية التقارير/Court-File
│   ├── Coverage-Ledger.md
│   ├── Dashboard.md
│   ├── Visual/
│   │   ├── README-Visual.md
│   │   ├── Graph-Setup.md
│   │   ├── Canvas-Protocol.md
│   │   └── Canvases/
│   │       ├── 01-Evidence-Board.canvas
│   │       ├── 02-Crime-Scene-Map.canvas
│   │       ├── 03-Timeline-Canvas.canvas
│   │       ├── 04-Suspect-Profile.canvas
│   │       └── 05-Link-Analysis.canvas
│   └── Meta/
│       ├── Vault-Philosophy.md
│       ├── Changelog.md
│       └── (Milestones/)
│
├── 01-Evidence/                              # محتوى متحقق فقط
│   ├── Physical/
│   ├── Digital/                              # + wiretap-evidence, audio-visual
│   ├── Testimonial/                          # + informant-testimony
│   ├── Documentary/                          # + financial-record, cargo-manifest
│   ├── Data-Analysis/                        # v0.2.0 — محاكاة، نماذج، نتائج تحليل بيانات
│   ├── Chain-of-Custody/                     # تشغيلي (جمع → حفظ)
│   └── Source-Provenance/                    # v0.2.0 — للمصادر الأرشيفية/العامة (بديل CoC)
│
├── 02-Entities/
│   ├── Persons/
│   │   ├── Victims/
│   │   ├── Suspects/
│   │   ├── Witnesses/
│   │   ├── Persons-of-Interest/
│   │   └── Groups/                           # v0.2.0 — مجموعة ضحايا/ركاب/طاقم (Group-Entity)
│   ├── Locations/
│   ├── Vehicles/                             # Vehicle عام + Vessel / Aircraft عبر حقول متخصصة
│   ├── Organizations/
│   ├── Objects/
│   ├── System-Failures/                      # v0.2.0 — فشل تنظيمي/تقني/ثقافي
│   └── Regulatory-Gaps/                      # v0.2.0 — ثغرات تنظيمية
│
├── 03-Hypotheses/
│   ├── Primary/
│   ├── Alternative/
│   ├── Counter/
│   └── Rejected/
│
├── 04-Timeline/
│   ├── Master-Timeline.md
│   ├── Events/                               # + era / period / severity للتحذيرات
│   ├── Alibis/
│   └── Contradictions/
│
├── 05-Analysis/
│   ├── Modus-Operandi/
│   ├── Motives/
│   ├── Behavioral-Patterns/
│   ├── Link-Charts/
│   ├── Series-Linkage/                       # v0.3.1 — سلاسل / قتلة متسلسلون
│   ├── Enterprise-Maps/                      # v0.3.1 — جريمة منظمة / RICO-style
│   ├── Technical-Analysis/                   # v0.2.0 — محاكاة، حسابات ثباتية، نماذج
│   ├── Safety-Culture/                       # v0.2.0 — ثقافة سلامة الشركة
│   └── Survivability-Analysis/               # v0.2.0 — لماذا نجا البعض
│
├── 02b-Exploration/
│   ├── Sandbox/
│   └── Promotion-Log/
│
├── 06-Outputs/
│   ├── Case-Reports/
│   ├── Court-File/
│   ├── Briefings/
│   ├── Snapshots/
│   ├── Recommendations/                      # v0.2.0 — توصيات سلامة/تنظيمية (NTSB-style)
│   ├── Cold-Case-Reports/                    # v0.2.0 — تقارير قضايا باردة/مفتوحة
│   └── Press/
│
├── 07-Cold-Case/                             # v0.2.0 — اختياري عند case-status: cold-case / open
│   ├── Open-Leads/
│   └── What-We-Know/
│
├── 08-Tooling/                               # v0.4.0 — self-tooling محلي ومقيد
│   ├── Active/                                # أدوات القضية قيد التجربة
│   ├── Library/                               # أدوات راجعها الإنسان لإعادة الاستخدام
│   ├── Archive/                               # أدوات متقاعدة مع سبب الاحتفاظ
│   ├── Manifests/                             # Tool-Manifest
│   ├── Audits/                                # Tool-Audit ونتائج التشغيل
│   ├── Fixtures/                              # مدخلات اختبار صغيرة وغير حساسة
│   └── Runs/                                  # مخرجات تحليل/محاكاة قابلة لإعادة التشغيل
│
├── 90-Reference-Sources/                     # مراجع عامة / أرشيف عام
│
└── 99-Attachments/
    ├── Images/
    ├── Audio-Video/
    ├── Documents/
    └── Raw-Exports/

case-logs/                                     # سجل جلسة وأحداث الأدوات خارج Evidence
├── session.jsonl
├── tool-runs.jsonl
├── decisions.md
└── redactions.md
```

## قواعد التسمية والمناطق (محدثة v0.2.0)

- **`01-Evidence`**: Verified فقط. لا تخمين.
- **سلسلة الحفظ**:
  - أدلة تشغيلية (مادية/رقمية/شهادات ميدانية) → `Chain-of-Custody` إلزامي.
  - مصادر أرشيفية/عامة (`source-kind: public-archive`) → `source-provenance` إلزامي (بديل منطقي لـ CoC).
- **`03-Hypotheses/Primary`**: كل فرضية رئيسية → Counter إلزامي.
- **`02b-Exploration`**: `status: exploration` فقط.
- **Cold Case**: عند `case-status: cold-case` أو `open-investigation` يُفعَّل مجلد `07-Cold-Case/` ويُستخدم قالب Cold-Case-Report.
- **Group-Entity**: للضحايا/الركاب المتعددين غير المسمّين أو الجزئيين.
- **Vessel / Aircraft**: تُسجَّل تحت Vehicles مع حقول متخصصة (IMO / N-number / flag-state / type-certificate).
- `08-Tooling` لا يُعامل كEvidence؛ مخرجاته Analysis/Exploration حتى Human Gate.
- `case-logs` سجل تشغيل قابل للتتبع وليس بديلاً عن Chain-of-Custody.
- أي أداة جديدة تُوثَّق في Tool-Manifest وTool-Audit، وأي مجلد جديد يُوثَّق في Meta/Changelog.md.
