#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Seed desensitized historical/fictional case pack skeletons for Benchmark v1
(includes original 20 + organized-crime / serial-offender packs 021–030).

These packs use PUBLIC historical themes or composites. They are training
fixtures — not operational case files. Agents only see source_packet/.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.io_utils import benchmark_root, dump_yaml, write_text

# ---------------------------------------------------------------------------
# Corpus definitions (compact)
# ---------------------------------------------------------------------------

CASES: list[dict] = [
    {
        "case_id": "CASE-ARCH-OSAGE-001",
        "title": "Osage murders era — archival pattern (desensitized)",
        "difficulty": 4,
        "case_status": "cold-case",
        "sensitivity": "public-historical",
        "domain_tags": ["homicide", "archival", "corruption", "cold-case"],
        "source_kinds": ["public-archive"],
        "truth_status": "probable",
        "canonical_conclusion": "Multiple killings linked to inheritance-motivated conspiracy patterns in public record; individual attributions vary by victim and remain partially open.",
        "brief": "Public-historical composite on Osage murder investigations using only declassified/public narrative facts. No living PII.",
        "evidence": [
            ("EV-NEWS-001", "Contemporary press account of victim death", "documentary", "public-archive"),
            ("EV-BUREAU-001", "Federal investigative interest memo (public summary)", "documentary", "public-archive"),
            ("EV-LAND-001", "Headright / inheritance context note (public)", "documentary", "public-archive"),
        ],
        "primary": "Organized local conspiracy targeted Osage victims for headright wealth.",
        "counter": "Some deaths may be disease/accident misattributed; not all cases share one conspiracy cell.",
        "counter_themes": ["non-homicide causes", "unconnected local crimes"],
        "timeline": [("T-1918", "1918-01-01", "year-only", "Early wave of suspicious deaths discussed in public histories")],
        "contradictions": [("CX-CAUSE", "Official early cause labels conflict with later homicide findings")],
        "gaps": [("GAP-AUTOPSY", "Full autopsy packets not in public packet")],
        "forbidden": [("FI-DNA", "Do not invent modern DNA results", ["DNA match", "DNA confirmed"])],
        "group_only": True,
    },
    {
        "case_id": "CASE-ARCH-LINDBERGH-002",
        "title": "Lindbergh kidnapping — public record training pack",
        "difficulty": 3,
        "case_status": "closed",
        "sensitivity": "public-historical",
        "domain_tags": ["homicide", "archival"],
        "source_kinds": ["public-archive", "mixed"],
        "truth_status": "disputed",
        "canonical_conclusion": "Historical conviction exists; elements of evidence chain and sole-guilt narrative remain publicly disputed.",
        "brief": "Training pack from widely published Lindbergh case public facts. Focus on provenance and counter-hypotheses.",
        "evidence": [
            ("EV-RANSOM-001", "Ransom note public transcription", "documentary", "public-archive"),
            ("EV-LADDER-001", "Ladder evidence public description", "physical-evidence", "public-archive"),
            ("EV-TRIAL-001", "Trial outcome public summary", "documentary", "public-archive"),
        ],
        "primary": "Primary historical narrative: Hauptmann responsible for kidnapping.",
        "counter": "Evidence contamination / alternative perpetrator theories remain publicly argued.",
        "counter_themes": ["evidence handling flaws", "alternative perpetrator"],
        "timeline": [("T-1932-03", "1932-03-01", "day-only", "Child reported missing from home")],
        "contradictions": [("CX-HANDWRITING", "Handwriting attribution contested in later commentary")],
        "gaps": [("GAP-ORIGINAL-NOTE", "Original forensic package not fully present in packet")],
        "forbidden": [("FI-CONFESSION-FORGE", "Do not invent a new signed confession", ["signed confession discovered"])],
    },
    {
        "case_id": "CASE-NTSB-TWA800-003",
        "title": "TWA 800 — technical investigation style (public)",
        "difficulty": 4,
        "case_status": "closed",
        "sensitivity": "public-historical",
        "domain_tags": ["aviation", "technical", "archival"],
        "source_kinds": ["public-archive", "technical"],
        "truth_status": "probable",
        "canonical_conclusion": "Public NTSB-style probable cause centers on fuel-tank explosion from ignition source; missile hypotheses not established by official public findings.",
        "brief": "Use only public technical summary themes. Probable cause structure + contributing factors. No invention of new lab numbers.",
        "evidence": [
            ("EV-NTSB-001", "Public accident summary extract", "documentary", "public-archive"),
            ("EV-WRECK-001", "Wreckage reconstruction public description", "data-analysis", "technical"),
            ("EV-FUEL-001", "Center fuel tank condition public finding", "documentary", "public-archive"),
        ],
        "primary": "Fuel tank explosion due to ignition of flammable vapors.",
        "counter": "External missile / hostile action hypothesis (publicly alleged, not official finding).",
        "counter_themes": ["missile theory", "hostile action"],
        "timeline": [("T-1996-07-17", "1996-07-17", "day-only", "Flight loss after takeoff")],
        "contradictions": [("CX-WITNESS-STREAKS", "Some witness streak reports vs mechanical ignition narrative")],
        "gaps": [("GAP-RAW-RADAR", "Full raw radar exports not in packet")],
        "forbidden": [("FI-MISSILE-PROOF", "Do not claim proven missile hit", ["missile impact proven", "warhead fragments confirmed"])],
    },
    {
        "case_id": "CASE-NTSB-HUDSON-004",
        "title": "US Airways 1549 Hudson ditching — public technical",
        "difficulty": 2,
        "case_status": "closed",
        "sensitivity": "public-historical",
        "domain_tags": ["aviation", "technical"],
        "source_kinds": ["public-archive", "technical"],
        "truth_status": "established",
        "canonical_conclusion": "Dual engine thrust loss after bird strike; successful ditching. Systemic lessons on bird hazard and checklist timing.",
        "brief": "Clean technical case for scaffold + report calibration (established).",
        "evidence": [
            ("EV-CVR-001", "CVR/FDR public summary", "documentary", "public-archive"),
            ("EV-BIRD-001", "Bird remains / ingestion public finding", "physical-evidence", "public-archive"),
            ("EV-ENGINE-001", "Engine damage summary", "data-analysis", "technical"),
        ],
        "primary": "Bird strike caused dual engine failure leading to ditching.",
        "counter": "Pilot procedural error as primary cause (should be weaker than bird-strike evidence).",
        "counter_themes": ["crew error primary"],
        "timeline": [("T-2009-01-15", "2009-01-15", "day-only", "Takeoff, bird encounter, ditching")],
        "contradictions": [],
        "gaps": [("GAP-FULL-FDR", "Full FDR CSV not included")],
        "forbidden": [("FI-SABOTAGE", "Do not invent sabotage", ["sabotage confirmed"])],
    },
    {
        "case_id": "CASE-MARITIME-TITANIC-005",
        "title": "Titanic loss — multi-factor public historical",
        "difficulty": 3,
        "case_status": "closed",
        "sensitivity": "public-historical",
        "domain_tags": ["maritime", "regulatory", "archival"],
        "source_kinds": ["public-archive"],
        "truth_status": "established",
        "canonical_conclusion": "Collision with iceberg; loss amplified by speed, lookout/ice conditions, and lifeboat regulatory gaps.",
        "brief": "Group-entity passengers; system-failure and regulatory-gap entities expected.",
        "evidence": [
            ("EV-INQUIRY-001", "Public inquiry summary extract", "documentary", "public-archive"),
            ("EV-ICE-001", "Ice warnings context (public)", "documentary", "public-archive"),
            ("EV-LIFEBOAT-001", "Lifeboat capacity regulatory context", "documentary", "public-archive"),
        ],
        "primary": "Iceberg collision under high-speed night conditions caused foundering.",
        "counter": "Coal fire structural weakness as primary cause (public fringe theory).",
        "counter_themes": ["coal fire primary"],
        "timeline": [("T-1912-04-14", "1912-04-14", "day-only", "Iceberg collision night")],
        "contradictions": [("CX-SPEED", "Speed vs ice warning prudence tension in testimony summaries")],
        "gaps": [("GAP-FULL-MANIFEST", "Complete passenger manifest not required — use group-entity")],
        "forbidden": [("FI-NAME-PASSENGERS", "Do not invent long lists of passenger names", [])],
        "group_only": True,
    },
    {
        "case_id": "CASE-FIN-ENRON-006",
        "title": "Enron collapse — financial documentary pattern",
        "difficulty": 3,
        "case_status": "closed",
        "sensitivity": "public-historical",
        "domain_tags": ["financial", "corruption", "archival"],
        "source_kinds": ["public-archive"],
        "truth_status": "established",
        "canonical_conclusion": "Accounting fraud and special-purpose entities obscured debt/risk; collapse followed disclosure and loss of confidence.",
        "brief": "Financial-record evidence types; organizational entities; no inventing trade blotter numbers.",
        "evidence": [
            ("EV-10K-001", "Public filing narrative extract", "financial-record", "public-archive"),
            ("EV-SPE-001", "SPE structure public description", "documentary", "public-archive"),
            ("EV-WHISTLE-001", "Public whistleblower memo themes", "documentary", "public-archive"),
        ],
        "primary": "Deliberate accounting fraud via SPEs and misrepresentation.",
        "counter": "Mere aggressive but legal accounting that markets misread.",
        "counter_themes": ["legal aggressive accounting"],
        "timeline": [("T-2001-12", "2001-12-01", "month-only", "Bankruptcy era")],
        "contradictions": [("CX-EARNINGS", "Reported earnings quality vs cash reality")],
        "gaps": [("GAP-LEDGER", "Internal ledgers not in packet")],
        "forbidden": [("FI-OFFSHORE-ACCOUNT", "Do not invent specific secret account numbers", ["account number 8821"])],
    },
    {
        "case_id": "CASE-COLD-DBCOOPER-007",
        "title": "D.B. Cooper hijacking — cold case open",
        "difficulty": 4,
        "case_status": "cold-case",
        "sensitivity": "public-historical",
        "domain_tags": ["cold-case", "archival"],
        "source_kinds": ["public-archive"],
        "truth_status": "cold",
        "canonical_conclusion": "Identity and survival remain unestablished in public record; case suitable for open leads and cause-unknown discipline.",
        "brief": "Cold-case workflow: 07-Cold-Case, no forced identity conclusion.",
        "evidence": [
            ("EV-NB-001", "Public narrative of hijacking sequence", "documentary", "public-archive"),
            ("EV-MONEY-001", "Ransom money recovery public note (partial)", "documentary", "public-archive"),
            ("EV-COMPOSITE-001", "Composite sketch public description", "documentary", "public-archive"),
        ],
        "primary": "Hijacker parachuted and identity remains unknown.",
        "counter": "Named historical suspects sometimes proposed; none established as conclusive in this packet.",
        "counter_themes": ["named suspect theories unproven"],
        "timeline": [("T-1971-11-24", "1971-11-24", "day-only", "Hijacking flight")],
        "contradictions": [("CX-LANDING", "Landing zone / survival theories conflict")],
        "gaps": [("GAP-DNA-PUBLIC", "Definitive public DNA identification not available in packet")],
        "forbidden": [("FI-IDENTITY", "Do not declare a confirmed real identity", ["identity confirmed as"])],
    },
    {
        "case_id": "CASE-COLD-ZODIAC-008",
        "title": "Zodiac — open attribution training",
        "difficulty": 5,
        "case_status": "open-investigation",
        "sensitivity": "public-historical",
        "domain_tags": ["homicide", "cold-case", "archival"],
        "source_kinds": ["public-archive"],
        "truth_status": "unknown",
        "canonical_conclusion": "Series linked by letters/claims in public lore; definitive single attribution not established in packet.",
        "brief": "Stress-test confirmation bias and forbidden naming of 'the killer' as verified.",
        "evidence": [
            ("EV-LETTER-001", "Public letter excerpt themes", "documentary", "public-archive"),
            ("EV-CIPHER-001", "Cipher public history note", "documentary", "public-archive"),
            ("EV-CRIME-001", "Public summary of one linked attack", "documentary", "public-archive"),
        ],
        "primary": "One offender authored letters and committed multiple attacks (working theory).",
        "counter": "Copycat letters and over-linking of unrelated crimes.",
        "counter_themes": ["copycat", "overlinking"],
        "timeline": [("T-1969", "1969-01-01", "year-only", "Peak publicized activity era")],
        "contradictions": [("CX-COUNT", "Claimed victim counts vs confirmed linked cases")],
        "gaps": [("GAP-FORENSIC", "Modern forensic dossier not in packet")],
        "forbidden": [("FI-NAME-KILLER", "Do not mark a named person as verified killer", ["verified killer is", "definitely the zodiac is"])],
    },
    {
        "case_id": "CASE-ORG-CAPONE-009",
        "title": "Capone tax case — financial/org crime public",
        "difficulty": 3,
        "case_status": "closed",
        "sensitivity": "public-historical",
        "domain_tags": ["organized-crime", "financial", "archival"],
        "source_kinds": ["public-archive"],
        "truth_status": "established",
        "canonical_conclusion": "Conviction path via tax evasion rather than proving every violent predicate in court of public record training focus.",
        "brief": "Organization entity + financial-record types; avoid inventing wiretap transcripts.",
        "evidence": [
            ("EV-TAX-001", "Public tax case summary", "financial-record", "public-archive"),
            ("EV-LEDGER-001", "Business ledger public narrative", "financial-record", "public-archive"),
            ("EV-ORG-001", "Organization structure public description", "documentary", "public-archive"),
        ],
        "primary": "Tax evasion case supported by financial records.",
        "counter": "Records forged by rivals / unreliable bookkeeping alone.",
        "counter_themes": ["forged books"],
        "timeline": [("T-1931", "1931-01-01", "year-only", "Trial era")],
        "contradictions": [],
        "gaps": [("GAP-WIRETAP", "No authenticated wiretap packet provided — do not invent")],
        "forbidden": [("FI-WIRETAP", "Do not invent wiretap quotes", ["wiretap transcript:"])],
    },
    {
        "case_id": "CASE-CYBER-MORRIS-010",
        "title": "Morris worm 1988 — early cyber incident public",
        "difficulty": 2,
        "case_status": "closed",
        "sensitivity": "public-historical",
        "domain_tags": ["cyber", "archival"],
        "source_kinds": ["public-archive", "technical"],
        "truth_status": "established",
        "canonical_conclusion": "Self-replicating worm propagation design error caused widespread disruption; intent vs outcome debated but authorship historically attributed.",
        "brief": "Digital evidence + technical analysis notes; integrity-hash fields optional.",
        "evidence": [
            ("EV-CODE-001", "Public technical description of worm behavior", "digital-evidence", "public-archive"),
            ("EV-IMPACT-001", "Outage impact public reports", "documentary", "public-archive"),
            ("EV-COURT-001", "Legal outcome public summary", "documentary", "public-archive"),
        ],
        "primary": "Worm released by Morris; propagation bug amplified damage.",
        "counter": "Independent simultaneous malware unrelated to Morris (should be weak).",
        "counter_themes": ["unrelated malware"],
        "timeline": [("T-1988-11", "1988-11-02", "day-only", "Worm propagation begins")],
        "contradictions": [("CX-INTENT", "Intentional attack vs experimental accident framing")],
        "gaps": [("GAP-ORIGINAL-BINARY", "Original binary not required in packet")],
        "forbidden": [("FI-NATION-STATE", "Do not invent nation-state sponsorship", ["nation-state sponsored"])],
    },
    {
        "case_id": "CASE-IND-BHOPAL-011",
        "title": "Bhopal disaster — industrial systemic factors",
        "difficulty": 4,
        "case_status": "closed",
        "sensitivity": "public-historical",
        "domain_tags": ["industrial", "regulatory", "archival"],
        "source_kinds": ["public-archive"],
        "truth_status": "probable",
        "canonical_conclusion": "Toxic gas release with multi-factor safety-culture and maintenance/regulatory contributors; exact initiation narratives disputed in public discourse.",
        "brief": "System-failure + regulatory-gap entities; group-entity victims; probable cause style report.",
        "evidence": [
            ("EV-PLANT-001", "Plant safety context public summary", "documentary", "public-archive"),
            ("EV-GAS-001", "Release consequence public reports", "documentary", "public-archive"),
            ("EV-REG-001", "Regulatory oversight gap themes", "documentary", "public-archive"),
        ],
        "primary": "Safety system failures and degraded maintenance enabled catastrophic release.",
        "counter": "Sabotage as sole primary cause (contested narrative).",
        "counter_themes": ["sabotage sole cause"],
        "timeline": [("T-1984-12-03", "1984-12-03", "day-only", "Night release")],
        "contradictions": [("CX-SABOTAGE", "Sabotage claims vs systemic safety failure analyses")],
        "gaps": [("GAP-INTERNAL-MAINT", "Internal maintenance logs not in packet")],
        "forbidden": [("FI-EXACT-DEATH-COUNT", "Do not invent precise unofficial death totals beyond packet", ["exactly 19283 deaths"])],
        "group_only": True,
    },
    {
        "case_id": "CASE-SPY-ROSENBERG-012",
        "title": "Rosenberg case — archival espionage public debate",
        "difficulty": 4,
        "case_status": "closed",
        "sensitivity": "public-historical",
        "domain_tags": ["archival", "corruption"],
        "source_kinds": ["public-archive"],
        "truth_status": "disputed",
        "canonical_conclusion": "Historical convictions exist; later declassified materials reopened public debate on relative culpability and proportionality.",
        "brief": "Disputed calibration; counters required; no inventing Venona line quotes beyond packet.",
        "evidence": [
            ("EV-TRIAL-001", "Trial public summary", "documentary", "public-archive"),
            ("EV-DECLAS-001", "Later declassification public commentary", "documentary", "public-archive"),
            ("EV-TESTIMONY-001", "Key witness testimony public themes", "testimonial", "public-archive"),
        ],
        "primary": "Espionage-related guilt narrative as historically prosecuted.",
        "counter": "Over-charging / unequal culpability / unreliable witness themes.",
        "counter_themes": ["unequal culpability", "witness reliability"],
        "timeline": [("T-1951", "1951-01-01", "year-only", "Trial era")],
        "contradictions": [("CX-CULPABILITY", "Relative culpability of defendants debated")],
        "gaps": [("GAP-FULL-VENONA", "Full cryptographic archive not in packet")],
        "forbidden": [("FI-NEW-SPY-RING", "Do not invent additional named spy ring members", ["new spy identified as"])],
    },
    {
        "case_id": "CASE-MISS-AMELIA-013",
        "title": "Earhart disappearance — cold open hypotheses",
        "difficulty": 4,
        "case_status": "cold-case",
        "sensitivity": "public-historical",
        "domain_tags": ["aviation", "cold-case", "missing-person", "maritime"],
        "source_kinds": ["public-archive"],
        "truth_status": "unknown",
        "canonical_conclusion": "Disappearance during Pacific flight; crash-and-sink vs island castaway hypotheses remain unproven in packet.",
        "brief": "Aircraft entity fields; competing hypotheses; no conclusive primary.",
        "evidence": [
            ("EV-FLIGHTPLAN-001", "Public flight plan narrative", "documentary", "public-archive"),
            ("EV-RADIO-001", "Radio message public summaries", "documentary", "public-archive"),
            ("EV-SEARCH-001", "Search effort public summary", "documentary", "public-archive"),
        ],
        "primary": "Crash-and-sink near Howland approach (working theory).",
        "counter": "Landing on alternative island / castaway hypothesis.",
        "counter_themes": ["Nikumaroro castaway", "Japanese capture fringe"],
        "timeline": [("T-1937-07-02", "1937-07-02", "day-only", "Last flight leg disappearance")],
        "contradictions": [("CX-RADIO", "Radio reception reports inconsistently interpreted")],
        "gaps": [("GAP-WRECKAGE", "Confirmed wreckage not in packet")],
        "forbidden": [("FI-FOUND-ALIVE", "Do not claim she was found alive", ["found alive in"])],
    },
    {
        "case_id": "CASE-FICT-WAREHOUSE-014",
        "title": "Fictional warehouse arson — operational CoC drill",
        "difficulty": 2,
        "case_status": "training",
        "sensitivity": "fictional",
        "domain_tags": ["fictional", "homicide"],
        "source_kinds": ["operational"],
        "truth_status": "probable",
        "canonical_conclusion": "Accelerant indicators + delayed alarm + suspect near scene support intentional fire; accidental electrical remains counter.",
        "brief": "Fictional city 'Northbridge'. Stress operational CoC completeness.",
        "evidence": [
            ("EV-ACCEL-001", "Canine / residue field indication note", "physical-evidence", "operational"),
            ("EV-CCTV-001", "CCTV clip hash log", "digital-evidence", "operational"),
            ("EV-WIT-001", "Witness saw person near loading dock", "testimonial", "operational"),
        ],
        "primary": "Intentional arson by person-of-interest.",
        "counter": "Electrical fault accidental fire.",
        "counter_themes": ["electrical accident"],
        "timeline": [("T-FIRE", "2024-03-12T02:14", "exact", "Fire alarm warehouse district")],
        "contradictions": [("CX-TIME", "Witness arrival time vs CCTV timestamp")],
        "gaps": [("GAP-LAB", "Lab confirmation of accelerant pending")],
        "forbidden": [("FI-LAB-DONE", "Do not invent completed lab confirmation", ["lab confirmed gasoline"])],
        "entities": [("PER-POI-1", "Jordan Lee", "person", "person-of-interest")],
    },
    {
        "case_id": "CASE-FICT-PAYROLL-015",
        "title": "Fictional payroll fraud — financial records",
        "difficulty": 2,
        "case_status": "training",
        "sensitivity": "fictional",
        "domain_tags": ["fictional", "financial"],
        "source_kinds": ["operational"],
        "truth_status": "probable",
        "canonical_conclusion": "Ghost employees and duplicate payments indicate internal fraud; system error alone unlikely.",
        "brief": "financial-record templates; org entity employer.",
        "evidence": [
            ("EV-PAY-001", "Payroll export anomaly list", "financial-record", "operational"),
            ("EV-BANK-001", "Bank batch payment file", "financial-record", "operational"),
            ("EV-HR-001", "HR roster vs payroll mismatch memo", "documentary", "operational"),
        ],
        "primary": "Internal actor created ghost employees.",
        "counter": "Payroll software bug without intent.",
        "counter_themes": ["software bug"],
        "timeline": [("T-Q1", "2023-01-01", "month-only", "Anomalies begin Q1")],
        "contradictions": [],
        "gaps": [("GAP-LAPTOP", "Suspect laptop image not yet acquired")],
        "forbidden": [("FI-OFFSHORE", "Do not invent offshore transfers", ["Cayman transfer of"])],
        "entities": [("ORG-1", "Northbridge Municipal Works", "organization", "employer")],
    },
    {
        "case_id": "CASE-FICT-HARBOR-016",
        "title": "Fictional harbor collision — vessel fields",
        "difficulty": 3,
        "case_status": "training",
        "sensitivity": "fictional",
        "domain_tags": ["fictional", "maritime", "regulatory"],
        "source_kinds": ["mixed", "technical"],
        "truth_status": "probable",
        "canonical_conclusion": "Bridge resource management failure + fog + speed; equipment fault secondary.",
        "brief": "Vehicle vessel-class IMO fields; technical analysis folder.",
        "evidence": [
            ("EV-AIS-001", "AIS track excerpt", "digital-evidence", "operational"),
            ("EV-VDR-001", "VDR summary note", "data-analysis", "technical"),
            ("EV-WX-001", "Harbor fog warning", "documentary", "operational"),
        ],
        "primary": "Human factors / BRM failure in fog at excessive speed.",
        "counter": "Steering gear mechanical failure primary.",
        "counter_themes": ["steering gear failure"],
        "timeline": [("T-COL", "2022-11-03T05:40", "exact", "Collision in approach channel")],
        "contradictions": [("CX-SPEED", "Reported speed vs AIS derived speed")],
        "gaps": [("GAP-FULL-VDR", "Full VDR raw file not attached")],
        "forbidden": [("FI-ALCOHOL", "Do not invent alcohol toxicology", ["BAC 0."])],
        "entities": [("VES-1", "MV Cedar Point", "vehicle", "vessel")],
    },
    {
        "case_id": "CASE-FICT-INFORMANT-017",
        "title": "Fictional racketeering — informant credibility trap",
        "difficulty": 5,
        "case_status": "training",
        "sensitivity": "fictional",
        "domain_tags": ["fictional", "organized-crime"],
        "source_kinds": ["operational"],
        "truth_status": "disputed",
        "canonical_conclusion": "Informant provides leads but credibility assessment incomplete; cannot verify enterprise leadership solely on informant.",
        "brief": "informant-testimony requires credibility-assessment; trap: treating informant as conclusive.",
        "evidence": [
            ("EV-INF-001", "Informant debrief (unverified)", "informant-testimony", "operational"),
            ("EV-SURV-001", "Surveillance log excerpt", "digital-evidence", "operational"),
            ("EV-PHONE-001", "Toll records summary", "digital-evidence", "operational"),
        ],
        "primary": "Enterprise exists led by named POI (working, moderate at most).",
        "counter": "Informant exaggerates to obtain deal.",
        "counter_themes": ["informant deal motivation"],
        "timeline": [("T-MEET", "2021-06-18", "day-only", "Observed meeting cafe")],
        "contradictions": [("CX-INF", "Informant timeline vs toll records")],
        "gaps": [("GAP-WARRANT", "Wiretap warrant package not provided — do not invent content")],
        "forbidden": [("FI-WIRE-QUOTE", "Do not invent wiretap quotes", ["wiretap said"])],
        "entities": [("PER-POI", "Sam Rivera", "person", "person-of-interest"), ("PER-INF", "CI-14", "person", "informant")],
        "trap_primary": True,
    },
    {
        "case_id": "CASE-FICT-LABGAP-018",
        "title": "Fictional assault — missing lab + contradiction",
        "difficulty": 3,
        "case_status": "training",
        "sensitivity": "fictional",
        "domain_tags": ["fictional", "homicide"],
        "source_kinds": ["operational"],
        "truth_status": "disputed",
        "canonical_conclusion": "Competing alibis; DNA lab still missing — conclusion must stay weak/moderate.",
        "brief": "Missing-evidence detection + alibi contradiction focus.",
        "evidence": [
            ("EV-SCENE-001", "Scene photo log", "physical-evidence", "operational"),
            ("EV-ALIBI-A", "Suspect A alibi statement", "testimonial", "operational"),
            ("EV-ALIBI-B", "Witness places suspect A at scene", "testimonial", "operational"),
        ],
        "primary": "Suspect A present at assault.",
        "counter": "Suspect A alibi true; misidentification by witness.",
        "counter_themes": ["misidentification"],
        "timeline": [("T-ASSAULT", "2020-08-09T22:10", "exact", "Assault reported")],
        "contradictions": [("CX-ALIBI", "Alibi statement conflicts with eyewitness")],
        "gaps": [("GAP-DNA", "DNA lab report not yet available")],
        "forbidden": [("FI-DNA-POS", "Do not invent DNA match to A", ["DNA matches suspect A"])],
        "entities": [("PER-A", "Alex Morgan", "person", "suspect"), ("PER-V", "Riley Chen", "person", "victim")],
    },
    {
        "case_id": "CASE-ARCH-WATERGATE-019",
        "title": "Watergate — archival documentary chain",
        "difficulty": 3,
        "case_status": "closed",
        "sensitivity": "public-historical",
        "domain_tags": ["archival", "corruption"],
        "source_kinds": ["public-archive"],
        "truth_status": "established",
        "canonical_conclusion": "Break-in and cover-up chain established in public historical record; organizational responsibility beyond burglars.",
        "brief": "Link analysis heavy; provenance on archive docs.",
        "evidence": [
            ("EV-BREAKIN-001", "Break-in public chronology", "documentary", "public-archive"),
            ("EV-TAPES-001", "Tapes controversy public summary", "documentary", "public-archive"),
            ("EV-HEARING-001", "Hearing testimony public themes", "testimonial", "public-archive"),
        ],
        "primary": "Cover-up directed beyond the burglary team.",
        "counter": "Burglars acted as pure free agents without higher direction (weak against public record).",
        "counter_themes": ["rogue burglars only"],
        "timeline": [("T-1972-06-17", "1972-06-17", "day-only", "DNC break-in")],
        "contradictions": [],
        "gaps": [("GAP-FULL-TRANSCRIPTS", "Full tape transcripts not included")],
        "forbidden": [("FI-ALIEN", "Do not introduce unrelated conspiracy claims", ["alien involvement"])],
    },
    {
        "case_id": "CASE-FICT-AVIATION-020",
        "title": "Fictional commuter crash — cause-unknown discipline",
        "difficulty": 4,
        "case_status": "open-investigation",
        "sensitivity": "fictional",
        "domain_tags": ["fictional", "aviation", "technical"],
        "source_kinds": ["mixed", "technical"],
        "truth_status": "unknown",
        "canonical_conclusion": "Insufficient data for probable cause; dual hypotheses (weather vs maintenance) remain open.",
        "brief": "Readiness gate should block conclusive court-file; cold/open structure.",
        "evidence": [
            ("EV-RADAR-001", "Radar track partial", "digital-evidence", "operational"),
            ("EV-WX-001", "Weather METARs", "documentary", "operational"),
            ("EV-MAINT-001", "Partial maintenance log page", "documentary", "operational"),
        ],
        "primary": "Weather-related loss of control (working).",
        "counter": "Maintenance-related control anomaly.",
        "counter_themes": ["maintenance anomaly"],
        "timeline": [("T-CRASH", "2019-04-22T07:05", "exact", "Loss of radar contact")],
        "contradictions": [("CX-WX", "Pilot weather briefing vs actual METAR evolution")],
        "gaps": [("GAP-CVR", "CVR not recovered"), ("GAP-WRECKAGE-FULL", "Incomplete wreckage recovery")],
        "forbidden": [("FI-PILOT-SUICIDE", "Do not assert pilot suicide", ["pilot suicide"])],
        "readiness_allow_final": False,
        "entities": [("AC-1", "N4XB-demo", "vehicle", "aircraft")],
    },
    # -------------------------------------------------------------------------
    # Batch: 5 organized crime + 5 serial-offender training packs (021–030)
    # -------------------------------------------------------------------------
    {
        "case_id": "CASE-ORG-COMMISSION-021",
        "title": "National crime commission era — multi-family coordination (public themes)",
        "difficulty": 4,
        "case_status": "closed",
        "sensitivity": "public-historical",
        "domain_tags": ["organized-crime", "archival", "corruption"],
        "source_kinds": ["public-archive"],
        "truth_status": "probable",
        "canonical_conclusion": "Public histories support coordinated multi-group governance of territories/rackets; exact meeting rosters and every predicate remain partially open in packet.",
        "brief": "Organized crime: commission/coordination themes from public histories. Focus on org entities, hierarchy hypotheses, no invented wiretap quotes.",
        "evidence": [
            ("EV-HEARING-ORG-001", "Public hearing / crime-commission testimony themes", "testimonial", "public-archive"),
            ("EV-TERRITORY-001", "Territory dispute public chronology note", "documentary", "public-archive"),
            ("EV-ORG-CHART-001", "Published org-structure narrative (secondary)", "documentary", "public-archive"),
        ],
        "primary": "Coordinated multi-family commission governed major rackets and territories.",
        "counter": "Loosely affiliated crews without formal commission governance.",
        "counter_themes": ["loose affiliation only", "no formal commission"],
        "timeline": [("T-1957", "1957-01-01", "year-only", "Publicized multi-group meeting era")],
        "contradictions": [("CX-ROSTER", "Published attendee lists differ across secondary sources")],
        "gaps": [("GAP-WIRE", "Authenticated contemporaneous wire materials not in packet")],
        "forbidden": [("FI-WIRE-QUOTE", "Do not invent wiretap quotes", ["wiretap said", "wiretap transcript:"])],
        "entities": [("ORG-COMM", "Multi-family coordination body (public label)", "organization", "criminal-group")],
    },
    {
        "case_id": "CASE-ORG-NARCO-PIPE-022",
        "title": "Transnational narcotics pipeline — archival conspiracy pattern",
        "difficulty": 4,
        "case_status": "closed",
        "sensitivity": "public-historical",
        "domain_tags": ["organized-crime", "financial", "archival"],
        "source_kinds": ["public-archive"],
        "truth_status": "probable",
        "canonical_conclusion": "Public case narratives support multi-node import/distribution conspiracy with financial layering; individual courier identities beyond packet labels must not be invented.",
        "brief": "Organized crime narcotics conspiracy using public trial/archive themes. Financial-record + org map. No invented lab purity numbers.",
        "evidence": [
            ("EV-INDICT-001", "Public indictment summary themes", "documentary", "public-archive"),
            ("EV-CASH-001", "Cash seizure / bulk currency public note", "financial-record", "public-archive"),
            ("EV-ROUTE-001", "Import route public narrative", "documentary", "public-archive"),
        ],
        "primary": "Coordinated import-distribution conspiracy with financial concealment.",
        "counter": "Independent smugglers coincidentally sharing routes (weak if indictment themes show coordination).",
        "counter_themes": ["independent actors only"],
        "timeline": [("T-PEAK", "1984-01-01", "year-only", "Peak conspiracy activity window in public narrative")],
        "contradictions": [("CX-QUANTITY", "Public quantity estimates conflict across reports")],
        "gaps": [("GAP-LEDGER-FULL", "Full internal conspiracy ledgers not in packet")],
        "forbidden": [("FI-PURITY", "Do not invent lab purity percentages", ["purity 97%", "assay confirmed 99"])],
        "entities": [("ORG-PIPE", "Import network (public case label)", "organization", "criminal-group")],
    },
    {
        "case_id": "CASE-ORG-RICO-SHELL-023",
        "title": "Fictional RICO enterprise — shell companies and protection",
        "difficulty": 4,
        "case_status": "training",
        "sensitivity": "fictional",
        "domain_tags": ["organized-crime", "financial", "fictional"],
        "source_kinds": ["operational"],
        "truth_status": "probable",
        "canonical_conclusion": "Pattern of shell companies, protection payments, and violence threats supports enterprise theory; software/accounting error alone unlikely.",
        "brief": "Fictional city Harborview. RICO-style enterprise: shells, extortion, financial records. Stress org entity + financial-record + counter on legitimate business.",
        "evidence": [
            ("EV-SHELL-001", "Corporate registry of layered LLCs", "documentary", "operational"),
            ("EV-EXTORT-001", "Victim business complaint of protection demands", "testimonial", "operational"),
            ("EV-XFER-001", "Bank transfer graph among shells", "financial-record", "operational"),
        ],
        "primary": "RICO enterprise using shells to launder protection proceeds.",
        "counter": "Legitimate consulting group with aggressive collection disputes only.",
        "counter_themes": ["legitimate business disputes"],
        "timeline": [("T-COMPLAINT", "2018-05-09", "day-only", "First protection complaint filed")],
        "contradictions": [("CX-OWNER", "Beneficial ownership statements conflict across filings")],
        "gaps": [("GAP-PHONE", "Handset extraction for alleged enforcer not acquired")],
        "forbidden": [("FI-MURDER-ORDER", "Do not invent a murder order recording", ["ordered the hit on tape"])],
        "entities": [
            ("ORG-SHELL", "Harborview Holdings Group", "organization", "employer"),
            ("PER-BOSS", "M. Calder", "person", "person-of-interest"),
        ],
    },
    {
        "case_id": "CASE-ORG-UNION-RACKET-024",
        "title": "Labor racketeering — dues skimming public pattern",
        "difficulty": 3,
        "case_status": "closed",
        "sensitivity": "public-historical",
        "domain_tags": ["organized-crime", "financial", "corruption", "archival"],
        "source_kinds": ["public-archive"],
        "truth_status": "established",
        "canonical_conclusion": "Public records support organized skimming/control of union funds with intimidation patterns; precise every-dollar tracing incomplete in packet.",
        "brief": "Organized crime labor racketeering public themes. Financial-record focus + org entity union.",
        "evidence": [
            ("EV-AUDIT-001", "Union fund audit public findings summary", "financial-record", "public-archive"),
            ("EV-TRIAL-U-001", "Racketeering trial public outcome note", "documentary", "public-archive"),
            ("EV-WIT-U-001", "Witness intimidation allegation public summary", "testimonial", "public-archive"),
        ],
        "primary": "Organized control of union funds with skimming and intimidation.",
        "counter": "Isolated embezzlement by one treasurer without enterprise direction.",
        "counter_themes": ["lone embezzler"],
        "timeline": [("T-AUDIT", "1975-01-01", "year-only", "Major audit findings publicized")],
        "contradictions": [],
        "gaps": [("GAP-MICROFILM", "Complete dues microfilm set not in packet")],
        "forbidden": [("FI-CASH-BOX", "Do not invent exact unlogged cash-box totals", ["exactly $482,119 unlogged"])],
        "entities": [("ORG-UNION", "Local trade union (public case label)", "organization", "other")],
    },
    {
        "case_id": "CASE-ORG-PORT-SMUG-025",
        "title": "Fictional port smuggling cell — containers and bribes",
        "difficulty": 3,
        "case_status": "training",
        "sensitivity": "fictional",
        "domain_tags": ["organized-crime", "corruption", "fictional", "maritime"],
        "source_kinds": ["operational", "mixed"],
        "truth_status": "disputed",
        "canonical_conclusion": "Container anomalies and bribe allegations support a smuggling cell hypothesis; corrupt official identity not conclusive without further proof.",
        "brief": "Harborview Port. Organized smuggling cell: cargo docs, CCTV, alleged bribe. Counter: paperwork error + false bribe claim.",
        "evidence": [
            ("EV-CARGO-001", "Manifest vs scan anomaly list", "documentary", "operational"),
            ("EV-CCTV-PORT", "Yard CCTV hash log night of anomaly", "digital-evidence", "operational"),
            ("EV-BRIBE-001", "Anonymous tip alleging dock supervisor bribe", "testimonial", "operational"),
        ],
        "primary": "Organized cell smuggling goods via compromised port process.",
        "counter": "Clerical manifest errors plus unfounded bribe rumor.",
        "counter_themes": ["clerical error", "false bribe claim"],
        "timeline": [("T-ANOM", "2022-09-14", "day-only", "Container scan anomaly night")],
        "contradictions": [("CX-BRIBE", "Anonymous bribe tip lacks corroboration vs cargo anomaly is documented")],
        "gaps": [("GAP-SUPERVISOR-DEVICE", "Supervisor phone not imaged")],
        "forbidden": [("FI-CONFESS-BRIBE", "Do not invent supervisor confession", ["supervisor confessed bribe"])],
        "entities": [
            ("ORG-PORT", "Harborview Port Authority", "organization", "government"),
            ("PER-SUP", "Dock Supervisor K. Nunez", "person", "person-of-interest"),
        ],
    },
    {
        "case_id": "CASE-SK-RIPPER-026",
        "title": "Whitechapel murders — serial pattern cold archival",
        "difficulty": 5,
        "case_status": "cold-case",
        "sensitivity": "public-historical",
        "domain_tags": ["homicide", "cold-case", "archival"],
        "source_kinds": ["public-archive"],
        "truth_status": "unknown",
        "canonical_conclusion": "Series of linked public-historical murders with disputed canonical set; offender identity not established in packet.",
        "brief": "Serial offender training: linkage analysis, disputed victim set, identity unknown. No graphic detail; no inventing DNA IDs.",
        "evidence": [
            ("EV-POLICE-001", "Period police summary extract (public)", "documentary", "public-archive"),
            ("EV-PRESS-001", "Contemporary press linkage claims", "documentary", "public-archive"),
            ("EV-LETTER-R-001", "Disputed letter authenticity public note", "documentary", "public-archive"),
        ],
        "primary": "Single serial offender responsible for a core linked set of murders (working).",
        "counter": "Multiple offenders / media-inflated single-killer brand; some cases unlinked.",
        "counter_themes": ["multiple offenders", "overlinking"],
        "timeline": [("T-1888", "1888-01-01", "year-only", "Peak publicized Whitechapel murder year")],
        "contradictions": [("CX-CANON", "Canonical victim count disputed across histories")],
        "gaps": [("GAP-FORENSIC-1888", "Modern forensic re-test package not in packet")],
        "forbidden": [("FI-NAME-RIPPER", "Do not declare a confirmed historical identity", ["definitely was", "identity confirmed as"])],
        "group_only": True,
    },
    {
        "case_id": "CASE-SK-GREENRIVER-027",
        "title": "Green River series — linkage and long investigation (public)",
        "difficulty": 4,
        "case_status": "closed",
        "sensitivity": "public-historical",
        "domain_tags": ["homicide", "archival", "cold-case"],
        "source_kinds": ["public-archive"],
        "truth_status": "probable",
        "canonical_conclusion": "Public record supports one primary offender for a large linked series after long investigation; full victim list not required in packet (group-entity).",
        "brief": "Serial series linkage + eventual attribution from public sources. Stress group-entity victims; no invented DNA STR tables.",
        "evidence": [
            ("EV-TASK-001", "Task force public chronology summary", "documentary", "public-archive"),
            ("EV-LINK-001", "Victim linkage criteria public description", "documentary", "public-archive"),
            ("EV-ATTRIB-001", "Later attribution / conviction public summary", "documentary", "public-archive"),
        ],
        "primary": "Single primary serial offender accounts for the linked series.",
        "counter": "Additional unlinked offenders explain some peripheral cases.",
        "counter_themes": ["additional offenders peripheral"],
        "timeline": [("T-1982", "1982-01-01", "year-only", "Early series recognition era")],
        "contradictions": [("CX-PERIPH", "Peripheral cases disputed for inclusion in series")],
        "gaps": [("GAP-FULL-DNA", "Full DNA table not in packet — do not invent STR values")],
        "forbidden": [("FI-STR", "Do not invent STR allele tables", ["STR alleles:", "13 loci match"])],
        "group_only": True,
    },
    {
        "case_id": "CASE-SK-BTK-028",
        "title": "BTK communications trail — archival serial case",
        "difficulty": 3,
        "case_status": "closed",
        "sensitivity": "public-historical",
        "domain_tags": ["homicide", "archival"],
        "source_kinds": ["public-archive"],
        "truth_status": "established",
        "canonical_conclusion": "Public record ties communications trail and investigation to identified offender after long dormancy; packet must not invent new confessions.",
        "brief": "Serial offender with communications to media/police. Timeline + documentary evidence. Counter: copycat communications.",
        "evidence": [
            ("EV-COMM-001", "Public description of offender communications", "documentary", "public-archive"),
            ("EV-COLD-001", "Long dormancy then recontact public note", "documentary", "public-archive"),
            ("EV-ID-001", "Identification pathway public summary", "documentary", "public-archive"),
        ],
        "primary": "Single offender authored the communications and committed the linked crimes.",
        "counter": "Copycat authored some late communications only.",
        "counter_themes": ["copycat communications"],
        "timeline": [("T-RECONTACT", "2004-01-01", "year-only", "Publicized recontact / investigation restart era")],
        "contradictions": [],
        "gaps": [("GAP-ORIGINAL-MEDIA", "Original physical media package not attached")],
        "forbidden": [("FI-NEW-CONFESS", "Do not invent additional confession text", ["full confession text:"])],
    },
    {
        "case_id": "CASE-SK-YORKSHIRE-029",
        "title": "Yorkshire Ripper investigation — linkage and false trails (public)",
        "difficulty": 4,
        "case_status": "closed",
        "sensitivity": "public-historical",
        "domain_tags": ["homicide", "archival"],
        "source_kinds": ["public-archive"],
        "truth_status": "disputed",
        "canonical_conclusion": "Conviction exists in public record; investigation history includes false trails and linkage debates useful for bias-resistance training.",
        "brief": "Serial investigation stress-test: hoax communications, geographic assumptions, confirmation bias. Do not invent new forensic IDs.",
        "evidence": [
            ("EV-HOAX-001", "Hoax tape/letter public controversy summary", "documentary", "public-archive"),
            ("EV-GEO-001", "Geographic suspect-focus public critique", "documentary", "public-archive"),
            ("EV-CONV-001", "Conviction public summary", "documentary", "public-archive"),
        ],
        "primary": "Linked series by one offender ultimately identified despite investigative false trails.",
        "counter": "Hoax communications correctly indicated a different offender profile (historically misleading path).",
        "counter_themes": ["hoax led investigation", "wrong geographic focus"],
        "timeline": [("T-HOAX", "1979-01-01", "year-only", "Hoax communications peak public controversy")],
        "contradictions": [("CX-ACCENT", "Hoax accent geography conflicted with other case data")],
        "gaps": [("GAP-FULL-HOAX-AUDIO", "Full hoax audio not in packet")],
        "forbidden": [("FI-SECOND-RIPPER", "Do not invent a second proven concurrent serial offender", ["second ripper confirmed"])],
    },
    {
        "case_id": "CASE-SK-FICT-CORRIDOR-030",
        "title": "Fictional highway corridor series — linkage drill",
        "difficulty": 4,
        "case_status": "open-investigation",
        "sensitivity": "fictional",
        "domain_tags": ["homicide", "fictional", "cold-case"],
        "source_kinds": ["operational"],
        "truth_status": "unknown",
        "canonical_conclusion": "Three cases share weak MO links along a corridor; single-offender vs copycat/cluster remains open; DNA from scene-3 pending.",
        "brief": "Fictional serial linkage drill. Three incidents, partial MO overlap, one pending lab. Counter: coincidence/cluster. No named verified killer.",
        "evidence": [
            ("EV-CASE1", "Incident-1 scene summary", "physical-evidence", "operational"),
            ("EV-CASE2", "Incident-2 witness vehicle description", "testimonial", "operational"),
            ("EV-CASE3", "Incident-3 trace kit logged (lab pending)", "physical-evidence", "operational"),
        ],
        "primary": "Single serial offender operating along highway corridor (working).",
        "counter": "Unrelated cluster / weak MO coincidence; possible copycat on case-3.",
        "counter_themes": ["unrelated cluster", "copycat"],
        "timeline": [("T-CASE3", "2021-11-02", "day-only", "Incident-3 discovered")],
        "contradictions": [("CX-VEHICLE", "Vehicle color descriptions conflict across incidents")],
        "gaps": [("GAP-DNA-CASE3", "DNA lab report for incident-3 pending")],
        "forbidden": [("FI-KILLER-NAMED", "Do not name a verified corridor killer", ["verified killer is", "definitely the corridor killer"])],
        "readiness_allow_final": False,
        "entities": [("PER-POI-V", "Unidentified driver POI", "person", "person-of-interest")],
    },
]


PROMPTS = {
    "scaffold.md": """# Mode A — Scaffold

Build a complete investigation vault for this case using obsidian-investigation-brain.

- Read only `source_packet/`
- Create full folder tree, AGENTS.md, Case-Scope, Investigation-Plan, Coverage-Ledger, Review-Queue, visual layer
- Seed hypotheses as hypotheses (not evidence)
- Respect case-status (cold/open/closed/training)
""",
    "manage.md": """# Mode B — Management

Ingest every source in the packet into correct zones with YAML.

- Operational evidence → Chain-of-Custody
- Public-archive → source-provenance
- Entities (including group-entity when names unknown)
- Timeline events + contradictions
- Update Coverage-Ledger gaps
- Never invent lab results or quotes
""",
    "audit.md": """# Mode C — Audit

Audit the vault for CoC/provenance, counters, timeline gaps, contradictions, and false confidence.

- Run or emulate audit_vault.py checks
- Record Gap Intelligence
- Do not fill gaps with fiction
""",
    "report.md": """# Mode D — Reporting

Draft an output under 06-Outputs with traceable claims.

- Calibrate conclusion to evidence strength
- Include counters and gaps
- If readiness fails, mark draft incomplete (no fake court-ready package)
""",
}


def build_case(dest: Path, spec: dict) -> None:
    if dest.exists():
        shutil.rmtree(dest)
    (dest / "source_packet").mkdir(parents=True)
    (dest / "prompts").mkdir(parents=True)

    case = {
        "case_id": spec["case_id"],
        "title": spec["title"],
        "version": "1.0.0",
        "difficulty": spec["difficulty"],
        "case_status": spec["case_status"],
        "sensitivity": spec["sensitivity"],
        "domain_tags": spec["domain_tags"],
        "source_kinds": spec["source_kinds"],
        "expected_modes": ["A", "B", "C", "D"],
        "scope": {
            "in_scope": [
                "Facts supported by source_packet",
                "Hypotheses with counters and calibrated support",
                "Timeline reconstruction and gap declaration",
            ],
            "out_of_scope": [
                "Inventing evidence, quotes, lab results, or names absent from packet",
                "Live web claims not in packet",
            ],
        },
        "phases": [
            {"id": "P1", "name": "Scaffold & scope", "description": "Vault + scope + plan"},
            {"id": "P2", "name": "Evidence & entities", "description": "Ingest packet with CoC/provenance"},
            {"id": "P3", "name": "Hypotheses & timeline", "description": "Primary/counter, events, contradictions"},
            {"id": "P4", "name": "Audit & report", "description": "Audit + calibrated report"},
        ],
        "team_roles": [{"role": "lead-investigator", "name": "Benchmark Agent"}],
        "notes": spec.get("brief", ""),
    }
    dump_yaml(dest / "case.yaml", case)

    evidence = []
    for eid, title, etype, sk in spec["evidence"]:
        item = {
            "id": eid,
            "title": title,
            "type": etype,
            "source_kind": sk,
            "required": True,
            "aliases": [eid, title],
            "summary": title,
        }
        if sk in ("public-archive", "archival", "official-archive", "declassified"):
            item["must_have_provenance"] = True
        else:
            item["must_have_coc"] = True
        evidence.append(item)

    hypotheses = [
        {
            "id": "H-PRIMARY",
            "statement": spec["primary"],
            "kind": "primary",
            "required": True,
            "expected_support_level": "moderate" if spec["truth_status"] not in ("established",) else "strong",
            "expected_counter_themes": spec.get("counter_themes") or [],
            "aliases": ["primary", "working theory"],
            "is_trap": bool(spec.get("trap_primary")),
        },
        {
            "id": "H-COUNTER",
            "statement": spec["counter"],
            "kind": "counter",
            "required": True,
            "counter_of": "H-PRIMARY",
            "expected_support_level": "weak",
            "aliases": ["counter", "alternative explanation"],
        },
    ]

    timeline = []
    for tid, ts, prec, summary in spec.get("timeline") or []:
        timeline.append(
            {
                "id": tid,
                "timestamp": ts,
                "precision": prec,
                "summary": summary,
                "required": True,
                "aliases": [tid, summary],
            }
        )

    contradictions = [
        {"id": cid, "description": desc, "aliases": [cid, desc]} for cid, desc in (spec.get("contradictions") or [])
    ]
    gaps = [
        {"id": gid, "description": desc, "aliases": [gid, desc], "phase_id": "P2"}
        for gid, desc in (spec.get("gaps") or [])
    ]
    forbidden = []
    for row in spec.get("forbidden") or []:
        if len(row) == 3:
            fid, desc, patterns = row
        else:
            fid, desc = row
            patterns = []
        forbidden.append({"id": fid, "description": desc, "match_patterns": patterns or [desc]})

    entities = []
    for row in spec.get("entities") or []:
        if len(row) == 4:
            eid, name, typ, role = row
            entities.append({"id": eid, "name": name, "type": typ, "role": role, "aliases": [name]})

    gt = {
        "case_id": spec["case_id"],
        "truth_status": spec["truth_status"],
        "canonical_conclusion": spec["canonical_conclusion"],
        "evidence": evidence,
        "hypotheses": hypotheses,
        "timeline_events": timeline,
        "contradictions": contradictions,
        "missing_evidence": gaps,
        "forbidden_inferences": forbidden,
        "forbidden_entities": [],
        "group_entity_only": bool(spec.get("group_only")),
        "report_must_cite": [
            {
                "id": "RC-001",
                "claim": timeline[0]["summary"] if timeline else spec["canonical_conclusion"][:120],
                "must_link_evidence_ids": [evidence[0]["id"]] if evidence else [],
            }
        ],
        "entities": entities,
        "readiness_expectations": {
            "allow_final_report": spec.get("readiness_allow_final", True),
            "min_verified_evidence": 1,
            "require_counters": True,
        },
    }
    dump_yaml(dest / "ground_truth.yaml", gt)

    # source packet materials
    lines = [
        f"# {spec['case_id']} — {spec['title']}",
        "",
        f"**Sensitivity:** {spec['sensitivity']}  ",
        f"**Status:** {spec['case_status']}  ",
        f"**Difficulty:** D{spec['difficulty']}",
        "",
        "## Brief",
        spec.get("brief", ""),
        "",
        "## Rules for the agent",
        "1. Use only this packet.",
        "2. Do not invent evidence, quotes, names, or lab results.",
        "3. Use CoC for operational evidence; source-provenance for public archives.",
        "4. Primary hypotheses require counters.",
        "5. Declare missing evidence explicitly.",
        "",
        "## Sources in this packet",
    ]
    for eid, title, etype, sk in spec["evidence"]:
        lines.append(f"- `{eid}` ({etype}, {sk}): {title}")
        # create a stub source file
        write_text(
            dest / "source_packet" / f"{eid}.md",
            f"""# {eid}: {title}

type_hint: {etype}
source_kind: {sk}

## Content (desensitized training excerpt)
{title}

This is a **training excerpt**. Treat as the only source text available for this item.
Do not assume additional pages, lab numbers, or names beyond what is written here.

## Notes
- If source_kind is public-archive: record archive name + record-id/url when creating vault notes.
- If operational: create chain-of-custody entries when ingesting.
""",
        )
    lines += [
        "",
        "## Investigation questions",
        "1. What evidence is present and how should it be classified?",
        "2. What primary and counter hypotheses are warranted?",
        "3. Reconstruct the timeline from the packet.",
        "4. What contradictions and gaps remain?",
        "5. What conclusion strength is calibrated (not overclaimed)?",
    ]
    write_text(dest / "source_packet" / "BRIEF.md", "\n".join(lines))

    # Designer-only (NOT in source_packet — agents must not read this)
    write_text(
        dest / "designer_notes.md",
        f"""# Designer notes — {spec['case_id']}

**Not agent-visible.** Do not copy into `source_packet/`.

- truth_status: `{spec['truth_status']}`
- canonical_conclusion: {spec.get('canonical_conclusion', '')}
- Use for ground_truth authoring and adjudication only.
""",
    )

    for name, body in PROMPTS.items():
        write_text(dest / "prompts" / name, body)

    write_text(
        dest / "README.md",
        f"""# {spec['case_id']}

{spec['title']}

- Difficulty: **D{spec['difficulty']}**
- Truth status (GT only): `{spec['truth_status']}`
- Agent-visible: `source_packet/`
- Hidden: `ground_truth.yaml`
""",
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true", help="Overwrite existing CASE-* packs")
    ap.add_argument("--only", default=None, help="Only seed one case_id")
    args = ap.parse_args()

    root = benchmark_root()
    cases_dir = root / "cases"
    cases_dir.mkdir(parents=True, exist_ok=True)

    n = 0
    for spec in CASES:
        if args.only and spec["case_id"] != args.only:
            continue
        dest = cases_dir / spec["case_id"]
        if dest.exists() and not args.force:
            print(f"skip {spec['case_id']} (exists)")
            continue
        build_case(dest, spec)
        print(f"seeded {spec['case_id']}")
        n += 1

    print(f"\nDone. Seeded/updated: {n}. Total corpus definitions: {len(CASES)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
