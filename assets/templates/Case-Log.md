---
type: case-log
status: draft
created: {{date}}
updated: {{date}}
case-id: 
session-id: SESSION-000
log-format: jsonl
append-only: true
redactions: []
related-tools: []
tags: [tooling, log, trace]
---

# Case Log — SESSION-000

هذا الملف فهرس بشري للسجل الآلي الموجود في `case-logs/session.jsonl`. السجل الآلي هو المصدر الكامل لتتابع الأحداث التشغيلية؛ هذا الملف يلخص القرارات المهمة ولا يستبدله.

## Session scope

- الهدف:
- الوضع: A / B / C / D
- النطاق:
- المجلدات المسموح الكتابة إليها:

## Event schema

كل سطر في `session.jsonl` كائن JSON يتضمن، قدر الإمكان:

```json
{"ts":"YYYY-MM-DDTHH:MM:SSZ","event_id":"EV-000","event":"decision","session_id":"SESSION-000","summary":"...","observation":"...","decision":"...","uncertainty":"...","next_action":"...","confidence":"medium","refs":["[[Note]]"]}
```

## Durable decisions

| الوقت | القرار | الملاحظة/السبب | عدم اليقين | الخطوة التالية | المراجع |
|---|---|---|---|---|---|
| | | | | | |

## Recovery

استخدم `python3 scripts/case_memory.py resume <case-root> --last 12` لعرض snapshot مختصر. لا تطبع `session.jsonl` كاملاً داخل سياق الوكيل، ولا تسجل سلسلة التفكير السرية؛ سجّل فقط ما يمكن مراجعته من ملاحظة وقرار ومصدر وخطوة تالية.

## Redaction policy

احذف الأسرار والرموز المميزة والمعلومات الشخصية غير اللازمة من النسخ التي تُشارك. لا تحذف أحداثاً تغيّر تفسير النتيجة؛ سجّل redaction صراحة.
