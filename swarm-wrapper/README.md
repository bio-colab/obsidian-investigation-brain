# Investigation Swarm Wrapper MVP

هذه طبقة تشغيل مستقلة فوق `obsidian-investigation-brain`. هدفها تنسيق أدوار متعددة وإنتاج **proposals** و**conflict reports** و**consensus drafts** فقط. لا تكتب إلى `01-Evidence` ولا تغيّر `status` ولا تنتج Court-File تلقائياً.

## التشغيل الآمن

يتطلب التشغيل `Python 3.10+` و`PyYAML`، وهي نفس الاعتمادية المستخدمة في أدوات الـ vault الحالية.

```bash
# تحقق من manifest فقط
python3 swarm-wrapper/run.py validate \
  --manifest swarm-wrapper/examples/team-manifest.yaml

# أنشئ vault تجريبياً يحتوي على 01-Evidence ثم شغّل dry-run
python3 swarm-wrapper/run.py run \
  --manifest swarm-wrapper/examples/team-manifest.yaml \
  --vault-root /path/to/demo-vault \
  --run-id RUN-DEMO-001
```

`run-id` معرف آمن فقط من الأحرف والأرقام والنقطة والشرطة السفلية والشرطة، وليس مساراً. كما أن `entrypoint` و`inputs` و`output-dir` و`writes-to` يجب أن تكون مسارات نسبية بلا `.` أو `..`، ويُرفض أي مسار يحل خارج Vault أو يمر عبر symlink خارجي قبل إنشاء المجلدات أو تشغيل الأداة.

تُحفظ النتائج في:

```text
08-Tooling/Swarm/TEAM-DEMO-001/runs/RUN-DEMO-001/
├── run.json
├── proposals/*.md
├── conflicts.md
├── consensus-draft.md
└── human-gates/GATE-TEAM-DEMO-001-RUN-DEMO-001.md
```

## OpenMausBot mode

يمكن أن يضم manifest `mode: openmausbot` و`bot_id` لكل agent. يستخدم العميل المحلي `GET /api/bots` و`POST /api/bots/<bot_id>/messages` ثم ينتظر thread حتى يهدأ. لا يستخدم wrapper مسار `ask_bot` الداخلي؛ فهو يملك fan-out والـ correlation والمهلات بنفسه.

قبل هذا الوضع يجب تشغيل OpenMausBot على loopback فقط، واستخدام bots تجريبية، وتعطيل computer وComposio للقضية. لا تُمرر أسرار أو بيانات Evidence حساسة إلى agent قبل إعداد سياسة احتفاظ ومراجعة بشرية.

## قواعد التصميم

- كل رد وكيل untrusted analysis text، ويُحلل إلى Proposal مهيكل أو يُوسم `unstructured`.
- كل تشغيل ينتج Human Gate pending؛ لا توجد دالة promotion في هذا MVP.
- `dry-run` حتمي ولا يتصل بشبكة أو نموذج، ولذلك هو المسار الأول للاختبار.
- fan-out محدود بـ `max_workers <= 8`، والمهلة والحد الأقصى للمطالبات معرفان في manifest.
- المصدر يُثبت بـ snapshot hash، لكن hash لا يحول النص إلى Evidence؛ يبقى التحقق المنهجي منفصلاً.
