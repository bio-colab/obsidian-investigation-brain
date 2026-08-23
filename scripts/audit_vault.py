#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
audit_vault.py — تدقيق حتمي لـ vault أوبسيديان التحقيقي
(obsidian-investigation-brain v0.4.0)

يفحص:
- وجود الملفات الهيكلية الحرجة
- توزيع المناطق والحالات (status)
- انتهاكات منطقة Evidence (لا تخمين)
- سلسلة حفظ الأدلة (Chain of Custody)
- فرضيات Primary بلا Counter
- اكتمال الحقول الإلزامية حسب النوع
- الروابط الويكي المكسورة (تقريبي)
- إشارات Gap Intelligence

Usage:
    python3 audit_vault.py /path/to/case-vault [--json out.json] [--md out.md] [--strict]

Exit codes:
    0  سليم، أو ملاحظات طفيفة/جوهرية فقط (استخدم --strict للفشل عند الجوهرية)
    1  وجود مشكلة حرجة، أو --strict مع وجود جوهرية
    2  خطأ في التشغيل
"""

from __future__ import annotations

import argparse
import json
import os
import posixpath
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required. pip install pyyaml", file=sys.stderr)
    sys.exit(2)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

REQUIRED_FIELDS = {"type", "status", "created", "updated"}
VALID_STATUSES = {
    "verified", "unverified", "draft", "stub", "deprecated",
    "exploration", "working", "pending-human-review", "rejected",
    "open-investigation", "cold-case", "cause-unknown"
}

ZONES = (
    "00-Scaffold",
    "01-Evidence",
    "02-Entities",
    "03-Hypotheses",
    "04-Timeline",
    "05-Analysis",
    "02b-Exploration",
    "06-Outputs",
    "07-Cold-Case",
    "08-Tooling",
    "case-logs",
    "90-Reference-Sources",
    "99-Attachments",
    "OTHER",
)

CRITICAL_FILES = [
    "00-Scaffold/AGENTS.md",
    "00-Scaffold/Case-Scope.md",
    "00-Scaffold/Investigation-Plan.md",
    "00-Scaffold/Coverage-Ledger.md",
    "00-Scaffold/Review-Queue.md",
]

EVIDENCE_TYPES = {
    "physical-evidence", "digital-evidence", "testimonial", "documentary",
    "financial-record", "wiretap-evidence", "audio-visual-evidence", "data-analysis",
    "informant-testimony",
}
HYPOTHESIS_KINDS = {"primary", "alternative", "counter", "rejected"}
REPORT_TYPES = {"case-report", "court-file", "cold-case-report", "briefing"}
MIN_COUNTER_BODY_CHARS = 40
TOOLING_TYPES = {"tool-manifest", "tool-audit", "simulation-run", "case-log"}
TOOLING_ALLOWED_WRITE_PREFIXES = ("08-Tooling", "05-Analysis", "02b-Exploration", "case-logs")

WIKILINK_RE = re.compile(r"\[\[([^\]]+?)(?:\|[^\]]+)?\]\]")
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def detect_zone(rel_path: str) -> str:
    p = rel_path.replace("\\", "/")
    for z in ZONES:
        if p.startswith(z + "/") or p == z:
            return z
    return "OTHER"


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}, text
    try:
        data = yaml.safe_load(m.group(1)) or {}
        if not isinstance(data, dict):
            data = {}
    except Exception:
        data = {}
    body = text[m.end():]
    return data, body


def collect_note_basenames(root: Path) -> set[str]:
    names: set[str] = set()
    for p in root.rglob("*.md"):
        names.add(p.stem)
        try:
            rel = p.relative_to(root).with_suffix("").as_posix()
            names.add(rel)
            names.add(rel.split("/")[-1])
        except ValueError:
            pass
    return names


def find_broken_wikilinks(body: str, known: set[str]) -> list[str]:
    broken = []
    for m in WIKILINK_RE.finditer(body):
        target = m.group(1).strip()
        if target.startswith("#") or target.startswith("^"):
            continue
        pure = target.split("#")[0].split("|")[0].strip()
        if not pure:
            continue
        if pure not in known and pure.replace("\\", "/") not in known:
            last = pure.split("/")[-1]
            if last not in known:
                broken.append(pure)
    return broken


def resolve_link_target(link: str, known: set[str]) -> bool:
    if not link:
        return False
    pure = str(link).strip().strip("[]")
    pure = pure.split("#")[0].split("|")[0].strip()
    if pure in known or pure.replace("\\", "/") in known:
        return True
    last = pure.split("/")[-1]
    return last in known


# ---------------------------------------------------------------------------
# Core audit
# ---------------------------------------------------------------------------

def audit_vault(vault: Path) -> dict[str, Any]:
    if not vault.is_dir():
        raise FileNotFoundError(f"Vault path does not exist or is not a directory: {vault}")

    result: dict[str, Any] = {
        "vault": str(vault),
        "critical_files": {},
        "zones": {z: {"count": 0, "statuses": Counter()} for z in ZONES},
        "status_global": Counter(),
        "issues": [],
        "evidence_without_coc": [],
        "primary_without_counter": [],
        "missing_required_fields": [],
        "invalid_status": [],
        "broken_links_sample": [],
        "notes_total": 0,
        "evidence_count": 0,
        "hypothesis_count": 0,
        "coc_count": 0,
        "skill_version_target": "0.4.2",
        "tooling_manifests": [],
        "tooling_audits": [],
        "memory_events": 0,
        "memory_invalid_lines": 0,
        "memory_snapshot_present": False,
        "coverage_intelligence": None,
    }

    # Collected for post-pass checks (v0.3)
    group_entities: list[tuple[str, dict[str, Any], str]] = []  # rel, fm, body
    person_notes: list[tuple[str, dict[str, Any], str]] = []
    report_notes: list[tuple[str, dict[str, Any], str]] = []
    readiness_notes: list[tuple[str, dict[str, Any]]] = []
    hypothesis_notes: list[tuple[str, dict[str, Any], str]] = []
    tooling_manifests: list[tuple[str, dict[str, Any], str]] = []
    tooling_audits: list[tuple[str, dict[str, Any], str]] = []
    coverage_ledgers: list[tuple[str, dict[str, Any], str]] = []
    investigation_plans: list[tuple[str, dict[str, Any], str]] = []
    contradiction_notes: list[tuple[str, dict[str, Any], str]] = []

    # --- Critical files ---
    for rel in CRITICAL_FILES:
        p = vault / rel
        result["critical_files"][rel] = p.is_file()
        if not p.is_file():
            result["issues"].append({
                "severity": "critical",
                "code": "MISSING_CRITICAL_FILE",
                "msg": f"ملف هيكلي مفقود: {rel}",
                "path": rel,
            })

    # v0.4: optional external decision memory health. It becomes actionable
    # only when the vault opted into 08-Tooling or case-logs.
    memory_dir = vault / "case-logs"
    session_path = memory_dir / "session.jsonl"
    snapshot_path = memory_dir / "memory-snapshot.md"
    opted_into_memory = (vault / "08-Tooling").is_dir() or memory_dir.is_dir()
    if opted_into_memory:
        result["memory_snapshot_present"] = snapshot_path.is_file()
        if session_path.is_file():
            for line in session_path.read_text(encoding="utf-8", errors="replace").splitlines():
                if not line.strip():
                    continue
                try:
                    row = json.loads(line)
                    if isinstance(row, dict):
                        result["memory_events"] += 1
                    else:
                        result["memory_invalid_lines"] += 1
                except json.JSONDecodeError:
                    result["memory_invalid_lines"] += 1
            if result["memory_invalid_lines"]:
                result["issues"].append({
                    "severity": "major",
                    "code": "CASE_MEMORY_INVALID_JSONL",
                    "msg": f"case-logs/session.jsonl يحوي {result['memory_invalid_lines']} سطر غير صالح",
                    "path": "case-logs/session.jsonl",
                })
        else:
            result["issues"].append({
                "severity": "minor",
                "code": "CASE_MEMORY_SESSION_MISSING",
                "msg": "تم تفعيل tooling دون case-logs/session.jsonl",
                "path": "case-logs/session.jsonl",
            })
        if not snapshot_path.is_file():
            result["issues"].append({
                "severity": "minor",
                "code": "CASE_MEMORY_SNAPSHOT_MISSING",
                "msg": "لا يوجد memory-snapshot.md للاستئناف المختصر",
                "path": "case-logs/memory-snapshot.md",
            })

    known_names = collect_note_basenames(vault)
    broken_total = 0

    # --- Walk all markdown notes ---
    for md_path in sorted(vault.rglob("*.md")):
        if any(part.startswith(".") for part in md_path.parts):
            continue
        try:
            rel = md_path.relative_to(vault).as_posix()
        except ValueError:
            continue

        zone = detect_zone(rel)
        result["zones"][zone]["count"] += 1
        result["notes_total"] += 1

        try:
            text = md_path.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            result["issues"].append({
                "severity": "major",
                "code": "READ_ERROR",
                "msg": f"تعذر قراءة الملف: {e}",
                "path": rel,
            })
            continue

        fm, body = parse_frontmatter(text)
        ntype = str(fm.get("type", "")).strip().lower()
        status = str(fm.get("status", "")).strip().lower()

        if status:
            result["status_global"][status] += 1
            result["zones"][zone]["statuses"][status] += 1
        else:
            result["invalid_status"].append(rel)
            result["issues"].append({
                "severity": "major",
                "code": "MISSING_STATUS",
                "msg": "ملاحظة بلا حقل status",
                "path": rel,
            })

        if status and status not in VALID_STATUSES:
            result["invalid_status"].append(rel)
            result["issues"].append({
                "severity": "major",
                "code": "INVALID_STATUS",
                "msg": f"status غير معروف: {status}",
                "path": rel,
            })

        # Required fields
        missing = [f for f in REQUIRED_FIELDS if f not in fm or fm.get(f) in (None, "")]
        if missing and zone not in ("99-Attachments", "OTHER"):
            result["missing_required_fields"].append({"path": rel, "missing": missing})
            result["issues"].append({
                "severity": "minor",
                "code": "MISSING_FIELDS",
                "msg": f"حقول ناقصة: {', '.join(missing)}",
                "path": rel,
            })

        # Zone violations: exploration content must not live in Evidence
        if zone == "01-Evidence" and status == "exploration":
            result["issues"].append({
                "severity": "critical",
                "code": "EXPLORATION_IN_EVIDENCE",
                "msg": "محتوى exploration داخل منطقة Evidence",
                "path": rel,
            })

        # --- Evidence checks (v0.2.0: support source-provenance for public-archive) ---
        if ntype in EVIDENCE_TYPES or (zone == "01-Evidence" and ntype not in ("chain-of-custody", "source-provenance")):
            result["evidence_count"] += 1
            source_kind = str(fm.get("source-kind") or fm.get("source_kind") or "").strip().lower()
            is_archival = source_kind in ("public-archive", "archival", "official-archive", "declassified")

            # Prefer source-provenance for archival/public sources
            sp = fm.get("source-provenance") or fm.get("source_provenance")
            has_provenance = bool(sp) and (
                (isinstance(sp, dict) and sp.get("archive") and (sp.get("record-id") or sp.get("record_id") or sp.get("url")))
                or (isinstance(sp, str) and sp.strip())
            )

            coc = fm.get("chain-of-custody") or fm.get("chain_of_custody")
            has_coc = False
            if coc:
                if isinstance(coc, list):
                    has_coc = any(resolve_link_target(str(c), known_names) for c in coc)
                else:
                    has_coc = resolve_link_target(str(coc), known_names)
            if ntype == "chain-of-custody":
                has_coc = True
                result["coc_count"] += 1

            if is_archival:
                if not has_provenance and not has_coc:
                    result["evidence_without_coc"].append(rel)
                    result["issues"].append({
                        "severity": "critical",
                        "code": "ARCHIVAL_NO_PROVENANCE",
                        "msg": "مصدر أرشيفي/عام بلا source-provenance (أو CoC بديل)",
                        "path": rel,
                    })
            else:
                if not has_coc and ntype != "chain-of-custody":
                    result["evidence_without_coc"].append(rel)
                    result["issues"].append({
                        "severity": "critical",
                        "code": "EVIDENCE_NO_COC",
                        "msg": "دليل بلا سلسلة حفظ (chain-of-custody) صالحة",
                        "path": rel,
                    })

        if ntype == "chain-of-custody":
            result["coc_count"] += 1
            eref = fm.get("evidence-ref") or fm.get("evidence_ref")
            if not eref or not resolve_link_target(str(eref), known_names):
                result["issues"].append({
                    "severity": "major",
                    "code": "COC_NO_EVIDENCE_REF",
                    "msg": "سجل سلسلة حفظ بلا evidence-ref صالح",
                    "path": rel,
                })

        # --- Hypothesis checks ---
        if ntype == "hypothesis":
            result["hypothesis_count"] += 1
            kind = str(fm.get("hypothesis-kind") or fm.get("hypothesis_kind") or "").strip().lower()
            if kind not in HYPOTHESIS_KINDS and kind:
                result["issues"].append({
                    "severity": "minor",
                    "code": "UNKNOWN_HYPOTHESIS_KIND",
                    "msg": f"hypothesis-kind غير معروف: {kind}",
                    "path": rel,
                })
            if kind == "primary":
                counter = fm.get("counter-hypothesis") or fm.get("counter_hypothesis")
                has_counter = False
                if counter:
                    if isinstance(counter, list):
                        has_counter = any(resolve_link_target(str(c), known_names) for c in counter)
                    else:
                        has_counter = resolve_link_target(str(counter), known_names)
                if not has_counter:
                    result["primary_without_counter"].append(rel)
                    result["issues"].append({
                        "severity": "critical",
                        "code": "PRIMARY_NO_COUNTER",
                        "msg": "فرضية Primary بلا Counter-Hypothesis مرتبطة",
                        "path": rel,
                    })

            support = str(fm.get("support-level") or fm.get("support_level") or "").strip().lower()
            supporting = fm.get("supporting-notes") or fm.get("supporting_notes") or []
            if support in ("strong", "conclusive") and (not supporting or supporting == []):
                result["issues"].append({
                    "severity": "major",
                    "code": "STRONG_HYP_NO_SUPPORT",
                    "msg": f"فرضية {support} بلا supporting-notes",
                    "path": rel,
                })
            if support == "conclusive" and isinstance(supporting, list) and len(supporting) < 2:
                result["issues"].append({
                    "severity": "major",
                    "code": "CONCLUSIVE_NEEDS_MULTIPLE_SUPPORT",
                    "msg": "support-level conclusive يتطلب أدلة متعددة ومستقلة (supporting-notes >= 2)",
                    "path": rel,
                })
            hypothesis_notes.append((rel, fm, body))

        # --- v0.3.0: informant / wiretap gates ---
        if ntype == "informant-testimony" and status == "verified":
            cred = fm.get("credibility-assessment") or fm.get("credibility_assessment")
            incomplete = False
            if not cred:
                incomplete = True
            elif isinstance(cred, str) and cred.strip().lower() in ("", "incomplete", "unknown", "n/a"):
                incomplete = True
            elif isinstance(cred, dict):
                # require at least one substantive field
                vals = [str(v).strip() for v in cred.values() if v is not None and str(v).strip()]
                if not vals or all(v.lower() in ("incomplete", "unknown", "n/a", "") for v in vals):
                    incomplete = True
            if incomplete:
                result["issues"].append({
                    "severity": "critical",
                    "code": "INFORMANT_VERIFIED_NO_CRED",
                    "msg": "informant-testimony بحالة verified بلا credibility-assessment مكتمل",
                    "path": rel,
                })

        if ntype == "wiretap-evidence" and status in ("verified", "pending-human-review"):
            auth = fm.get("legal-authorization") or fm.get("legal_authorization")
            if not auth or (isinstance(auth, str) and not str(auth).strip()):
                # also allow body mention
                if "legal-authorization" not in text.lower() and "warrant" not in text.lower() and "تفويض" not in text:
                    sev = "critical" if status == "verified" else "major"
                    result["issues"].append({
                        "severity": sev,
                        "code": "WIRETAP_NO_AUTH",
                        "msg": "wiretap-evidence بلا legal-authorization موثّق",
                        "path": rel,
                    })

        if ntype == "group-entity":
            group_entities.append((rel, fm, body))
        if ntype == "person":
            person_notes.append((rel, fm, body))
        if ntype == "coverage-ledger" or rel.endswith("Coverage-Ledger.md"):
            coverage_ledgers.append((rel, fm, body))
        if ntype == "investigation-plan" or rel.endswith("Investigation-Plan.md"):
            investigation_plans.append((rel, fm, body))
        if ntype == "contradiction":
            contradiction_notes.append((rel, fm, body))
        if ntype in REPORT_TYPES or zone == "06-Outputs":
            if ntype in REPORT_TYPES or "report" in rel.lower() or "court" in rel.lower():
                report_notes.append((rel, fm, body))
        if ntype == "readiness-checklist" or rel.endswith("Readiness-Checklist.md"):
            readiness_notes.append((rel, fm))

        # v0.4: self-tooling records must stay auditable and case-scoped
        if ntype == "tool-manifest" or rel.startswith("08-Tooling/Manifests/"):
            tooling_manifests.append((rel, fm, body))
            result["tooling_manifests"].append(rel)
        if ntype == "tool-audit" or rel.startswith("08-Tooling/Audits/"):
            tooling_audits.append((rel, fm, body))
            result["tooling_audits"].append(rel)

        # Broken wikilinks (sample)
        broken = find_broken_wikilinks(body, known_names)
        if broken:
            broken_total += len(broken)
            if len(result["broken_links_sample"]) < 30:
                result["broken_links_sample"].append({
                    "path": rel,
                    "targets": broken[:5],
                })

    result["broken_links_total_est"] = broken_total

    # --- v0.3.1: Coverage-Ledger structured gaps ---
    for md_path in sorted(vault.rglob("Coverage-Ledger.md")):
        try:
            rel = md_path.relative_to(vault).as_posix()
            text = md_path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        fm, _body = parse_frontmatter(text)
        gaps = fm.get("gaps")
        if gaps is None:
            result["issues"].append({
                "severity": "minor",
                "code": "LEDGER_GAPS_UNSTRUCTURED",
                "msg": "Coverage-Ledger بلا حقل gaps: في YAML (مُفضّل v0.3.1)",
                "path": rel,
            })
        elif isinstance(gaps, list) and gaps:
            for i, g in enumerate(gaps):
                if not isinstance(g, dict) or not g.get("id") or not g.get("description"):
                    result["issues"].append({
                        "severity": "minor",
                        "code": "LEDGER_GAP_ROW_INCOMPLETE",
                        "msg": f"gaps[{i}] يحتاج id + description",
                        "path": rel,
                    })

    # --- v0.3 post-pass: thin counters ---
    for rel, fm, body in hypothesis_notes:
        kind = str(fm.get("hypothesis-kind") or fm.get("hypothesis_kind") or "").strip().lower()
        if kind != "primary":
            continue
        counter = fm.get("counter-hypothesis") or fm.get("counter_hypothesis")
        if not counter:
            continue
        targets = counter if isinstance(counter, list) else [counter]
        for c in targets:
            pure = str(c).strip().strip("[]").split("#")[0].split("|")[0].strip()
            stem = pure.split("/")[-1]
            # find counter note body among hypothesis_notes
            cbody = ""
            for r2, fm2, b2 in hypothesis_notes:
                if Path(r2).stem == stem or r2.endswith(stem + ".md"):
                    cbody = b2 or ""
                    break
            if cbody and len(cbody.strip()) < MIN_COUNTER_BODY_CHARS:
                result["issues"].append({
                    "severity": "major",
                    "code": "PRIMARY_COUNTER_THIN",
                    "msg": f"Counter مرتبط لكن مضمونه أقصر من {MIN_COUNTER_BODY_CHARS} حرفاً",
                    "path": rel,
                })

    # --- v0.3: group-entity vs named person victims ---
    empty_victim_groups = False
    for rel, fm, body in group_entities:
        role = str(fm.get("role") or "").strip().lower()
        if role not in ("victims", "passengers", "crew"):
            continue
        named = fm.get("named-individuals") or fm.get("named_individuals") or []
        if not named:
            empty_victim_groups = True
    if empty_victim_groups:
        for rel, fm, body in person_notes:
            role = str(fm.get("role") or "").strip().lower()
            if role not in ("victim", "passenger", "crew", "missing-person"):
                continue
            # Allow explicit packet labels that look like placeholders
            title_line = ""
            for line in (body or "").splitlines():
                if line.strip().startswith("#"):
                    title_line = line.strip().lstrip("#").strip()
                    break
            stem = Path(rel).stem
            label = title_line or stem
            low = label.lower()
            if any(x in low for x in ("unidentified", "unknown", "unnamed", "group", "label", "poi", "غير")):
                continue
            result["issues"].append({
                "severity": "major",
                "code": "GROUP_VICTIM_NAME_WITH_EMPTY_GROUP",
                "msg": "Person بدور ضحية/راكب بينما group-entity للضحايا بلا named-individuals — راجع اختلاق الأسماء",
                "path": rel,
            })

    # --- v0.4.3: Coverage Intelligence — نسبة مراحل الخطة التي لها صف في الـ Ledger
    def _table_data_rows(body_text: str) -> list[str]:
        rows = []
        for ln in (body_text or "").splitlines():
            s = ln.strip()
            if not s.startswith("|"):
                continue
            core = s.strip("|").replace("-", "").replace(":", "").replace(" ", "").replace("|", "")
            if not core:
                continue  # separator row
            rows.append(s)
        if rows and any(k in rows[0] for k in ("المرحلة", "Phase", "phase", "البنود")):
            rows = rows[1:]
        return rows

    coverage_info: dict[str, Any] | None = None
    plan_rel, plan_body = next(((r, b) for r, _f, b in investigation_plans), (None, None))
    ledger_rel, ledger_body = next(((r, b) for r, _f, b in coverage_ledgers), (None, None))
    if plan_rel:
        plan_phases = len(re.findall(r"(?m)^\s*\d+\.\s+\S", plan_body or ""))
        ledger_rows = len(_table_data_rows(ledger_body)) if ledger_rel else 0
        pct = round((ledger_rows / plan_phases) * 100) if plan_phases else 0
        coverage_info = {
            "plan": plan_rel,
            "plan_phases": plan_phases,
            "ledger": ledger_rel,
            "ledger_rows": ledger_rows,
            "coverage_pct": pct,
        }
        result["coverage_intelligence"] = coverage_info
        if not ledger_rel:
            result["issues"].append({
                "severity": "major",
                "code": "COVERAGE_LEDGER_MISSING_ROWS_FILE",
                "msg": "خطة تحقيق موجودة بلا Coverage-Ledger قابل للقراءة",
                "path": str(plan_rel),
            })
        elif ledger_rows == 0 and plan_phases > 0:
            result["issues"].append({
                "severity": "major",
                "code": "COVERAGE_LEDGER_EMPTY",
                "msg": f"Coverage-Ledger بلا صفوف مراحل بينما الخطة تحتوي {plan_phases} مرحلة",
                "path": str(ledger_rel),
            })
        elif pct < 50:
            result["issues"].append({
                "severity": "major",
                "code": "COVERAGE_LEDGER_LOW",
                "msg": f"تغطية الـ Ledger منخفضة: {ledger_rows}/{plan_phases} مراحل ({pct}%)",
                "path": str(ledger_rel),
            })
        elif pct < 100:
            result["issues"].append({
                "severity": "minor",
                "code": "COVERAGE_LEDGER_PARTIAL",
                "msg": f"تغطية جزئية للخطة في الـ Ledger: {ledger_rows}/{plan_phases} مراحل ({pct}%)",
                "path": str(ledger_rel),
            })

    # --- v0.4.3: فرضيات قوية معتمدة على أدلة داخل تناقض مفتوح
    def _link_stem(value: Any) -> str:
        s = str(value).strip().strip("[]")
        s = s.split("#")[0].split("|")[0].strip()
        stem = s.replace("\\", "/").split("/")[-1]
        return re.sub(r"\.md$", "", stem).strip().lower()

    open_contradictions: dict[str, set[str]] = {}
    for rel, fm, _body in contradiction_notes:
        status_c = str(fm.get("status") or "").strip().lower()
        between = fm.get("between") or fm.get("related-evidence") or fm.get("related-events") or []
        if not isinstance(between, list):
            between = [between]
        stems = {_link_stem(x) for x in between if str(x).strip()}
        stems.discard("")
        # `undermines` names the side(s) the contradiction actually weakens. When
        # present it takes precedence so hypotheses resting on the *surviving*
        # side are not falsely flagged for merely sharing the contradiction.
        if "undermines" in fm:
            under = fm.get("undermines") or []
            if not isinstance(under, list):
                under = [under]
            stems = {_link_stem(x) for x in under if str(x).strip()}
            stems.discard("")
        if not stems and status_c not in ("deprecated", "rejected"):
            result["issues"].append({
                "severity": "minor",
                "code": "CONTRADICTION_UNLINKED",
                "msg": "تناقض مسجل بلا روابط بين الأطراف المتناقضة (between/undermines)",
                "path": rel,
            })
            continue
        open_contradictions[rel] = stems
    for hrel, hfm, _hbody in hypothesis_notes:
        h_status = str(hfm.get("status") or "").strip().lower()
        h_kind = str(hfm.get("hypothesis-kind") or hfm.get("hypothesis_kind") or "").strip().lower()
        if h_status in ("rejected", "deprecated") or h_kind == "rejected":
            continue  # rejected hypotheses may legitimately cite contradicted evidence
        sup = hfm.get("supporting-notes") or hfm.get("supporting_notes") or []
        if not isinstance(sup, list) or not sup:
            continue
        hs = {_link_stem(x) for x in sup}
        lvl = str(hfm.get("support-level") or hfm.get("support_level") or "").strip().lower()
        hits = sorted(cr for cr, stems in open_contradictions.items() if stems & hs)
        if not hits:
            continue
        if lvl in ("strong", "conclusive"):
            result["issues"].append({
                "severity": "major",
                "code": "HYPOTHESIS_STRONG_ON_CONTRADICTION",
                "msg": f"فرضية {lvl} تعتمد على دليل داخل تناقض غير محلول: {', '.join(Path(h).stem for h in hits)}",
                "path": hrel,
            })
        else:
            result["issues"].append({
                "severity": "minor",
                "code": "HYPOTHESIS_ON_CONTRADICTION",
                "msg": f"فرضية تستخدم دليلاً داخل تناقض مفتوح: {', '.join(Path(h).stem for h in hits)}",
                "path": hrel,
            })

        # --- v0.4: self-tooling manifest/audit consistency
    audit_blob = "\n".join(f"{r}\n{b}" for r, _fm, b in tooling_audits)
    for rel, fm, _body in tooling_manifests:
        tool_id = str(fm.get("tool-id") or fm.get("tool_id") or "").strip()
        entrypoint = str(fm.get("entrypoint") or "").strip()
        if not tool_id or not entrypoint:
            result["issues"].append({
                "severity": "major",
                "code": "TOOL_MANIFEST_INCOMPLETE",
                "msg": "Tool-Manifest يحتاج tool-id وentrypoint",
                "path": rel,
            })
        writes = fm.get("writes-to") or fm.get("writes_to") or []
        if not isinstance(writes, list):
            writes = [writes]
        for write_target in writes:
            raw_text_target = str(write_target).replace("\\", "/")
            drive_prefix = os.path.splitdrive(raw_text_target)[0]
            is_absolute = bool(drive_prefix) or raw_text_target.startswith("/")
            clean = posixpath.normpath(raw_text_target.lstrip("/"))
            escapes = is_absolute or clean == ".." or clean.startswith("../")
            if escapes or not any(clean == prefix or clean.startswith(prefix + "/") for prefix in TOOLING_ALLOWED_WRITE_PREFIXES):
                result["issues"].append({
                    "severity": "critical",
                    "code": "TOOL_MANIFEST_WRITE_ESCAPE",
                    "msg": f"Self-tooling writes outside allowed case prefixes: {write_target}",
                    "path": rel,
                })
        if tool_id and tool_id not in audit_blob:
            result["issues"].append({
                "severity": "minor",
                "code": "TOOL_MANIFEST_NO_AUDIT",
                "msg": f"Tool-Manifest {tool_id} has no matching Tool-Audit yet",
                "path": rel,
            })

    # --- v0.3: reports claim-trace + court readiness
    readiness_ok = False
    for rel, fm in readiness_notes:
        if fm.get("readiness-passed") is True or str(fm.get("readiness-passed")).lower() == "true":
            readiness_ok = True

    for rel, fm, body in report_notes:
        ntype = str(fm.get("type") or "").strip().lower()
        status = str(fm.get("status") or "").strip().lower()
        claim_trace = fm.get("claim-trace") or fm.get("claim_trace") or []
        has_trace = isinstance(claim_trace, list) and len(claim_trace) > 0
        if not has_trace and "claim-trace" in (body or "").lower():
            # table-only partial credit → still major if court/final
            has_trace = False

        is_court = ntype == "court-file" or "court-file" in rel.lower() or "/Court-File" in rel.replace("\\", "/")
        is_finalish = status in ("verified",) or is_court

        if is_court:
            rp = fm.get("readiness-passed")
            court_ready = rp is True or str(rp).lower() == "true"
            if not court_ready and not readiness_ok:
                result["issues"].append({
                    "severity": "critical",
                    "code": "COURT_WITHOUT_READINESS",
                    "msg": "court-file بدون readiness-passed على التقرير أو Readiness-Checklist",
                    "path": rel,
                })
            if not has_trace:
                # check empty list vs missing
                empty_rows = True
                if isinstance(claim_trace, list):
                    for row in claim_trace:
                        if isinstance(row, dict) and (row.get("evidence") or row.get("claim")):
                            empty_rows = False
                            break
                if empty_rows:
                    result["issues"].append({
                        "severity": "critical",
                        "code": "COURT_NO_CLAIM_TRACE",
                        "msg": "court-file بلا claim-trace (مصفوفة تتبع الادعاءات)",
                        "path": rel,
                    })

        if ntype in ("case-report", "cold-case-report") and is_finalish and not has_trace:
            result["issues"].append({
                "severity": "major",
                "code": "REPORT_NO_CLAIM_TRACE",
                "msg": "تقرير معتمد/verified بلا claim-trace",
                "path": rel,
            })

        # claim-trace rows must have evidence when present
        if isinstance(claim_trace, list):
            for i, row in enumerate(claim_trace):
                if not isinstance(row, dict):
                    continue
                ev = row.get("evidence") or row.get("supporting-notes") or []
                if not ev:
                    result["issues"].append({
                        "severity": "major",
                        "code": "CLAIM_TRACE_NO_EVIDENCE",
                        "msg": f"claim-trace[{i}] بلا evidence",
                        "path": rel,
                    })

    return result


def compute_score(res: dict[str, Any]) -> dict[str, int]:
    critical = sum(1 for i in res["issues"] if i["severity"] == "critical")
    major = sum(1 for i in res["issues"] if i["severity"] == "major")
    minor = sum(1 for i in res["issues"] if i["severity"] == "minor")
    return {
        "critical": critical,
        "major": major,
        "minor": minor,
        "total_issues": critical + major + minor,
    }


def render_markdown(res: dict[str, Any], score: dict[str, int]) -> str:
    lines: list[str] = []
    lines.append("# تقرير تدقيق الـ Vault التحقيقي")
    lines.append("")
    lines.append(f"**المسار:** `{res['vault']}`")
    lines.append(f"**إجمالي الملاحظات:** {res['notes_total']}")
    lines.append(f"**أدلة:** {res['evidence_count']} · **سجلات CoC:** {res['coc_count']} · **فرضيات:** {res['hypothesis_count']}")
    if "memory_events" in res:
        lines.append(f"**External memory:** events={res['memory_events']} · invalid={res['memory_invalid_lines']} · snapshot={'yes' if res['memory_snapshot_present'] else 'no'}")
    if res.get("native_validation"):
        native = res["native_validation"]
        lines.append(f"**Native formats:** errors={native.get('errors', 0)} · warnings={native.get('warnings', 0)}")
    lines.append("")
    lines.append("## الدرجة")
    lines.append("")
    lines.append(f"- 🔴 حرج (critical): **{score['critical']}**")
    lines.append(f"- 🟠 جوهري (major): **{score['major']}**")
    lines.append(f"- 🟡 طفيف (minor): **{score['minor']}**")
    lines.append("")

    # Critical files
    lines.append("## الملفات الهيكلية الحرجة")
    lines.append("")
    for rel, ok in res["critical_files"].items():
        mark = "✅" if ok else "❌"
        lines.append(f"- {mark} `{rel}`")
    lines.append("")

    # Zones
    lines.append("## توزيع المناطق")
    lines.append("")
    lines.append("| المنطقة | عدد الملاحظات |")
    lines.append("|---------|----------------|")
    for z in ZONES:
        if z == "OTHER" and res["zones"][z]["count"] == 0:
            continue
        lines.append(f"| `{z}` | {res['zones'][z]['count']} |")
    lines.append("")

    # Status distribution
    lines.append("## توزيع status")
    lines.append("")
    sg = res["status_global"]
    if isinstance(sg, Counter):
        for k, v in sg.most_common():
            lines.append(f"- `{k}`: {v}")
    else:
        for k, v in sorted(sg.items(), key=lambda x: -x[1]):
            lines.append(f"- `{k}`: {v}")
    lines.append("")

    # Gap Intelligence
    lines.append("## Gap Intelligence")
    lines.append("")
    lines.append(f"- أدلة بلا سلسلة حفظ: **{len(res['evidence_without_coc'])}**")
    for p in res["evidence_without_coc"][:15]:
        lines.append(f"  - `{p}`")
    if len(res["evidence_without_coc"]) > 15:
        lines.append(f"  - ... و {len(res['evidence_without_coc']) - 15} أخرى")
    lines.append("")
    lines.append(f"- فرضيات Primary بلا Counter: **{len(res['primary_without_counter'])}**")
    for p in res["primary_without_counter"][:15]:
        lines.append(f"  - `{p}`")
    if len(res["primary_without_counter"]) > 15:
        lines.append(f"  - ... و {len(res['primary_without_counter']) - 15} أخرى")
    lines.append("")

    # Issues
    lines.append("## قائمة المشكلات")
    lines.append("")
    if not res["issues"]:
        lines.append("_لا توجد مشكلات مكتشفة._")
    else:
        by_sev = defaultdict(list)
        for i in res["issues"]:
            by_sev[i["severity"]].append(i)
        for sev in ("critical", "major", "minor"):
            items = by_sev.get(sev, [])
            if not items:
                continue
            lines.append(f"### {sev.upper()} ({len(items)})")
            lines.append("")
            for i in items[:40]:
                lines.append(f"- **{i['code']}** — {i['msg']}")
                lines.append(f"  - `{i.get('path', '')}`")
            if len(items) > 40:
                lines.append(f"- ... و {len(items) - 40} أخرى")
            lines.append("")

    # Broken links sample
    if res.get("broken_links_sample"):
        lines.append("## عيّنة روابط مكسورة (تقريبي)")
        lines.append("")
        lines.append(f"تقدير إجمالي: ~{res.get('broken_links_total_est', 0)}")
        lines.append("")
        for item in res["broken_links_sample"][:10]:
            targets = ", ".join(f"`{t}`" for t in item["targets"])
            lines.append(f"- `{item['path']}` → {targets}")
        lines.append("")

    lines.append("---")
    lines.append("*تولّد بواسطة `scripts/audit_vault.py` — obsidian-investigation-brain*")
    return "\n".join(lines)


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(
        description="Deterministic audit of an Obsidian investigation vault."
    )
    ap.add_argument("vault", help="Path to the case vault root directory")
    ap.add_argument("--json", default=None, help="Write full JSON report to this path")
    ap.add_argument("--md", default=None, help="Write Markdown report to this path (default: stdout)")
    ap.add_argument("--strict", action="store_true", help="Exit 1 on any critical or major issue")
    ap.add_argument("--native", action="store_true", help="Also validate Markdown, Canvas, and Bases formats")
    args = ap.parse_args()

    vault = Path(args.vault)
    try:
        res = audit_vault(vault)
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2
    except Exception as e:
        print(f"ERROR: unexpected failure: {e}", file=sys.stderr)
        return 2

    if args.native:
        try:
            from validate_obsidian_native import validate as validate_native
            native = validate_native(vault)
            res["native_validation"] = native["score"]
            for item in native["issues"]:
                severity = "major" if item["severity"] == "error" else "minor"
                res["issues"].append({
                    "severity": severity,
                    "code": f"NATIVE_{item['code']}",
                    "msg": item["message"],
                    "path": item["path"],
                })
        except Exception as exc:
            res["native_validation"] = {"errors": 1, "warnings": 0, "total": 1}
            res["issues"].append({
                "severity": "major",
                "code": "NATIVE_VALIDATOR_FAILED",
                "msg": str(exc),
                "path": str(vault),
            })

    score = compute_score(res)

    # Make Counters JSON-serializable
    def serialize(obj: Any) -> Any:
        if isinstance(obj, Counter):
            return dict(obj)
        if isinstance(obj, dict):
            return {k: serialize(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [serialize(x) for x in obj]
        return obj

    md = render_markdown(res, score)

    if args.json:
        out = serialize({**res, "score": score})
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=2)
        print(f"JSON written to {args.json}", file=sys.stderr)

    if args.md:
        with open(args.md, "w", encoding="utf-8") as f:
            f.write(md)
        print(f"Markdown written to {args.md}", file=sys.stderr)
    else:
        print(md)

    if args.strict and (score["critical"] > 0 or score["major"] > 0):
        return 1
    if score["critical"] > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
