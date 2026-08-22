---
type: tool-manifest
status: draft
created: "{{date}}"
updated: "{{date}}"
tool-id: TOOL-000
version: 0.1.0
runtime: python3
backend: none
network: denied
entrypoint: ""
source-hash: ""
input-hashes: []
output-hashes: []
writes-to:
  - 08-Tooling/Runs/
human-review: required
related-evidence: []
related-analysis: []
tags: [tooling, manifest]
---

# Tool Manifest — TOOL-000

## Purpose

ما السؤال التحليلي الذي تعالجه الأداة؟ وما الذي لا تدّعي الإجابة عنه؟

## Inputs

- Input path(s):
- Expected format:
- Read-only sources:

## Outputs

- Output path(s):
- Output type: `analysis` / `exploration` / `simulation`
- Downstream note(s):

## Safety boundary

- لا شبكة.
- لا أسرار.
- لا كتابة خارج `08-Tooling/` أو مسار مخرجات معلن.
- لا تغيير تلقائي لـ `01-Evidence` أو `status: verified`.

## Validation

- Fixture(s):
- Command:
- Expected result:

## Promotion decision

- [ ] Tool-Audit مكتمل
- [ ] Human Gate مكتمل
- [ ] مسموح بالنقل إلى `08-Tooling/Library/`
