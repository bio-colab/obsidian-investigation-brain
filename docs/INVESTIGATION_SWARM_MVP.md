# Investigation Swarm Wrapper MVP

## الغرض

هذه الطبقة تنسق مجموعة صغيرة من الوكلاء حول قضية تدريبية أو محلية، لكنها لا تغيّر تعريف Evidence في `obsidian-investigation-brain`. OpenMausBot هو طبقة تشغيل اختيارية؛ الـ vault والمدقق هما طبقة artifacts والمنهجية.

## حدود MVP

يدعم الإصدار الحالي `dry-run` الحتمي للاختبارات، و`openmausbot` عبر HTTP المحلي إلى bots محددة مسبقاً. يرسل orchestrator turns مستقلة بصورة متوازية محدودة، يلتقط الردود، يحاول تحليل JSON المهيكل، ثم يكتب proposals وconflicts وconsensus draft وHuman Gate.

لا يدعم الإصدار الحالي promotion، ولا الكتابة إلى Evidence، ولا fork/merge، ولا case library، ولا auto-judge، ولا إرسال بيانات إلى Composio أو computer use. هذه قيود مقصودة وليست نواقص مخفية.

## مسار التشغيل

```text
Team Manifest
     │ validate
     ▼
Source snapshot + hash
     │
     ├── agent A ──┐
     ├── agent B ──┼── bounded fan-out
     └── red team ┘
             │
             ▼
       Proposal parser
             │
     ┌───────┴────────┐
     ▼                ▼
Conflicts       Consensus draft
     │                │
     └───────┬────────┘
             ▼
       Human Gate pending
```

كل agent له `agent_id` وrole وtask وjurisdiction وbot_id اختياري. كل run له `case_id` و`team_id` و`run_id` وsource snapshot hash. هذه المعرفات تمنع خلط مخرجات فريق بآخر.

## بنية المخرجات

```text
08-Tooling/Swarm/<team-id>/runs/<run-id>/
├── run.json
├── proposals/<agent-id>.md
├── conflicts.md
├── consensus-draft.md
└── human-gates/<gate-id>.md
```

ويسجل `case-logs/session.jsonl` أحداثاً مختصرة عن إنشاء التشغيل وكتابة المقترحات وإنتاج المسودة. لا يُنسخ chain-of-thought الخام؛ النص الخام محفوظ داخل proposal على أنه untrusted analysis text لأغراض المراجعة فقط.

## علاقة OpenMausBot

في وضع `openmausbot` يستخدم العميل المسارين العموميين `GET /api/bots` و`POST /api/bots/<id>/messages` ثم ينتظر thread حتى يهدأ. لا يعتمد على `ask_bot` الداخلي، لأن ذلك المسار one-hop ومملوك لهارنس OpenMausBot. بذلك يبقى fan-out والمهلات والـ correlation تحت سيطرة wrapper، مع احترام loopback وعدم كشف token داخلي.

قبل تفعيل live mode يجب تشغيل OpenMausBot على `127.0.0.1`، إنشاء bots اختبارية، تعطيل computer وComposio، وعدم تمرير قضية حساسة قبل تحديد retention وredaction. مخرجات agent تبقى draft مهما كان النموذج أو عدد الوكلاء.

## استخدام

```bash
python3 swarm-wrapper/run.py validate \
  --manifest swarm-wrapper/examples/team-manifest.yaml

mkdir -p /tmp/swarm-vault/01-Evidence
printf '%s\n' 'training source' > /tmp/swarm-vault/01-Evidence/source.txt

python3 swarm-wrapper/run.py run \
  --manifest swarm-wrapper/examples/team-manifest.yaml \
  --vault-root /tmp/swarm-vault \
  --run-id RUN-TRAINING-001

python3 scripts/validate_swarm.py /tmp/swarm-vault \
  --team-id TEAM-DEMO-001 \
  --run-id RUN-TRAINING-001
```

## التوسعة بعد MVP

الخطوة التالية ليست إضافة UI مباشرة. يجب أولاً إضافة event correlation موحد، cancellation، cost budget، وsemantic conflict review على fixtures. بعد ذلك يمكن إضافة route داخل OpenMausBot أو لوحة War Room، مع الحفاظ على wrapper versioned كطبقة مستقلة.
