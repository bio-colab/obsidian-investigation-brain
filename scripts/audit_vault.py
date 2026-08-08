#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
audit_vault.py — تدقيق حتمي لـ vault أوبسيديان التحقيقي
(obsidian-investigation-brain v0.3.0)

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
    0  سليم أو ملاحظات طفيفة فقط
    1  انتهاكات جوهرية أو حرجة
    2  خطأ في التشغيل
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Optional

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
    "exploration", "pending-human-review", "rejected",
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
        "skill_version_target": "0.3.1",
    }

    # Collected for post-pass checks (v0.3)
    group_entities: list[tuple[str, dict[str, Any], str]] = []  # rel, fm, body
    person_notes: list[tuple[str, dict[str, Any], str]] = []
    report_notes: list[tuple[str, dict[str, Any], str]] = []
    readiness_notes: list[tuple[str, dict[str, Any]]] = []
    hypothesis_notes: list[tuple[str, dict[str, Any], str]] = []

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
        if ntype in REPORT_TYPES or zone == "06-Outputs":
            if ntype in REPORT_TYPES or "report" in rel.lower() or "court" in rel.lower():
                report_notes.append((rel, fm, body))
        if ntype == "readiness-checklist" or rel.endswith("Readiness-Checklist.md"):
            readiness_notes.append((rel, fm))

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

    # --- v0.3: reports claim-trace + court readiness ---
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

    # Convert Counters for later JSON
    result["status_global"] = result["status_global"]
    for z in result["zones"]:
        result["zones"][z]["statuses"] = result["zones"][z]["statuses"]

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
    ap = argparse.ArgumentParser(
        description="Deterministic audit of an Obsidian investigation vault."
    )
    ap.add_argument("vault", help="Path to the case vault root directory")
    ap.add_argument("--json", default=None, help="Write full JSON report to this path")
    ap.add_argument("--md", default=None, help="Write Markdown report to this path (default: stdout)")
    ap.add_argument("--strict", action="store_true", help="Exit 1 on any critical or major issue")
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
