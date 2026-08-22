---
type: readiness-checklist
status: draft
created: "{{date}}"
updated: "{{date}}"
readiness-passed: false
tags: [scaffold, readiness]
---

# Readiness Checklist

Use before any **final** case-report adoption or **any** Court-File.

## Gates

| # | Check | Pass? |
|---|--------|-------|
| 1 | Minimum verified evidence in scope for used claims | [ ] |
| 2 | Every used evidence has CoC **or** source-provenance (archival) | [ ] |
| 3 | Every Primary has resolvable Counter (or written waiver in Changelog) | [ ] |
| 4 | Strong/conclusive hypotheses have non-empty supporting-notes | [ ] |
| 5 | Report has **claim-trace** (YAML + table) linking claims → evidence | [ ] |
| 6 | Open critical gaps declared in Coverage-Ledger **and** report | [ ] |
| 7 | No `status: exploration` in `01-Evidence` | [ ] |
| 8 | Informant/wiretap not verified without credibility / legal-authorization | [ ] |
| 9 | Group-entity used instead of inventing unnamed victim/passenger lists | [ ] |
| 10 | Human Gate recorded for sensitive items / final report | [ ] |

## Decision

- [ ] **Not ready** — report stays `draft` / `pending-human-review`; **no Court-File**
- [ ] **Ready** — set this note and the report frontmatter:
  - `readiness-passed: true`
  - `status: pending-human-review` then human approval

## Blockers
- 
- 

## Sign-off
- Reviewer:
- Date:
