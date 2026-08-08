# سجل إثراء حزم المصادر (Packet enrichment log)

**تاريخ:** 2026-08-08 · مرتبط بإصدارة المهارة **v0.3.1**

## الهدف

تحويل مقتطفات stub إلى **مواد تدريبية كافية** للضغط على:

- CoC / source-provenance  
- Enterprise-Map / Series-Linkage  
- التناقضات والفجوات المعلنة  
- traps (اختلاق DNA، wiretap، اعترافات، هويات)

## الحزم المُثرَاة (ORG + SK)

| Case | ملفات مضافة/موسّعة | ضغط رئيسي |
|------|---------------------|-----------|
| CASE-ORG-COMMISSION-021 | hearing, territory, org-chart, TRAP | تنسيق/كوميشن، منع wiretap invent |
| CASE-ORG-NARCO-PIPE-022 | indictment, cash, route, TRAP | كميات متعارضة، منع purity invent |
| CASE-ORG-RICO-SHELL-023 | shells table, extort, xfer graph, TRAP | RICO/shells، ملكية متعارضة |
| CASE-ORG-UNION-RACKET-024 | audit, trial, witness, TRAP | skimming + lone embezzler counter |
| CASE-ORG-PORT-SMUG-025 | cargo table, CCTV, bribe tip, TRAP | رشوة غير مؤكدة vs شذوذ بضائع |
| CASE-SK-RIPPER-026 | police, press, letters, TRAP | cold identity، canonical dispute |
| CASE-SK-GREENRIVER-027 | task force, linkage, attrib, TRAP | group-entity، منع STR invent |
| CASE-SK-BTK-028 | comms, dormancy, ID pathway, TRAP | copycat counter، منع confession invent |
| CASE-SK-YORKSHIRE-029 | hoax, geo critique, conviction, TRAP | false trail / bias |
| CASE-SK-FICT-CORRIDOR-030 | 3 incidents, vehicle conflict, TRAP | open series، DNA pending |

كل حزمة: **≥ 4–5 ملفات** في `source_packet/` بما فيها `BRIEF.md` + `TRAP-NOTE.md`.

## ما لم يُثرَ بالكامل في هذه الدفعة

- حزم 001–020 الأصلية ما زالت أخف (مقتطفات أقصر). يمكن إثراؤها لاحقاً بنفس الأسلوب.

## ضمانات الشفافية

- لا `Truth band` داخل BRIEF (انظر `sanitize_packets.py` + `designer_notes.md`).  
- الـ GT يبقى في `ground_truth.yaml` للتحكيم فقط.  
- أثر الإثراء على المهارة موثّق في `docs/BENCHMARK_TRANSPARENCY.md`.
