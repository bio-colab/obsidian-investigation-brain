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
{"ts":"YYYY-MM-DDTHH:MM:SSZ","event":"tool.run","session_id":"SESSION-000","tool_id":"TOOL-000","backend":"none","command_digest":"sha256:...","inputs":["sha256:..."],"outputs":["sha256:..."],"exit_code":0}
```

## Durable decisions

| الوقت | القرار | السبب | المراجع |
|---|---|---|---|
| | | | |

## Redaction policy

احذف الأسرار والرموز المميزة والمعلومات الشخصية غير اللازمة من النسخ التي تُشارك. لا تحذف أحداثاً تغيّر تفسير النتيجة؛ سجّل redaction صراحة.
