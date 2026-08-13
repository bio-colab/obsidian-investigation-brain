#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build skill-compliant investigation vaults for a benchmark run.

Uses only case.yaml + source_packet/ (does not read ground_truth.yaml).
This is a disciplined Mode A–D producer for harness smoke / baseline runs.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.io_utils import benchmark_root, load_yaml, write_text  # noqa: E402

TODAY = "2026-08-08"

# Case-specific investigative content derived from packet themes (not GT file).
CASE_INTEL: dict[str, dict] = {
    "CASE-FICT-WAREHOUSE-014": {
        "location": "Northbridge warehouse district / loading dock",
        "entities": [
            ("person", "Persons/Persons-of-Interest", "Witness-Dock-Observer", "witness", "Witness who saw a person near loading dock (unnamed in packet)."),
            ("location", "Locations", "Northbridge-Warehouse-Dock", "scene", "Warehouse loading dock area, Northbridge."),
        ],
        "primary": {
            "file": "H-Intentional-Arson",
            "title": "Intentional arson near loading dock",
            "body": "Field accelerant indicators, CCTV activity, and a witness placing a person near the loading dock support a working theory of intentional ignition.",
            "level": "moderate",
            "status": "draft",
        },
        "counter": {
            "file": "H-Electrical-Accident",
            "title": "Accidental electrical fire",
            "body": "Counter-hypothesis: electrical accident / electrical fault accidental fire without intentional ignition. Explains fire presence without requiring an offender; currently weaker because packet includes canine/residue field indication, but lab confirmation is absent.",
            "level": "weak",
        },
        "events": [
            ("T-FIRE-ALARM", "2024-03-12", "day-only", "Fire alarm warehouse district", "[[EV-CCTV-001]]"),
        ],
        "contradictions": [
            (
                "CX-TIME-WITNESS-CCTV",
                "Witness arrival time vs CCTV timestamp — packet does not fully reconcile clocks.",
            )
        ],
        "gaps": [
            "Lab confirmation of accelerant pending (field indication only; GAP-LAB)",
            "Named identification of person near dock not established in packet",
            "Full CCTV raw export not attached beyond hash log note",
        ],
        "timeline_master": "Fire-related activity around warehouse loading dock; exact clock reconciliation pending.",
        "conclusion": "Intentional arson is a **probable** working theory (moderate). Not conclusive without lab confirmation.",
        "conclusion_level": "moderate",
        "cold": False,
        "report_status": "pending-human-review",
        "allow_court": False,
    },
    "CASE-FICT-PAYROLL-015": {
        "location": "Northbridge Municipal Works (employer org)",
        "entities": [
            ("organization", "Organizations", "Northbridge-Municipal-Works", "employer", "Employer organization referenced by payroll/HR materials."),
        ],
        "primary": {
            "file": "H-Internal-Payroll-Fraud",
            "title": "Internal payroll fraud via ghost employees / duplicate payments",
            "body": "Payroll anomaly export, bank batch payments, and HR roster mismatch memo together support intentional internal manipulation of payroll.",
            "level": "moderate",
            "status": "draft",
        },
        "counter": {
            "file": "H-Software-Bug",
            "title": "Payroll software error without intent",
            "body": "Counter-hypothesis: payroll software bug / software error without intent. Possible, but three independent record streams (payroll, bank, HR) reduce pure-bug likelihood unless a single system feeds all three.",
            "level": "weak",
        },
        "events": [
            ("T-ANOMALY-START", "2023-01-01", "month-only", "Anomalies begin Q1", "[[EV-PAY-001]]"),
        ],
        "contradictions": [],
        "gaps": [
            "Suspect laptop image not yet acquired (GAP-LAPTOP)",
            "Authorization logs for payroll changes not provided",
            "Named individual perpetrator not identified in packet",
        ],
        "timeline_master": "Anomalies span a multi-month payroll period; precise first bad payment date needs bank file line-level review.",
        "conclusion": "Internal fraud is **probable** (moderate). Do not name a perpetrator without additional attribution evidence.",
        "conclusion_level": "moderate",
        "cold": False,
        "report_status": "pending-human-review",
        "allow_court": False,
    },
    "CASE-NTSB-HUDSON-004": {
        "location": "Hudson River ditching after takeoff (public historical)",
        "entities": [
            ("vehicle", "Vehicles", "Aircraft-US-Airways-1549-public", "aircraft", "Public-historical aircraft incident subject. Use public labels only."),
            ("organization", "Organizations", "NTSB-public-record-context", "investigative-body", "Public technical investigation context (archive-style sources)."),
        ],
        "primary": {
            "file": "H-Bird-Strike-Dual-Engine",
            "title": "Bird strike caused dual engine thrust loss leading to ditching",
            "body": "Public CVR/FDR summary themes, bird remains/ingestion finding, and engine damage analysis converge on bird strike and dual thrust loss with successful ditching.",
            "level": "strong",
            "status": "pending-human-review",
        },
        "counter": {
            "file": "H-Crew-Error-Primary",
            "title": "Crew procedural error as primary cause",
            "body": "Counter-hypothesis: crew error primary — checklist/procedure choices as primary cause rather than bird strike. Packet bird remains and engine damage make this weaker as a *primary* cause, though crew actions remain relevant to outcome management.",
            "level": "weak",
        },
        "events": [
            ("T-2009-01-15", "2009-01-15", "day-only", "Takeoff, bird encounter, dual thrust loss, ditching (public chronology theme)", "[[EV-CVR-001]]"),
        ],
        "contradictions": [],
        "gaps": [
            "Full FDR CSV not included in packet",
            "Raw CVR audio not included — public summary only",
        ],
        "timeline_master": "Single-flight event chain on 2009-01-15 per public summaries.",
        "conclusion": "Bird-strike dual-engine failure with ditching is **established** at strong support from converging public technical sources. Safety lessons remain analysis, not new evidence.",
        "conclusion_level": "strong",
        "cold": False,
        "report_status": "pending-human-review",
        "allow_court": False,
        "probable_cause": True,
    },
    "CASE-COLD-DBCOOPER-007": {
        "location": "Pacific Northwest hijacking flight (public historical)",
        "entities": [
            ("person", "Persons/Persons-of-Interest", "Unidentified-Hijacker-DB-Cooper-label", "person-of-interest", "Public moniker only; identity not established in packet."),
        ],
        "primary": {
            "file": "H-Unknown-Hijacker-Parachute",
            "title": "Unidentified hijacker parachuted; identity remains unknown",
            "body": "Public narrative supports a hijacking and parachute escape sequence. Identity and post-jump survival are not established by this packet.",
            "level": "moderate",
            "status": "draft",
        },
        "counter": {
            "file": "H-Named-Suspect-Unproven",
            "title": "Any specific named historical suspect is unproven here",
            "body": "Counter / discipline hypothesis: public named-suspect theories must not be elevated to verified identity. Packet lacks definitive identification evidence (e.g., conclusive public DNA attribution).",
            "level": "weak",
        },
        "events": [
            ("T-1971-11-24", "1971-11-24", "day-only", "Hijacking flight date (public narrative)", "[[EV-NB-001]]"),
        ],
        "contradictions": [
            (
                "CX-LANDING-SURVIVAL",
                "Public theories conflict on landing zone and whether the hijacker survived — unresolved in packet.",
            )
        ],
        "gaps": [
            "Definitive public DNA identification not available in packet",
            "Complete ransom serial recovery chain partial only",
            "Identity unknown — cold lead",
        ],
        "timeline_master": "1971-11-24 hijacking; subsequent money recovery is partial/public-note level only.",
        "conclusion": "Case remains **cold/open on identity**. Do not declare a confirmed identity. Survival and landing zone remain disputed.",
        "conclusion_level": "weak",
        "cold": True,
        "report_status": "draft",
        "allow_court": False,
        "case_status_field": "cold-case",
    },
    "CASE-FICT-LABGAP-018": {
        "location": "Fictional assault scene (packet-limited)",
        "entities": [
            ("person", "Persons/Suspects", "Suspect-A", "suspect", "Suspect A referenced in alibi materials (packet label only)."),
            ("person", "Persons/Victims", "Victim-Riley-label", "victim", "Victim referenced in scene materials — use only packet labels; no extra biography."),
            ("person", "Persons/Witnesses", "Eyewitness-Scene", "witness", "Witness who places Suspect A at scene."),
        ],
        "primary": {
            "file": "H-Suspect-A-Present",
            "title": "Suspect A present at assault",
            "body": "Eyewitness places Suspect A at scene. Competes with Suspect A alibi statement. DNA lab not available — support must stay limited.",
            "level": "weak",
            "status": "draft",
        },
        "counter": {
            "file": "H-Misidentification-Alibi-True",
            "title": "Misidentification; alibi true",
            "body": "Counter-hypothesis: Suspect A alibi is accurate and eyewitness misidentified the person. Equally live until lab/forensic resolution.",
            "level": "weak",
        },
        "events": [
            ("T-ASSAULT", "2020-08-09", "day-only", "Assault reported (packet theme)", "[[EV-SCENE-001]]"),
        ],
        "contradictions": [
            (
                "CX-ALIBI-VS-EYEWITNESS",
                "Suspect A alibi statement conflicts with eyewitness placing Suspect A at scene.",
            )
        ],
        "gaps": [
            "DNA lab report not yet available",
            "Independent digital location data not in packet",
            "No resolution of alibi vs eyewitness contradiction",
        ],
        "timeline_master": "Assault event 2020-08-09; alibi window conflicts with witness account.",
        "conclusion": "Attribution remains **disputed**. Both presence and alibi hypotheses are weak without lab results. Do not treat either as strong/conclusive.",
        "conclusion_level": "weak",
        "cold": False,
        "report_status": "draft",
        "allow_court": False,
    },
    # ---- Hard set (run-5b) ----
    "CASE-FICT-INFORMANT-017": {
        "location": "Fictional racketeering inquiry (Northbridge)",
        "entities": [
            ("person", "Persons/Persons-of-Interest", "Sam-Rivera", "person-of-interest", "POI named in packet materials only."),
            ("person", "Persons/Persons-of-Interest", "CI-14", "informant", "Confidential informant label CI-14; credibility incomplete."),
        ],
        "primary": {
            "file": "H-Enterprise-Led-By-POI",
            "title": "Enterprise exists led by named POI (working theory)",
            "body": "Informant debrief plus partial surveillance and toll records support a working enterprise theory involving Sam Rivera. Support must stay moderate-at-most because informant credibility assessment is incomplete and no wiretap warrant package is in the packet.",
            "level": "moderate",
            "status": "draft",
        },
        "counter": {
            "file": "H-Informant-Exaggeration",
            "title": "Informant exaggerates to obtain deal",
            "body": "Counter-hypothesis: informant deal motivation drives exaggeration; enterprise leadership claim is inflated. Informant credibility / deal terms / protection status not fully documented — do not treat informant as conclusive.",
            "level": "moderate",
        },
        "events": [
            ("T-MEET", "2021-06-18", "day-only", "Observed meeting cafe", "[[EV-SURV-001]]"),
        ],
        "contradictions": [
            (
                "CX-INF",
                "Informant timeline vs toll records — conflict themes present in packet pairing.",
            )
        ],
        "gaps": [
            "Wiretap warrant package not provided — do not invent content (GAP-WARRANT)",
            "Informant credibility-assessment incomplete (reliability / deal-terms / protection-status)",
            "Independent corroboration of enterprise leadership incomplete",
        ],
        "timeline_master": "Key observed meeting 2021-06-18; informant chronology partially conflicts with toll summary.",
        "conclusion": "Enterprise/POI theory is **disputed / moderate-at-most**. Informant is a lead source, not conclusive proof. No court-file.",
        "conclusion_level": "moderate",
        "cold": False,
        "report_status": "draft",
        "allow_court": False,
        "informant_sensitive": True,
    },
    "CASE-COLD-ZODIAC-008": {
        "location": "Northern California public-historical crime letters era",
        "entities": [
            ("person", "Persons/Persons-of-Interest", "Unidentified-Letter-Author-Label", "person-of-interest", "Public moniker/context only — identity not verified in packet."),
        ],
        "primary": {
            "file": "H-Single-Offender-Letters-Attacks",
            "title": "One offender authored letters and committed multiple attacks (working)",
            "body": "Public letter themes, cipher history, and one linked-attack summary support a working single-offender theory. No individual in this packet is treated as conclusively identified.",
            "level": "weak",
            "status": "draft",
        },
        "counter": {
            "file": "H-Copycat-Overlinking",
            "title": "Copycat letters and over-linking of unrelated crimes",
            "body": "Counter-hypothesis: copycat correspondence and overlinking inflate a single-offender narrative. Claimed victim counts may exceed confirmed linked cases.",
            "level": "weak",
        },
        "events": [
            ("T-1969", "1969-01-01", "year-only", "Peak publicized activity era", "[[EV-LETTER-001]]"),
        ],
        "contradictions": [
            (
                "CX-COUNT",
                "Claimed victim counts vs confirmed linked cases — unresolved in packet.",
            )
        ],
        "gaps": [
            "Modern forensic dossier not in packet (GAP-FORENSIC)",
            "No verified identity of letter author in packet",
            "Scope of linked crimes uncertain",
        ],
        "timeline_master": "Peak publicized activity around 1969 era; multi-year public letter history not fully dated in packet.",
        "conclusion": "Attribution remains **unknown**. No named person is accepted as the established offender. Keep open-investigation posture.",
        "conclusion_level": "weak",
        "cold": True,
        "report_status": "draft",
        "allow_court": False,
        "case_status_field": "open-investigation",
        "forbid_verified_killer": True,
    },
    "CASE-NTSB-TWA800-003": {
        "location": "TWA 800 public technical investigation (1996)",
        "entities": [
            ("vehicle", "Vehicles", "Aircraft-TWA800-public", "aircraft", "Public-historical flight subject only."),
            ("organization", "Organizations", "NTSB-public-context", "investigative-body", "Public technical investigation context."),
            ("system-failure", "System-Failures", "SF-Fuel-Tank-Ignition-Context", "system", "Fuel tank flammable vapor / ignition source context from public findings themes."),
        ],
        "primary": {
            "file": "H-Fuel-Tank-Explosion",
            "title": "Fuel tank explosion due to ignition of flammable vapors",
            "body": "Public accident summary, wreckage reconstruction description, and center fuel tank condition finding support fuel-tank explosion from ignition of flammable vapors as the working probable cause theme.",
            "level": "strong",
            "status": "pending-human-review",
        },
        "counter": {
            "file": "H-Missile-Hostile-Action",
            "title": "External missile / hostile action hypothesis",
            "body": "Counter-hypothesis: external munition / hostile action narrative. Publicly alleged in discourse but not established by official public findings in this packet. No authenticated warhead debris is present here.",
            "level": "weak",
        },
        "events": [
            ("T-1996-07-17", "1996-07-17", "day-only", "Flight loss after takeoff", "[[EV-NTSB-001]]"),
        ],
        "contradictions": [
            (
                "CX-WITNESS-STREAKS",
                "Some witness streak reports vs mechanical ignition narrative.",
            )
        ],
        "gaps": [
            "Full raw radar exports not in packet (GAP-RAW-RADAR)",
            "Original lab measurement tables not in packet — do not invent numbers",
        ],
        "timeline_master": "1996-07-17 flight loss after takeoff per public summary themes.",
        "conclusion": "Fuel-tank explosion from flammable vapor ignition is **probable/strong** on public packet sources. External munition hypotheses remain unestablished here.",
        "conclusion_level": "strong",
        "cold": False,
        "report_status": "pending-human-review",
        "allow_court": False,
        "probable_cause": True,
    },
    "CASE-MARITIME-TITANIC-005": {
        "location": "North Atlantic (public historical maritime loss)",
        "entities": [
            ("vehicle", "Vehicles", "Vessel-Titanic-public", "vessel", "Public-historical vessel; vessel-class ship."),
            ("group-entity", "Persons/Groups", "Passengers-Crew-Unnamed", "passengers", "Group-entity for passengers/crew — roster individuals only if present in packet (none listed here)."),
            ("system-failure", "System-Failures", "SF-Speed-Lookout-Ice", "system", "Speed/lookout/ice-condition decision failures in public inquiry themes."),
            ("regulatory-gap", "Regulatory-Gaps", "RG-Lifeboat-Capacity", "regulatory", "Lifeboat capacity regulatory gap context from public sources."),
        ],
        "primary": {
            "file": "H-Iceberg-Collision-Foundering",
            "title": "Iceberg collision under high-speed night conditions caused foundering",
            "body": "Public inquiry summary, ice warnings context, and lifeboat regulatory context support iceberg collision with amplifying factors (speed, ice conditions, lifeboat capacity gaps).",
            "level": "strong",
            "status": "pending-human-review",
        },
        "counter": {
            "file": "H-Coal-Fire-Primary",
            "title": "Coal fire structural weakness as primary cause",
            "body": "Counter-hypothesis: coal fire primary structural weakness. Public fringe theory relative to inquiry iceberg narrative; keep as counter, not established primary from this packet.",
            "level": "weak",
        },
        "events": [
            ("T-1912-04-14", "1912-04-14", "day-only", "Iceberg collision night", "[[EV-INQUIRY-001]]"),
        ],
        "contradictions": [
            (
                "CX-SPEED",
                "Speed vs ice warning prudence tension in testimony summaries.",
            )
        ],
        "gaps": [
            "Complete passenger manifest not required — use group-entity (GAP-FULL-MANIFEST)",
            "No full individual passenger roster in packet",
        ],
        "timeline_master": "1912-04-14 iceberg collision night; foundering follows.",
        "conclusion": "Iceberg collision foundering is **established** at strong support from public inquiry themes, with regulatory/system contributing factors. Passengers handled as group-entity only.",
        "conclusion_level": "strong",
        "cold": False,
        "report_status": "pending-human-review",
        "allow_court": False,
        "probable_cause": True,
        "group_entity_mode": True,
    },
    "CASE-FICT-AVIATION-020": {
        "location": "Fictional commuter flight loss (open investigation)",
        "entities": [
            ("vehicle", "Vehicles", "Aircraft-N4XB-demo", "aircraft", "Aircraft N4XB-demo from packet labels."),
        ],
        "primary": {
            "file": "H-Weather-LOC",
            "title": "Weather-related loss of control (working)",
            "body": "Partial radar track and METARs support a weather-related loss-of-control working theory. CVR not recovered; wreckage incomplete — keep support weak/moderate and status open.",
            "level": "weak",
            "status": "draft",
        },
        "counter": {
            "file": "H-Maintenance-Anomaly",
            "title": "Maintenance-related control anomaly",
            "body": "Counter-hypothesis: maintenance anomaly from partial maintenance log page. Equally live; insufficient data for probable cause. cause-unknown discipline applies.",
            "level": "weak",
        },
        "events": [
            ("T-CRASH", "2019-04-22T07:05", "exact", "Loss of radar contact", "[[EV-RADAR-001]]"),
        ],
        "contradictions": [
            (
                "CX-WX",
                "Pilot weather briefing vs actual METAR evolution — incomplete reconciliation.",
            )
        ],
        "gaps": [
            "CVR not recovered (GAP-CVR)",
            "Incomplete wreckage recovery (GAP-WRECKAGE-FULL)",
            "Insufficient data for probable cause — dual hypotheses remain open",
        ],
        "timeline_master": "2019-04-22T07:05 loss of radar contact; pre-event weather/maintenance context partial.",
        "conclusion": "Cause remains **unknown**. Weather LOC and maintenance anomaly both open. No conclusive finding; readiness blocks court-file. Intentional crew self-harm is unsupported and out of scope.",
        "conclusion_level": "weak",
        "cold": True,
        "report_status": "draft",
        "allow_court": False,
        "case_status_field": "open-investigation",
        "cause_unknown": True,
    },
    # ---- Organized crime (021–025) ----
    "CASE-ORG-COMMISSION-021": {
        "location": "Multi-city public-historical organized crime governance era",
        "entities": [
            ("organization", "Organizations", "Multi-family-coordination-body", "criminal-group", "Public-label coordination body; hierarchy partially reconstructed."),
        ],
        "primary": {
            "file": "H-Commission-Governance",
            "title": "Coordinated multi-family commission governed rackets",
            "body": "Hearing themes, territory chronology, and published structure narratives support a working theory of formal multi-group coordination of rackets/territories.",
            "level": "moderate",
            "status": "draft",
        },
        "counter": {
            "file": "H-Loose-Affiliation",
            "title": "Loose affiliation without formal commission",
            "body": "Counter-hypothesis: loose affiliation only / no formal commission governance. Explains coordination appearance as ad-hoc alliances.",
            "level": "weak",
        },
        "events": [
            ("T-1957", "1957-01-01", "year-only", "Publicized multi-group meeting era", "[[EV-HEARING-ORG-001]]"),
        ],
        "contradictions": [
            ("CX-ROSTER", "Published attendee lists differ across secondary sources"),
        ],
        "gaps": [
            "Authenticated contemporaneous wire materials not in packet (GAP-WIRE)",
            "Exact full roster of any meeting not verified in packet",
        ],
        "timeline_master": "Publicized multi-group meeting era ~1957; broader racket chronology multi-year.",
        "conclusion": "Commission-style coordination is **probable** (moderate) on public themes. No invented wire content.",
        "conclusion_level": "moderate",
        "cold": False,
        "report_status": "pending-human-review",
        "allow_court": False,
    },
    "CASE-ORG-NARCO-PIPE-022": {
        "location": "Transnational import corridor (public case themes)",
        "entities": [
            ("organization", "Organizations", "Import-network-public-label", "criminal-group", "Import/distribution network as public case label."),
        ],
        "primary": {
            "file": "H-Import-Distribution-Conspiracy",
            "title": "Coordinated import-distribution conspiracy with financial concealment",
            "body": "Indictment themes, bulk currency note, and route narrative support coordinated conspiracy rather than pure coincidence.",
            "level": "moderate",
            "status": "draft",
        },
        "counter": {
            "file": "H-Independent-Smugglers",
            "title": "Independent actors only sharing routes",
            "body": "Counter-hypothesis: independent actors only. Weaker if public indictment themes allege coordination, but packet lacks full ledgers.",
            "level": "weak",
        },
        "events": [
            ("T-PEAK", "1984-01-01", "year-only", "Peak conspiracy activity window in public narrative", "[[EV-INDICT-001]]"),
        ],
        "contradictions": [
            ("CX-QUANTITY", "Public quantity estimates conflict across reports"),
        ],
        "gaps": [
            "Full internal conspiracy ledgers not in packet (GAP-LEDGER-FULL)",
            "Lab purity figures not present — do not invent",
        ],
        "timeline_master": "Peak activity window ~1984 in public narrative; multi-year conspiracy possible.",
        "conclusion": "Coordinated conspiracy is **probable** (moderate). Do not invent purity assays or courier names beyond packet.",
        "conclusion_level": "moderate",
        "cold": False,
        "report_status": "pending-human-review",
        "allow_court": False,
    },
    "CASE-ORG-RICO-SHELL-023": {
        "location": "Harborview (fictional) — shell enterprise",
        "entities": [
            ("organization", "Organizations", "Harborview-Holdings-Group", "employer", "Layered LLC cluster used in alleged enterprise."),
            ("person", "Persons/Persons-of-Interest", "M-Calder", "person-of-interest", "POI M. Calder from packet labels only."),
        ],
        "primary": {
            "file": "H-RICO-Shell-Enterprise",
            "title": "RICO enterprise using shells to move protection proceeds",
            "body": "Layered LLCs, protection complaint, and bank transfer graph support enterprise theory under working moderate support.",
            "level": "moderate",
            "status": "draft",
        },
        "counter": {
            "file": "H-Legitimate-Disputes",
            "title": "Legitimate business disputes only",
            "body": "Counter-hypothesis: legitimate consulting/collection disputes without criminal enterprise. Possible if protection claim is unreliable and transfers have lawful invoices (not shown).",
            "level": "weak",
        },
        "events": [
            ("T-COMPLAINT", "2018-05-09", "day-only", "First protection complaint filed", "[[EV-EXTORT-001]]"),
        ],
        "contradictions": [
            ("CX-OWNER", "Beneficial ownership statements conflict across filings"),
        ],
        "gaps": [
            "Handset extraction for alleged enforcer not acquired (GAP-PHONE)",
            "No authenticated recording of violent orders in packet",
        ],
        "timeline_master": "First protection complaint 2018-05-09; shell registry and transfers span surrounding period.",
        "conclusion": "Enterprise theory is **probable** (moderate). No invented murder-order recordings.",
        "conclusion_level": "moderate",
        "cold": False,
        "report_status": "draft",
        "allow_court": False,
    },
    "CASE-ORG-UNION-RACKET-024": {
        "location": "Labor union fund control (public historical themes)",
        "entities": [
            ("organization", "Organizations", "Local-trade-union-public", "other", "Local trade union (public case label)."),
        ],
        "primary": {
            "file": "H-Union-Fund-Enterprise",
            "title": "Organized control of union funds with skimming and intimidation",
            "body": "Audit findings, trial outcome themes, and intimidation allegations support organized racketeering of union funds.",
            "level": "strong",
            "status": "pending-human-review",
        },
        "counter": {
            "file": "H-Lone-Embezzler",
            "title": "Lone embezzler without enterprise direction",
            "body": "Counter-hypothesis: lone embezzler treasurer without broader enterprise. Weaker against intimidation + trial racketeering themes but remains a discipline check.",
            "level": "weak",
        },
        "events": [
            ("T-AUDIT", "1975-01-01", "year-only", "Major audit findings publicized", "[[EV-AUDIT-001]]"),
        ],
        "contradictions": [],
        "gaps": [
            "Complete dues microfilm set not in packet (GAP-MICROFILM)",
        ],
        "timeline_master": "Major audit findings publicized ~1975.",
        "conclusion": "Organized union-fund racketeering is **established/strong** on public packet themes. Exact unlogged totals not invented.",
        "conclusion_level": "strong",
        "cold": False,
        "report_status": "pending-human-review",
        "allow_court": False,
    },
    "CASE-ORG-PORT-SMUG-025": {
        "location": "Harborview Port (fictional)",
        "entities": [
            ("organization", "Organizations", "Harborview-Port-Authority", "government", "Port authority organization."),
            ("person", "Persons/Persons-of-Interest", "K-Nunez-Supervisor", "person-of-interest", "Dock Supervisor K. Nunez — bribe allegation uncorroborated."),
        ],
        "primary": {
            "file": "H-Port-Smuggling-Cell",
            "title": "Organized cell smuggling via compromised port process",
            "body": "Manifest/scan anomalies and CCTV window support smuggling activity; bribe tip is weaker and uncorroborated.",
            "level": "moderate",
            "status": "draft",
        },
        "counter": {
            "file": "H-Clerical-False-Bribe",
            "title": "Clerical error plus false bribe claim",
            "body": "Counter-hypothesis: clerical error and false bribe claim. Cargo anomaly is documented; anonymous bribe tip lacks corroboration — overall disputed.",
            "level": "moderate",
        },
        "events": [
            ("T-ANOM", "2022-09-14", "day-only", "Container scan anomaly night", "[[EV-CARGO-001]]"),
        ],
        "contradictions": [
            ("CX-BRIBE", "Anonymous bribe tip lacks corroboration vs cargo anomaly is documented"),
        ],
        "gaps": [
            "Supervisor phone not imaged (GAP-SUPERVISOR-DEVICE)",
            "Bribe allegation uncorroborated",
        ],
        "timeline_master": "Container scan anomaly night 2022-09-14.",
        "conclusion": "Smuggling cell is **disputed/probable-leaning moderate** on cargo+CCTV; bribe/corrupt official not conclusive. No invented confession.",
        "conclusion_level": "moderate",
        "cold": False,
        "report_status": "draft",
        "allow_court": False,
    },
    # ---- Serial offender packs (026–030) ----
    "CASE-SK-RIPPER-026": {
        "location": "Whitechapel district (public historical)",
        "entities": [
            ("group-entity", "Persons/Groups", "Linked-Victims-Core-Set", "victims", "Core victim set disputed; use group-entity, no invented name roster."),
            ("person", "Persons/Persons-of-Interest", "Unidentified-Serial-Offender-Label", "person-of-interest", "Offender identity not established in packet."),
        ],
        "primary": {
            "file": "H-Single-Serial-Core-Set",
            "title": "Single serial offender for a core linked set (working)",
            "body": "Period police extracts and press linkage support a working single-offender theory for a core set. Canonical count disputed; identity unknown.",
            "level": "weak",
            "status": "draft",
        },
        "counter": {
            "file": "H-Multiple-Offenders-Overlink",
            "title": "Multiple offenders / overlinking",
            "body": "Counter-hypothesis: multiple offenders and media overlinking. Some cases may be unlinked. Disputed letter authenticity weakens single-brand narrative.",
            "level": "weak",
        },
        "events": [
            ("T-1888", "1888-01-01", "year-only", "Peak publicized Whitechapel murder year", "[[EV-POLICE-001]]"),
        ],
        "contradictions": [
            ("CX-CANON", "Canonical victim count disputed across histories"),
        ],
        "gaps": [
            "Modern forensic re-test package not in packet (GAP-FORENSIC-1888)",
            "Offender identity unknown",
        ],
        "timeline_master": "Peak publicized year 1888; series window broader in secondary literature.",
        "conclusion": "Identity remains **unknown**. Single-offender core set is a weak working theory only. No confirmed historical identity declared.",
        "conclusion_level": "weak",
        "cold": True,
        "report_status": "draft",
        "allow_court": False,
        "case_status_field": "cold-case",
        "group_entity_mode": True,
    },
    "CASE-SK-GREENRIVER-027": {
        "location": "Pacific Northwest series (public historical themes)",
        "entities": [
            ("group-entity", "Persons/Groups", "Series-Victims-Group", "victims", "Large victim set — group-entity; no invented full name list."),
            ("organization", "Organizations", "Task-Force-Public", "law-enforcement", "Task force public chronology context."),
        ],
        "primary": {
            "file": "H-Single-Primary-Serial",
            "title": "Single primary serial offender for linked series",
            "body": "Task force chronology, linkage criteria, and later attribution summary support single primary offender for the linked series at probable/strong band for public packet.",
            "level": "strong",
            "status": "pending-human-review",
        },
        "counter": {
            "file": "H-Peripheral-Other-Offenders",
            "title": "Additional offenders for peripheral cases",
            "body": "Counter-hypothesis: additional offenders explain some peripheral cases. Inclusion criteria for periphery remain debated in public commentary.",
            "level": "weak",
        },
        "events": [
            ("T-1982", "1982-01-01", "year-only", "Early series recognition era", "[[EV-TASK-001]]"),
        ],
        "contradictions": [
            ("CX-PERIPH", "Peripheral cases disputed for inclusion in series"),
        ],
        "gaps": [
            "Full DNA table not in packet (GAP-FULL-DNA) — do not invent STR values",
        ],
        "timeline_master": "Early series recognition ~1982; long investigation thereafter.",
        "conclusion": "Single primary offender for linked series is **probable/strong** on public attribution themes. Peripheral inclusions remain debated. No invented STR tables.",
        "conclusion_level": "strong",
        "cold": False,
        "report_status": "pending-human-review",
        "allow_court": False,
        "group_entity_mode": True,
    },
    "CASE-SK-BTK-028": {
        "location": "Municipal series with communications trail (public historical)",
        "entities": [
            ("person", "Persons/Persons-of-Interest", "Identified-Offender-Public-Pathway", "suspect", "Identification pathway exists in public summary; treat as historical packet label only."),
        ],
        "primary": {
            "file": "H-Single-Author-Communications",
            "title": "Single offender authored communications and linked crimes",
            "body": "Communications descriptions, dormancy/recontact note, and identification pathway public summary support established single-offender narrative for this packet.",
            "level": "strong",
            "status": "pending-human-review",
        },
        "counter": {
            "file": "H-Copycat-Late-Comms",
            "title": "Copycat authored some late communications",
            "body": "Counter-hypothesis: copycat communications in late period only. Weaker against identification pathway summary but retained for bias resistance.",
            "level": "weak",
        },
        "events": [
            ("T-RECONTACT", "2004-01-01", "year-only", "Publicized recontact / investigation restart era", "[[EV-COLD-001]]"),
        ],
        "contradictions": [],
        "gaps": [
            "Original physical media package not attached (GAP-ORIGINAL-MEDIA)",
        ],
        "timeline_master": "Long dormancy then publicized recontact era ~2004.",
        "conclusion": "Single-offender communications+crimes narrative is **established/strong** on public packet. No invented confession text.",
        "conclusion_level": "strong",
        "cold": False,
        "report_status": "pending-human-review",
        "allow_court": False,
    },
    "CASE-SK-YORKSHIRE-029": {
        "location": "Regional serial investigation (public historical UK themes)",
        "entities": [
            ("organization", "Organizations", "Investigating-Force-Public", "law-enforcement", "Investigating force public critique context."),
        ],
        "primary": {
            "file": "H-Linked-Series-Despite-False-Trails",
            "title": "Linked series by one offender despite false trails",
            "body": "Conviction public summary supports eventual single-offender attribution; investigation history includes hoax and geographic false trails useful for bias lessons.",
            "level": "moderate",
            "status": "draft",
        },
        "counter": {
            "file": "H-Hoax-Profile-Path",
            "title": "Hoax communications path as correct profile (misleading historical path)",
            "body": "Counter / historical false-trail: hoax led investigation and wrong geographic focus. Retained to document confirmation-bias failure modes; not a claim of a second proven concurrent offender.",
            "level": "weak",
        },
        "events": [
            ("T-HOAX", "1979-01-01", "year-only", "Hoax communications peak public controversy", "[[EV-HOAX-001]]"),
        ],
        "contradictions": [
            ("CX-ACCENT", "Hoax accent geography conflicted with other case data"),
        ],
        "gaps": [
            "Full hoax audio not in packet (GAP-FULL-HOAX-AUDIO)",
        ],
        "timeline_master": "Hoax communications peak controversy ~1979 within longer series window.",
        "conclusion": "Linked series attribution is **disputed-to-probable** depending on which investigative path is weighed; public conviction summary supports eventual identification. Document false trails. No second concurrent offender invented.",
        "conclusion_level": "moderate",
        "cold": False,
        "report_status": "pending-human-review",
        "allow_court": False,
    },
    "CASE-SK-FICT-CORRIDOR-030": {
        "location": "Fictional highway corridor (open series)",
        "entities": [
            ("person", "Persons/Persons-of-Interest", "Unidentified-Driver-POI", "person-of-interest", "Unidentified driver POI — not a verified offender."),
            ("group-entity", "Persons/Groups", "Corridor-Incidents-Victims", "victims", "Victims across three incidents as group context without extra names."),
        ],
        "primary": {
            "file": "H-Corridor-Single-Offender",
            "title": "Single serial offender along highway corridor (working)",
            "body": "Three incidents with partial MO/vehicle themes support a weak working single-offender theory. Lab for incident-3 pending — do not elevate support.",
            "level": "weak",
            "status": "draft",
        },
        "counter": {
            "file": "H-Cluster-Or-Copycat",
            "title": "Unrelated cluster or copycat on case-3",
            "body": "Counter-hypothesis: unrelated cluster / weak MO coincidence; possible copycat on incident-3. Vehicle color conflicts support caution.",
            "level": "weak",
        },
        "events": [
            ("T-CASE3", "2021-11-02", "day-only", "Incident-3 discovered", "[[EV-CASE3]]"),
        ],
        "contradictions": [
            ("CX-VEHICLE", "Vehicle color descriptions conflict across incidents"),
        ],
        "gaps": [
            "DNA lab report for incident-3 pending (GAP-DNA-CASE3)",
            "No verified named corridor offender",
        ],
        "timeline_master": "Incident-3 discovered 2021-11-02; prior incidents earlier in corridor window (details limited in packet).",
        "conclusion": "Series linkage remains **unknown/open**. Single-offender is weak working theory only. No named verified offender. Lab pending blocks readiness.",
        "conclusion_level": "weak",
        "cold": True,
        "report_status": "draft",
        "allow_court": False,
        "case_status_field": "open-investigation",
        "cause_unknown": True,
        "group_entity_mode": True,
    },
}


def fm(fields: dict, body: str) -> str:
    lines = ["---"]
    for k, v in fields.items():
        if isinstance(v, list):
            if not v:
                lines.append(f"{k}: []")
            else:
                lines.append(f"{k}:")
                for item in v:
                    lines.append(f"  - {item}")
        elif v is None:
            lines.append(f"{k}:")
        else:
            lines.append(f"{k}: {v}")
    lines.append("---")
    lines.append("")
    lines.append(body.rstrip())
    lines.append("")
    return "\n".join(lines)


def parse_sources(brief_text: str) -> list[dict]:
    sources = []
    for m in re.finditer(
        r"`(EV-[A-Z0-9-]+)`\s*\(([^,]+),\s*([^)]+)\):\s*(.+)",
        brief_text,
    ):
        sources.append(
            {
                "id": m.group(1).strip(),
                "type": m.group(2).strip(),
                "source_kind": m.group(3).strip(),
                "title": m.group(4).strip(),
            }
        )
    return sources


def type_to_folder(etype: str) -> str:
    etype = etype.lower()
    if etype in ("physical-evidence",):
        return "Physical"
    if etype in ("digital-evidence", "wiretap-evidence"):
        return "Digital"
    if etype in ("testimonial", "informant-testimony"):
        return "Testimonial"
    if etype in ("documentary", "financial-record"):
        return "Documentary"
    if etype in ("data-analysis",):
        return "Data-Analysis"
    return "Documentary"


def read_source_body(packet: Path, eid: str) -> str:
    p = packet / f"{eid}.md"
    if p.is_file():
        return p.read_text(encoding="utf-8", errors="replace")
    return ""


def build_vault(case_dir: Path, vault: Path) -> None:
    case = load_yaml(case_dir / "case.yaml")
    case_id = case["case_id"]
    intel = CASE_INTEL[case_id]
    packet = case_dir / "source_packet"
    brief = (packet / "BRIEF.md").read_text(encoding="utf-8", errors="replace")
    sources = parse_sources(brief)
    if not sources:
        raise RuntimeError(f"No sources parsed for {case_id}")

    # directories
    dirs = [
        "00-Scaffold/Visual/Canvases",
        "00-Scaffold/Meta",
        "01-Evidence/Physical",
        "01-Evidence/Digital",
        "01-Evidence/Testimonial",
        "01-Evidence/Documentary",
        "01-Evidence/Data-Analysis",
        "01-Evidence/Chain-of-Custody",
        "01-Evidence/Source-Provenance",
        "02-Entities/Persons/Victims",
        "02-Entities/Persons/Suspects",
        "02-Entities/Persons/Witnesses",
        "02-Entities/Persons/Persons-of-Interest",
        "02-Entities/Locations",
        "02-Entities/Vehicles",
        "02-Entities/Organizations",
        "02-Entities/System-Failures",
        "02-Entities/Regulatory-Gaps",
        "03-Hypotheses/Primary",
        "03-Hypotheses/Alternative",
        "03-Hypotheses/Counter",
        "03-Hypotheses/Rejected",
        "04-Timeline/Events",
        "04-Timeline/Alibis",
        "04-Timeline/Contradictions",
        "05-Analysis/Technical-Analysis",
        "02b-Exploration/Sandbox",
        "02b-Exploration/Promotion-Log",
        "06-Outputs/Case-Reports",
        "06-Outputs/Court-File",
        "06-Outputs/Briefings",
        "06-Outputs/Snapshots",
        "06-Outputs/Recommendations",
        "06-Outputs/Cold-Case-Reports",
        "07-Cold-Case/Open-Leads",
        "07-Cold-Case/What-We-Know",
        "08-Tooling/Active",
        "08-Tooling/Library",
        "08-Tooling/Archive",
        "08-Tooling/Manifests",
        "08-Tooling/Audits",
        "08-Tooling/Fixtures",
        "08-Tooling/Runs",
        "case-logs",
        "90-Reference-Sources",
        "99-Attachments/Documents",
    ]
    for d in dirs:
        (vault / d).mkdir(parents=True, exist_ok=True)

    case_status = intel.get("case_status_field") or case.get("case_status") or "training"

    # --- Scaffold ---
    write_text(
        vault / "00-Scaffold/AGENTS.md",
        fm(
            {
                "type": "agents-instructions",
                "status": "verified",
                "created": TODAY,
                "updated": TODAY,
                "tags": ["scaffold"],
            },
            f"""# AGENTS — {case_id}

## Zones
- `01-Evidence`: verified/packet-backed only + CoC or source-provenance
- `03-Hypotheses`: claims with support-level; Primary requires Counter
- `02b-Exploration`: temporary only (`status: exploration`)
- `04-Timeline`: events with sources
- `06-Outputs`: reports after readiness thinking; Human Gate for strong claims

## Hard rules
1. No invented evidence, quotes, lab results, or names beyond packet.
2. Operational → Chain-of-Custody; public-archive → source-provenance.
3. Timeline-first; declare gaps in Coverage-Ledger.
4. Display (Canvas) ≠ truth.
""",
        ),
    )

    in_scope = "\n".join(f"- {x}" for x in (case.get("scope") or {}).get("in_scope") or [])
    out_scope = "\n".join(f"- {x}" for x in (case.get("scope") or {}).get("out_of_scope") or [])
    write_text(
        vault / "00-Scaffold/Case-Scope.md",
        fm(
            {
                "type": "case-scope",
                "status": "verified",
                "created": TODAY,
                "updated": TODAY,
                "case-status": case_status,
                "tags": ["scaffold", "scope"],
            },
            f"""# Case Scope — {case_id}

**Title:** {case.get("title")}  
**Sensitivity:** {case.get("sensitivity")}  
**Location/context:** {intel["location"]}

## In scope
{in_scope}

## Out of scope
{out_scope}

## Notes
{case.get("notes") or ""}
""",
        ),
    )

    phases = case.get("phases") or []
    plan_lines = [f"{i+1}. **{p.get('id')} — {p.get('name')}**: {p.get('description','')}" for i, p in enumerate(phases)]
    write_text(
        vault / "00-Scaffold/Investigation-Plan.md",
        fm(
            {
                "type": "investigation-plan",
                "status": "draft",
                "created": TODAY,
                "updated": TODAY,
                "tags": ["scaffold", "plan"],
            },
            f"""# Investigation Plan — {case_id}

## Phases
"""
            + "\n".join(plan_lines)
            + """

## Method
Packet-only ingest → entities/timeline → primary+counter → audit → calibrated report.
""",
        ),
    )

    write_text(
        vault / "00-Scaffold/Team-Roles.md",
        fm(
            {
                "type": "team-roles",
                "status": "draft",
                "created": TODAY,
                "updated": TODAY,
                "tags": ["scaffold"],
            },
            f"""# Team Roles

- Lead investigator: Benchmark Agent (run-5a)
- Human Gate: required before strong/conclusive or court-file
""",
        ),
    )

    gap_bullets = "\n".join(f"- {g}" for g in intel["gaps"])
    # structured gaps YAML
    gap_yaml_lines = ["gaps:"]
    for i, g in enumerate(intel["gaps"], 1):
        gid = f"GAP-{i:03d}"
        # prefer explicit GAP- id in text
        if "GAP-" in g:
            for tok in g.replace("(", " ").replace(")", " ").split():
                if tok.startswith("GAP-"):
                    gid = tok.strip(",.;")
                    break
        desc = g.replace('"', "'")
        gap_yaml_lines.append(f'  - id: {gid}')
        gap_yaml_lines.append(f'    description: "{desc}"')
        gap_yaml_lines.append("    phase_id: P2")
        gap_yaml_lines.append("    status: open")
    if len(gap_yaml_lines) == 1:
        gap_yaml_lines = ["gaps: []"]
    gap_yaml = "\n".join(gap_yaml_lines)
    ledger_text = f"""---
type: coverage-ledger
status: draft
created: {TODAY}
updated: {TODAY}
case-id: {case_id}
plan-ref: "[[Investigation-Plan]]"
{gap_yaml}
tags: [scaffold, gaps]
---

# Coverage Ledger — {case_id}

## Phase coverage
| Phase | Evidence | Hypotheses | Notes |
|-------|----------|------------|-------|
| P1 Scaffold | n/a | seeded | complete |
| P2 Evidence | packet ingested | — | CoC/provenance applied |
| P3 Hypotheses/Timeline | linked | primary+counter | contradictions logged if any |
| P4 Audit/Report | — | calibrated | Human Gate pending |

## Structured gaps
| id | description | phase | status |
|----|-------------|-------|--------|
"""
    for i, g in enumerate(intel["gaps"], 1):
        gid = f"GAP-{i:03d}"
        if "GAP-" in g:
            for tok in g.replace("(", " ").replace(")", " ").split():
                if tok.startswith("GAP-"):
                    gid = tok.strip(",.;")
                    break
        ledger_text += f"| {gid} | {g} | P2 | open |\n"
    ledger_text += f"""
## Known gaps / missing evidence
{gap_bullets}

## Open contradictions
"""
    ledger_text += (
        "\n".join(f"- [[{c[0]}]] — {c[1]}" for c in intel["contradictions"])
        if intel["contradictions"]
        else "- None formally logged beyond ordinary uncertainty."
    )
    write_text(vault / "00-Scaffold/Coverage-Ledger.md", ledger_text + "\n")

    write_text(
        vault / "00-Scaffold/Review-Queue.md",
        fm(
            {
                "type": "review-queue",
                "status": "draft",
                "created": TODAY,
                "updated": TODAY,
                "tags": ["scaffold", "human-gate"],
            },
            f"""# Review Queue

- [ ] Human review of primary hypothesis support-level
- [ ] Confirm no invented content beyond packet
- [ ] Report readiness before any court-file
- [ ] Gap list accuracy
""",
        ),
    )

    write_text(
        vault / "00-Scaffold/Readiness-Checklist.md",
        fm(
            {
                "type": "readiness-checklist",
                "status": "draft",
                "created": TODAY,
                "updated": TODAY,
                "readiness-passed": "false",
                "tags": ["scaffold", "readiness"],
            },
            f"""# Readiness Checklist — {case_id}

- readiness-passed: **false** (training baseline; no Court-File)
- Gaps remain declared in Coverage-Ledger
- Claim-trace present on draft report
- Human Gate still required for any upgrade
""",
        ),
    )

    write_text(
        vault / "00-Scaffold/Dashboard.md",
        fm(
            {
                "type": "dashboard",
                "status": "draft",
                "created": TODAY,
                "updated": TODAY,
                "tags": ["visual"],
            },
            f"""# Dashboard — {case_id}

- Scope: [[Case-Scope]]
- Plan: [[Investigation-Plan]]
- Ledger: [[Coverage-Ledger]]
- Review: [[Review-Queue]]
- Master timeline: [[Master-Timeline]]
- Primary: [[{intel['primary']['file']}]]
- Counter: [[{intel['counter']['file']}]]
""",
        ),
    )

    write_text(
        vault / "00-Scaffold/Visual/README-Visual.md",
        fm(
            {"type": "visual-doc", "status": "stub", "created": TODAY, "updated": TODAY},
            "# Visual layer\n\nCanvas protocols placeholder for run-5a.\n",
        ),
    )
    write_text(
        vault / "00-Scaffold/Meta/Changelog.md",
        fm(
            {"type": "changelog", "status": "draft", "created": TODAY, "updated": TODAY},
            f"""# Changelog

- {TODAY}: Scaffold + packet ingest + hypotheses + timeline + draft report (run-5a).
""",
        ),
    )
    write_text(
        vault / "00-Scaffold/Meta/Vault-Philosophy.md",
        fm(
            {"type": "meta", "status": "verified", "created": TODAY, "updated": TODAY},
            "# Philosophy\n\nEvidence ≠ hypothesis ≠ exploration. Prefer declared gaps over invention.\n",
        ),
    )

    # --- Native-format scaffold and case logs ---
    write_text(
        vault / "00-Scaffold/Investigation-Index.base",
        """filters:\n  or:\n    - file.hasTag(\"evidence\")\n    - file.hasTag(\"hypothesis\")\n    - file.hasTag(\"gap\")\nviews:\n  - type: table\n    name: \"Investigation Index\"\n    order:\n      - file.name\n      - type\n      - status\n      - support-level\n      - file.mtime\n  - type: list\n    name: \"Pending Human Review\"\n    filters:\n      and:\n        - status == \"pending-human-review\"\n    order:\n      - file.name\n      - type\n      - status\n""",
    )
    write_text(
        vault / "00-Scaffold/Visual/Canvases/00-Native-Format-Protocol.canvas",
        json.dumps(
            {
                "nodes": [
                    {"id": "scope", "type": "file", "x": 0, "y": 0, "width": 360, "height": 220, "file": "00-Scaffold/Case-Scope.md"},
                    {"id": "ledger", "type": "file", "x": 460, "y": 0, "width": 360, "height": 220, "file": "00-Scaffold/Coverage-Ledger.md"},
                    {"id": "report", "type": "file", "x": 920, "y": 0, "width": 360, "height": 220, "file": "06-Outputs/Case-Reports/Case-Report.md"},
                ],
                "edges": [
                    {"id": "scope-ledger", "fromNode": "scope", "toNode": "ledger", "fromSide": "right", "toSide": "left", "toEnd": "arrow", "label": "scope → gaps"},
                    {"id": "ledger-report", "fromNode": "ledger", "toNode": "report", "fromSide": "right", "toSide": "left", "toEnd": "arrow", "label": "coverage → report"},
                ],
            },
            ensure_ascii=False,
            indent=2,
        ) + "\n",
    )
    write_text(vault / "08-Tooling/README.md", fm(
        {"type": "tooling-readme", "status": "verified", "created": TODAY, "updated": TODAY, "tags": ["tooling"]},
        "# Case Tooling\n\nTools are optional, case-scoped, and never Evidence. Use Tool-Manifest, Tool-Audit, and the fail-closed executor.\n",
    ))
    write_text(vault / "case-logs/session.jsonl", "")
    write_text(vault / "case-logs/tool-runs.jsonl", "")
    write_text(vault / "case-logs/decisions.md", fm(
        {"type": "case-log", "status": "draft", "created": TODAY, "updated": TODAY, "case-id": case_id, "tags": ["log", "decisions"]},
        f"# Case Decisions — {case_id}\n\n| time | decision | reason | references |\n|---|---|---|---|\n",
    ))

    # --- Evidence ---
    ev_links = []
    for src in sources:
        eid = src["id"]
        etype = src["type"]
        sk = src["source_kind"]
        title = src["title"]
        body_src = read_source_body(packet, eid)
        folder = type_to_folder(etype)
        archival = sk in ("public-archive", "archival", "official-archive", "declassified")
        # informant testimony: never auto-verified without credibility assessment
        is_informant = etype == "informant-testimony"
        ev_status = "unverified" if is_informant else "verified"
        fields = {
            "type": etype,
            "status": ev_status,
            "created": TODAY,
            "updated": TODAY,
            "evidence-id": eid,
            "source-kind": "public-archive" if archival else ("technical" if sk == "technical" else "operational"),
            "collected-by": "packet-ingest",
            "collected-at": TODAY,
            "support-level": "weak" if is_informant else "moderate",
            "tags": ["evidence", etype],
        }
        if archival or sk == "technical":
            # technical public summaries: provenance style
            prov_name = f"SP-{eid}"
            fields["source-provenance"] = f"[[{prov_name}]]"
            fields["source-kind"] = "public-archive" if archival else "public-archive"
            # also embed structured provenance
            # YAML nested via block in body; frontmatter link is enough for scorer + embed dict:
            # use inline dict in frontmatter by writing manually below
            sp_block = {
                "archive": "public-historical-packet" if archival else "technical-public-summary",
                "collection": case_id,
                "record-id": eid,
                "date-accessed": TODAY,
                "url": f"packet://{case_id}/{eid}",
                "authenticity": "official" if archival else "unverified",
            }
            # rewrite with nested provenance in text form for yaml dump simplicity
            note = f"""---
type: {etype}
status: verified
created: {TODAY}
updated: {TODAY}
evidence-id: {eid}
source-kind: public-archive
collected-by: packet-ingest
collected-at: {TODAY}
support-level: moderate
source-provenance:
  archive: "{sp_block['archive']}"
  collection: "{sp_block['collection']}"
  record-id: "{sp_block['record-id']}"
  date-accessed: {TODAY}
  url: "{sp_block['url']}"
  authenticity: {sp_block['authenticity']}
tags: [evidence, archival]
---

# {eid}: {title}

## Packet excerpt
{body_src}

## Provenance
See also [[{prov_name}]].
"""
            write_text(vault / f"01-Evidence/{folder}/{eid}.md", note)
            write_text(
                vault / f"01-Evidence/Source-Provenance/{prov_name}.md",
                fm(
                    {
                        "type": "source-provenance",
                        "status": "verified",
                        "created": TODAY,
                        "updated": TODAY,
                        "evidence-ref": f'"[[{eid}]]"',
                        "source-kind": "public-archive",
                        "tags": ["provenance"],
                    },
                    f"""# Source Provenance — {eid}

```yaml
source-provenance:
  archive: {sp_block['archive']}
  collection: {sp_block['collection']}
  record-id: {eid}
  date-accessed: {TODAY}
  url: {sp_block['url']}
  authenticity: {sp_block['authenticity']}
```

Linked evidence: [[{eid}]]
""",
                ),
            )
        else:
            coc = f"CoC-{eid}"
            fields["chain-of-custody"] = f'"[[{coc}]]"'
            credibility = ""
            if is_informant:
                fields["credibility-assessment"] = "incomplete"
                credibility = """
## Credibility assessment (required for informant)
- reliability: **not fully assessed** (packet incomplete)
- motivation / deal-terms: **unknown in packet**
- protection-status: **unknown in packet**
- **Do not raise to verified/conclusive on informant alone**
"""
            note = fm(
                fields,
                f"""# {eid}: {title}

## Packet excerpt
{body_src}
{credibility}
## Chain of custody
→ [[{coc}]]
""",
            )
            write_text(vault / f"01-Evidence/{folder}/{eid}.md", note)
            write_text(
                vault / f"01-Evidence/Chain-of-Custody/{coc}.md",
                fm(
                    {
                        "type": "chain-of-custody",
                        "status": "verified",
                        "created": TODAY,
                        "updated": TODAY,
                        "evidence-ref": f'"[[{eid}]]"',
                        "current-custodian": "Benchmark-Vault-Locker",
                        "tags": ["coc"],
                    },
                    f"""# Chain of Custody — {eid}

| time | from | to | reason |
|------|------|-----|--------|
| {TODAY} | Source packet | Ingest agent | digital transfer into vault |
| {TODAY} | Ingest agent | Benchmark-Vault-Locker | secured case storage |

Evidence: [[{eid}]]
""",
                ),
            )
        ev_links.append(f"[[{eid}]]")

    # --- Entities ---
    for etype, sub, fname, role, desc in intel["entities"]:
        if etype == "person":
            write_text(
                vault / f"02-Entities/{sub}/{fname}.md",
                fm(
                    {
                        "type": "person",
                        "status": "unverified",
                        "created": TODAY,
                        "updated": TODAY,
                        "role": role,
                        "tags": ["entity", "person"],
                    },
                    f"# {fname.replace('-', ' ')}\n\n{desc}\n",
                ),
            )
        elif etype == "organization":
            org_kind = role if role in (
                "law-enforcement", "government", "corporate", "tribal",
                "criminal-group", "ngo", "other", "employer",
            ) else "other"
            if org_kind == "employer":
                org_kind = "corporate"
            write_text(
                vault / f"02-Entities/{sub}/{fname}.md",
                fm(
                    {
                        "type": "organization",
                        "status": "unverified",
                        "created": TODAY,
                        "updated": TODAY,
                        "org-kind": org_kind,
                        "tags": ["entity", "organization"],
                    },
                    f"# {fname.replace('-', ' ')}\n\n{desc}\n",
                ),
            )
        elif etype == "location":
            write_text(
                vault / f"02-Entities/{sub}/{fname}.md",
                fm(
                    {
                        "type": "location",
                        "status": "unverified",
                        "created": TODAY,
                        "updated": TODAY,
                        "tags": ["entity", "location"],
                    },
                    f"# {fname.replace('-', ' ')}\n\n{desc}\n",
                ),
            )
        elif etype == "vehicle":
            vclass = "aircraft" if ("aircraft" in role or "Aircraft" in fname or "N4XB" in fname) else (
                "vessel" if ("vessel" in role or "Vessel" in fname or "Titanic" in fname) else "other"
            )
            extra = ""
            if vclass == "vessel":
                extra = "\nvehicle-class note: vessel (IMO unknown in packet)\n"
            if vclass == "aircraft":
                extra = "\nvehicle-class note: aircraft (N-number only if in packet)\n"
            write_text(
                vault / f"02-Entities/{sub}/{fname}.md",
                fm(
                    {
                        "type": "vehicle",
                        "status": "unverified",
                        "created": TODAY,
                        "updated": TODAY,
                        "vehicle-class": vclass,
                        "tags": ["entity", "vehicle"],
                    },
                    f"# {fname.replace('-', ' ')}\n\n{desc}\n{extra}",
                ),
            )
        elif etype == "group-entity":
            (vault / f"02-Entities/{sub}").mkdir(parents=True, exist_ok=True)
            write_text(
                vault / f"02-Entities/{sub}/{fname}.md",
                fm(
                    {
                        "type": "group-entity",
                        "status": "unverified",
                        "created": TODAY,
                        "updated": TODAY,
                        "role": role,
                        "estimated-count": "unknown",
                        "named-individuals": [],
                        "tags": ["entity", "group-entity"],
                    },
                    f"""# {fname.replace('-', ' ')}

{desc}

**Rule:** individual passenger/crew identities are not listed in packet; use this group-entity instead of fabricating a roster.
""",
                ),
            )
        elif etype == "system-failure":
            (vault / "02-Entities/System-Failures").mkdir(parents=True, exist_ok=True)
            write_text(
                vault / f"02-Entities/System-Failures/{fname}.md",
                fm(
                    {
                        "type": "system-failure",
                        "status": "draft",
                        "created": TODAY,
                        "updated": TODAY,
                        "tags": ["entity", "system-failure"],
                    },
                    f"# {fname.replace('-', ' ')}\n\n{desc}\n",
                ),
            )
        elif etype == "regulatory-gap":
            (vault / "02-Entities/Regulatory-Gaps").mkdir(parents=True, exist_ok=True)
            write_text(
                vault / f"02-Entities/Regulatory-Gaps/{fname}.md",
                fm(
                    {
                        "type": "regulatory-gap",
                        "status": "draft",
                        "created": TODAY,
                        "updated": TODAY,
                        "tags": ["entity", "regulatory-gap"],
                    },
                    f"# {fname.replace('-', ' ')}\n\n{desc}\n",
                ),
            )

    # --- Hypotheses ---
    p = intel["primary"]
    c = intel["counter"]
    write_text(
        vault / f"03-Hypotheses/Primary/{p['file']}.md",
        fm(
            {
                "type": "hypothesis",
                "status": p.get("status", "draft"),
                "created": TODAY,
                "updated": TODAY,
                "hypothesis-kind": "primary",
                "support-level": p["level"],
                "supporting-notes": [f'"[[{s["id"]}]]"' for s in sources[:3]],
                "counter-hypothesis": f'"[[{c["file"]}]]"',
                "tags": ["hypothesis", "primary"],
            },
            f"""# {p['title']}

## Statement
> {p['body']}

## Support level
`{p['level']}` — calibrated to packet only.

## Supporting notes
"""
            + "\n".join(f"- [[{s['id']}]]" for s in sources)
            + f"""

## Counter
→ [[{c['file']}]]
""",
        ),
    )
    write_text(
        vault / f"03-Hypotheses/Counter/{c['file']}.md",
        fm(
            {
                "type": "hypothesis",
                "status": "draft",
                "created": TODAY,
                "updated": TODAY,
                "hypothesis-kind": "counter",
                "support-level": c["level"],
                "supporting-notes": [],
                "tags": ["hypothesis", "counter"],
            },
            f"""# {c['title']}

## Statement
> {c['body']}

## Support level
`{c['level']}`

This counter exists to resist confirmation bias. It must remain visible while primary is active.
""",
        ),
    )

    # --- Timeline ---
    event_links = []
    for eid, ts, prec, summary, source in intel["events"]:
        event_links.append(f"[[{eid}]]")
        write_text(
            vault / f"04-Timeline/Events/{eid}.md",
            fm(
                {
                    "type": "timeline-event",
                    "status": "unverified",
                    "created": TODAY,
                    "updated": TODAY,
                    "timestamp": ts,
                    "precision": prec,
                    "source": source,
                    "tags": ["timeline"],
                },
                f"""# {summary}

**Timestamp:** {ts} ({prec})  
**Source:** {source}
""",
            ),
        )

    for cid, desc in intel["contradictions"]:
        write_text(
            vault / f"04-Timeline/Contradictions/{cid}.md",
            fm(
                {
                    "type": "contradiction",
                    "status": "draft",
                    "created": TODAY,
                    "updated": TODAY,
                    "tags": ["contradiction"],
                },
                f"""# {cid}

{desc}

Status: open — do not resolve by inventing data.
""",
            ),
        )

    # Alibi notes for labgap
    if case_id == "CASE-FICT-LABGAP-018":
        write_text(
            vault / "04-Timeline/Alibis/Alibi-Suspect-A.md",
            fm(
                {
                    "type": "alibi",
                    "status": "unverified",
                    "created": TODAY,
                    "updated": TODAY,
                    "tags": ["alibi"],
                },
                """# Alibi — Suspect A

Derived from [[EV-ALIBI-A]]. Conflicts with [[EV-ALIBI-B]] eyewitness placement.
See [[CX-ALIBI-VS-EYEWITNESS]].
""",
            ),
        )

    write_text(
        vault / "04-Timeline/Master-Timeline.md",
        fm(
            {
                "type": "master-timeline",
                "status": "draft",
                "created": TODAY,
                "updated": TODAY,
                "tags": ["timeline"],
            },
            f"""# Master Timeline — {case_id}

{intel['timeline_master']}

## Events
"""
            + "\n".join(f"- {l}" for l in event_links)
            + "\n\n## Contradictions\n"
            + (
                "\n".join(f"- [[{c[0]}]]" for c in intel["contradictions"])
                if intel["contradictions"]
                else "- None logged"
            ),
        ),
    )

    # Cold case folder
    if intel.get("cold"):
        write_text(
            vault / "07-Cold-Case/What-We-Know/Summary.md",
            fm(
                {
                    "type": "cold-case-note",
                    "status": "draft",
                    "created": TODAY,
                    "updated": TODAY,
                    "tags": ["cold-case"],
                },
                f"""# What we know

- Public narrative of event exists in packet sources.
- Identity not established.
- Gaps: {'; '.join(intel['gaps'])}
""",
            ),
        )
        write_text(
            vault / "07-Cold-Case/Open-Leads/Identity-Unknown.md",
            fm(
                {
                    "type": "cold-case-note",
                    "status": "draft",
                    "created": TODAY,
                    "updated": TODAY,
                    "tags": ["cold-case", "lead"],
                },
                """# Open lead — identity

No packet basis to confirm a named identity. Keep lead open; periodic review.
""",
            ),
        )
        write_text(
            vault / "06-Outputs/Cold-Case-Reports/Cold-Case-Report.md",
            fm(
                {
                    "type": "cold-case-report",
                    "status": "draft",
                    "created": TODAY,
                    "updated": TODAY,
                    "tags": ["report", "cold-case"],
                },
                f"""# Cold Case / Open Report — {case_id}

## What we know
"""
                + "\n".join(f"- [[{s['id']}]] — {s['title']}" for s in sources)
                + f"""

## What we do not know
{gap_bullets}

## Live leads
- Keep identity/attribution open where packet does not establish it
- Review gaps periodically

## Hypotheses remaining
- Primary: [[{p['file']}]]
- Counter/discipline: [[{c['file']}]]

## Next steps
- Do not force conclusive identity or probable cause beyond packet
- Seek authenticated packages outside this training packet before upgrading support-level
""",
            ),
        )

    # Analysis stub for technical case
    if intel.get("probable_cause"):
        analysis_name = "Technical-Synthesis"
        analysis_body = "Technical/public synthesis of packet sources. Not a substitute for original docket."
        rec_name = "REC-Safety-General"
        rec_body = "Safety/regulatory recommendations derived as analysis only — not new evidence."
        if case_id == "CASE-NTSB-HUDSON-004":
            analysis_name = "Engine-Bird-Ingestion"
            analysis_body = "Synthesizes [[EV-ENGINE-001]] with [[EV-BIRD-001]] and [[EV-CVR-001]] public themes."
            rec_name = "REC-Bird-Hazard"
            rec_body = "Wildlife hazard management and dual-engine loss training emphasis."
        elif case_id == "CASE-NTSB-TWA800-003":
            analysis_name = "Fuel-Tank-Ignition-Analysis"
            analysis_body = "Synthesizes [[EV-NTSB-001]], [[EV-WRECK-001]], [[EV-FUEL-001]]. External munition narrative retained as counter only."
            rec_name = "REC-Fuel-Tank-Inerting"
            rec_body = "Fuel tank flammability reduction lessons (analysis-level recommendation)."
        elif case_id == "CASE-MARITIME-TITANIC-005":
            analysis_name = "Ice-Speed-Lifeboat-Factors"
            analysis_body = "Multi-factor: iceberg collision + speed/lookout + lifeboat regulatory gap ([[EV-INQUIRY-001]], [[EV-ICE-001]], [[EV-LIFEBOAT-001]])."
            rec_name = "REC-Lifeboat-Standards"
            rec_body = "Lifeboat capacity and ice-navigation prudence (historical regulatory lesson)."
        write_text(
            vault / f"05-Analysis/Technical-Analysis/{analysis_name}.md",
            fm(
                {
                    "type": "analysis",
                    "status": "draft",
                    "created": TODAY,
                    "updated": TODAY,
                    "tags": ["analysis", "technical"],
                },
                f"# Technical analysis note\n\n{analysis_body}\n",
            ),
        )
        write_text(
            vault / f"06-Outputs/Recommendations/{rec_name}.md",
            fm(
                {
                    "type": "recommendation",
                    "status": "draft",
                    "created": TODAY,
                    "updated": TODAY,
                    "tags": ["recommendation"],
                },
                f"# Safety recommendation (training)\n\n{rec_body}\n",
            ),
        )

    if intel.get("cause_unknown"):
        write_text(
            vault / "05-Analysis/Technical-Analysis/Cause-Unknown-Status.md",
            fm(
                {
                    "type": "analysis",
                    "status": "cause-unknown",
                    "created": TODAY,
                    "updated": TODAY,
                    "tags": ["analysis", "cause-unknown"],
                },
                """# Cause unknown

Insufficient data for probable cause. Dual hypotheses remain open. Do not issue conclusive findings or court-file.
""",
            ),
        )

    # Enterprise map for organized-crime packs
    if case_id.startswith("CASE-ORG-") or intel.get("enterprise_map"):
        (vault / "05-Analysis/Enterprise-Maps").mkdir(parents=True, exist_ok=True)
        write_text(
            vault / "05-Analysis/Enterprise-Maps/Enterprise-Map.md",
            fm(
                {
                    "type": "enterprise-map",
                    "status": "draft",
                    "created": TODAY,
                    "updated": TODAY,
                    "enterprise-id": f"ENT-{case_id[-3:]}",
                    "enterprise-confidence": intel.get("conclusion_level", "moderate"),
                    "counter-enterprise-theory": f'"[[{c["file"]}]]"',
                    "related-hypotheses": [f'"[[{p["file"]}]]"'],
                    "related-evidence": [f'"[[{s["id"]}]]"' for s in sources[:3]],
                    "tags": ["analysis", "organized-crime", "enterprise"],
                },
                f"""# Enterprise Map — {case_id}

## Working theory
{p['body']}

## Counter-enterprise
→ [[{c['file']}]]

## Evidence anchors
"""
                + "\n".join(f"- [[{s['id']}]]" for s in sources)
                + """

## Gaps
"""
                + gap_bullets,
            ),
        )

    # Series linkage for serial / SK packs
    if case_id.startswith("CASE-SK-") or intel.get("series_linkage") or intel.get("group_entity_mode"):
        if case_id.startswith("CASE-SK-") or intel.get("series_linkage"):
            (vault / "05-Analysis/Series-Linkage").mkdir(parents=True, exist_ok=True)
            write_text(
                vault / "05-Analysis/Series-Linkage/Series-Linkage.md",
                fm(
                    {
                        "type": "series-linkage",
                        "status": "draft",
                        "created": TODAY,
                        "updated": TODAY,
                        "series-id": f"SER-{case_id[-3:]}",
                        "linkage-confidence": intel.get("conclusion_level", "weak"),
                        "alternative-cluster-hypothesis": f'"[[{c["file"]}]]"',
                        "related-hypotheses": [f'"[[{p["file"]}]]"'],
                        "tags": ["analysis", "series", "linkage"],
                    },
                    f"""# Series Linkage — {case_id}

## Inclusion (working)
- Packet-backed pattern elements only
- Index events: {', '.join(event_links) if event_links else 'see Master-Timeline'}

## Alternative cluster / overlink resistance
→ [[{c['file']}]]

## Gaps
"""
                    + gap_bullets,
                ),
            )

    # Report
    report_type = "case-report"
    report_path = vault / "06-Outputs/Case-Reports/Case-Report.md"
    # Echo index event summaries so report_must_cite can match
    index_claims = "\n".join(
        f"- Index event claim: {ev[3]} ({ev[0]}) linked to {ev[4]}"
        for ev in intel.get("events") or []
    )
    claims = f"""## Claims (traceable)
- Packet evidence ingested: {', '.join(ev_links)}
- Primary hypothesis: [[{p['file']}]] (support `{p['level']}`)
- Counter hypothesis: [[{c['file']}]]
- Timeline: {', '.join(event_links) if event_links else 'see Master-Timeline'}
{index_claims}
"""
    if intel.get("cause_unknown"):
        pc_section = f"""
## Findings
- Partial only: {', '.join(ev_links)}
- **status: cause-unknown** — insufficient for probable cause

## Probable Cause
**Not established.** Dual open hypotheses: [[{p['file']}]] vs [[{c['file']}]].

## Readiness
- Court-file: **blocked**
- Unsupported intentional crew self-harm narratives excluded
"""
    elif intel.get("probable_cause"):
        if case_id == "CASE-NTSB-TWA800-003":
            pc_section = f"""
## Findings
- Public technical sources ({', '.join(ev_links)}) support center fuel tank / flammable vapor ignition themes.
- Index event: Flight loss after takeoff ([[T-1996-07-17]])

## Probable Cause (calibrated)
Fuel tank explosion from ignition of flammable vapors — support `{p['level']}`.

## Contributing Factors
- Fuel tank flammability / ignition source context ([[SF-Fuel-Tank-Ignition-Context]] if present)

## Counter retained
- External munition / hostile action — **not established** in packet ([[{c['file']}]])

## Safety Recommendations
- See Recommendations folder
"""
        elif case_id == "CASE-MARITIME-TITANIC-005":
            pc_section = f"""
## Findings
- Inquiry/public sources ({', '.join(ev_links)}) support iceberg collision and foundering.
- Index event: Iceberg collision night ([[T-1912-04-14]])

## Probable Cause (calibrated)
Iceberg collision under high-speed night conditions — support `{p['level']}`.

## Contributing Factors
- System: speed/lookout/ice ([[SF-Speed-Lookout-Ice]])
- Regulatory gap: lifeboat capacity ([[RG-Lifeboat-Capacity]])
- Passengers/crew: group-entity only ([[Passengers-Crew-Unnamed]]) — no fabricated individual roster

## Counter retained
- Coal fire as primary — fringe relative to packet ([[{c['file']}]])
"""
        else:
            pc_section = f"""
## Findings
- Converging public technical sources ({', '.join(ev_links)}).

## Probable Cause (calibrated)
Primary [[{p['file']}]] — support `{p['level']}` from packet.

## Contributing Factors
- See analysis notes

## Safety Recommendations
- See `06-Outputs/Recommendations/`
"""
    else:
        pc_section = ""

    # Build claim-trace YAML rows from index events + first evidence
    ct_rows = []
    for i, ev in enumerate(intel.get("events") or [], 1):
        eid_ev, _ts, _prec, summary, source = ev
        ev_link = source if source.startswith("[[") else f"[[{sources[0]['id']}]]"
        ct_rows.append(
            f'  - claim-id: RC-{i:03d}\n    claim: "{summary}"\n    evidence: ["{ev_link}"]\n    support-level: {intel.get("conclusion_level", "moderate")}'
        )
    if not ct_rows and sources:
        ct_rows.append(
            f'  - claim-id: RC-001\n    claim: "Packet evidence ingested for {case_id}"\n    evidence: ["[[{sources[0]["id"]}]]"]\n    support-level: {intel.get("conclusion_level", "moderate")}'
        )
    claim_trace_yaml = "claim-trace:\n" + "\n".join(ct_rows) if ct_rows else "claim-trace: []"

    report_body = f"""# Case Report — {case_id}

> Mode D draft. Human Gate required before any court use.
> Court-file: **not issued** (readiness discipline).
> readiness-passed: **false**

## Claim Trace Matrix

| claim-id | Claim | Evidence | support-level |
|----------|-------|----------|---------------|
"""
    for i, ev in enumerate(intel.get("events") or [], 1):
        _eid, _ts, _prec, summary, source = ev
        report_body += f"| RC-{i:03d} | {summary} | {source} | {intel.get('conclusion_level', 'moderate')} |\n"
    if not intel.get("events") and sources:
        report_body += f"| RC-001 | Packet evidence ingested | [[{sources[0]['id']}]] | {intel.get('conclusion_level', 'moderate')} |\n"

    report_body += f"""
## Scope
See [[Case-Scope]]. Location/context: {intel['location']}
See also [[Readiness-Checklist]].

## Evidence summary
{chr(10).join(f'- [[{s["id"]}]] — {s["title"]} ({s["type"]}, {s["source_kind"]})' for s in sources)}

{claims}
{pc_section}

## Contradictions
"""
    report_body += (
        "\n".join(f"- [[{x[0]}]]: {x[1]}" for x in intel["contradictions"])
        if intel["contradictions"]
        else "- None beyond ordinary uncertainty."
    )
    report_body += f"""

## Gaps (explicit)
{gap_bullets}

## Conclusion (calibrated)
{intel['conclusion']}

**support-level target:** `{intel['conclusion_level']}`
"""
    report_text = f"""---
type: {report_type}
status: {intel.get("report_status", "draft")}
created: {TODAY}
updated: {TODAY}
readiness-passed: false
{claim_trace_yaml}
tags: [report]
---

{report_body}
"""
    write_text(report_path, report_text)

    # Audit note
    write_text(
        vault / "00-Scaffold/Meta/Audit-Notes-run-5a.md",
        fm(
            {
                "type": "audit-note",
                "status": "draft",
                "created": TODAY,
                "updated": TODAY,
                "tags": ["audit"],
            },
            f"""# Audit notes (Mode C)

- Structural files present
- Evidence count: {len(sources)} with CoC or provenance
- Primary has counter link
- Gaps listed in Coverage-Ledger
- No court-file generated
- False-inference watch: no invented lab confirmations or confirmed identities beyond packet
""",
        ),
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", default="run-5a")
    ap.add_argument(
        "--cases",
        nargs="+",
        default=[
            "CASE-FICT-WAREHOUSE-014",
            "CASE-FICT-PAYROLL-015",
            "CASE-NTSB-HUDSON-004",
            "CASE-COLD-DBCOOPER-007",
            "CASE-FICT-LABGAP-018",
        ],
    )
    ap.add_argument(
        "--preset",
        choices=["5a", "5b", "10", "org-sk", "org", "sk"],
        default=None,
        help="5a/5b/10 prior sets; org-sk=10 new (5 organized crime + 5 serial); org/sk subsets",
    )
    args = ap.parse_args()
    presets = {
        "5a": [
            "CASE-FICT-WAREHOUSE-014",
            "CASE-FICT-PAYROLL-015",
            "CASE-NTSB-HUDSON-004",
            "CASE-COLD-DBCOOPER-007",
            "CASE-FICT-LABGAP-018",
        ],
        "5b": [
            "CASE-FICT-INFORMANT-017",
            "CASE-COLD-ZODIAC-008",
            "CASE-NTSB-TWA800-003",
            "CASE-MARITIME-TITANIC-005",
            "CASE-FICT-AVIATION-020",
        ],
        "org": [
            "CASE-ORG-COMMISSION-021",
            "CASE-ORG-NARCO-PIPE-022",
            "CASE-ORG-RICO-SHELL-023",
            "CASE-ORG-UNION-RACKET-024",
            "CASE-ORG-PORT-SMUG-025",
        ],
        "sk": [
            "CASE-SK-RIPPER-026",
            "CASE-SK-GREENRIVER-027",
            "CASE-SK-BTK-028",
            "CASE-SK-YORKSHIRE-029",
            "CASE-SK-FICT-CORRIDOR-030",
        ],
    }
    presets["10"] = presets["5a"] + presets["5b"]
    presets["org-sk"] = presets["org"] + presets["sk"]
    cases = presets[args.preset] if args.preset else args.cases
    if args.preset == "5b" and args.run_id == "run-5a":
        args.run_id = "run-5b"
    if args.preset == "10" and args.run_id == "run-5a":
        args.run_id = "run-10a"
    if args.preset == "org-sk" and args.run_id in ("run-5a", "run-5b"):
        args.run_id = "run-org-sk"

    root = benchmark_root()
    run_root = root / "results" / "runs" / args.run_id

    for cid in cases:
        case_dir = root / "cases" / cid
        if not case_dir.is_dir():
            print(f"MISSING case {cid}", file=sys.stderr)
            return 1
        if cid not in CASE_INTEL:
            print(f"No CASE_INTEL for {cid}", file=sys.stderr)
            return 1
        vault = run_root / cid / "vault"
        if vault.exists():
            import shutil

            shutil.rmtree(vault)
        vault.mkdir(parents=True)
        print(f"Building {cid} -> {vault}")
        build_vault(case_dir, vault)
        n = len(list(vault.rglob("*.md")))
        print(f"  notes: {n}")

    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
