---
type: tool-manifest
status: verified
created: 2026-08-13
updated: 2026-08-13
tool-id: EXAMPLE-METADATA-COMPARATOR
version: 0.1.0
runtime: python3
backend: docker
network: denied
entrypoint: 08-Tooling/Active/metadata_comparator.py
inputs:
  - 08-Tooling/Fixtures/metadata-comparator.json
writes-to:
  - 08-Tooling/Runs/
human-review: required
related-evidence: []
tags: [tooling, example]
---

# Example Metadata Comparator

هذا manifest مثال تعليمي. عند نسخه إلى قضية، يجب تثبيت `source-hash` الحقيقي، وإعادة اختبار fixture، وإنشاء Tool-Audit خاص بالقضية. النتيجة تحليلية لا دليل مستقل.
