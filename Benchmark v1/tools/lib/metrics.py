from __future__ import annotations

import re
from datetime import datetime, timedelta
from typing import Any, Optional

from .text_match import alias_hit, any_pattern_hit, normalize, similarity
from .vault_parse import (
    ARCHIVAL_KINDS,
    VaultIndex,
    evidence_has_coc,
    evidence_has_provenance,
    extract_wikilinks,
    is_archival_evidence,
    is_evidence_note,
    list_report_notes,
    resolve_link,
    source_kind_of,
)


def _clip(x: float) -> float:
    return max(0.0, min(1.0, float(x)))


def _as_list(v: Any) -> list[Any]:
    if v is None:
        return []
    if isinstance(v, list):
        return v
    return [v]


def _parse_date(s: str) -> Optional[datetime]:
    if not s:
        return None
    s = str(s).strip()
    for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M", "%Y-%m-%dT%H:%M:%S", "%Y/%m/%d", "%Y"):
        try:
            return datetime.strptime(s[: len(datetime.now().strftime(fmt)) if fmt == "%Y" else 19], fmt)
        except Exception:
            continue
    # year only
    m = re.match(r"^(\d{4})", s)
    if m:
        try:
            return datetime(int(m.group(1)), 1, 1)
        except Exception:
            return None
    return None


def _note_search_blob(note) -> str:
    eid = str(note.frontmatter.get("evidence-id") or note.frontmatter.get("evidence_id") or "")
    return " ".join([note.stem, note.title_guess, eid, note.body[:2000], str(note.frontmatter)])


def _match_evidence(gt_item: dict, idx: VaultIndex, threshold: float) -> tuple[Optional[Any], float]:
    aliases = [gt_item.get("id", ""), gt_item.get("title", "")] + list(gt_item.get("aliases") or [])
    best_n, best_s = None, 0.0
    for note in idx.notes:
        if not is_evidence_note(note) and note.type not in ("source-provenance",):
            # still allow match on evidence-like documentary notes only
            if note.zone != "01-Evidence":
                continue
        blob = _note_search_blob(note)
        eid = str(note.frontmatter.get("evidence-id") or note.frontmatter.get("evidence_id") or "")
        score = 0.0
        if eid and normalize(eid) == normalize(gt_item.get("id", "")):
            score = 1.0
        else:
            for a in aliases:
                if not a:
                    continue
                if normalize(a) and normalize(a) in normalize(blob):
                    score = max(score, 0.9)
                score = max(score, similarity(a, note.title_guess), similarity(a, note.stem))
                score = max(score, similarity(a, blob[:300]))
        if score > best_s:
            best_n, best_s = note, score
    if best_s >= threshold:
        return best_n, best_s
    return None, best_s


def score_evidence_coverage(gt: dict, idx: VaultIndex, threshold: float) -> dict:
    items = [e for e in (gt.get("evidence") or []) if e.get("required", True)]
    if not items:
        return {"id": "M01", "score": 1.0, "raw": {"recall": 1.0, "precision": 1.0}, "details": {"matched": []}}
    matched = []
    matched_paths = set()
    for e in items:
        note, s = _match_evidence(e, idx, threshold)
        if note:
            matched.append({"gt_id": e["id"], "path": note.path, "sim": round(s, 3)})
            matched_paths.add(note.path)
    recall = len(matched) / len(items)
    vault_ev = [n for n in idx.notes if is_evidence_note(n)]
    precision = (len(matched_paths) / len(vault_ev)) if vault_ev else 1.0
    # precision only among matched set size vs vault — softer: min(1, matched/max(vault,1)) style
    precision = _clip(precision if vault_ev else 1.0)
    # If many extra notes, precision drops; if few notes covering GT, precision high
    if vault_ev:
        precision = _clip(len(matched) / max(len(vault_ev), 1))
    score = _clip(0.7 * recall + 0.3 * precision)
    return {
        "id": "M01",
        "score": score,
        "raw": {"recall": recall, "precision": precision, "gt": len(items), "matched": len(matched)},
        "details": {"matched": matched, "unmatched": [e["id"] for e in items if e["id"] not in {m["gt_id"] for m in matched}]},
    }


def score_source_provenance(gt: dict, idx: VaultIndex, threshold: float, score_only_matched: bool = False) -> dict:
    items = [e for e in (gt.get("evidence") or []) if e.get("required", True)]
    checks = []
    if score_only_matched or items:
        for e in items:
            note, s = _match_evidence(e, idx, threshold)
            if not note:
                checks.append({"gt_id": e["id"], "ok": False, "reason": "missing_evidence"})
                continue
            archival = is_archival_evidence(note, e.get("source_kind"))
            if e.get("must_have_provenance") or archival or e.get("source_kind") in ARCHIVAL_KINDS:
                ok = evidence_has_provenance(note)
                checks.append({"gt_id": e["id"], "path": note.path, "ok": ok, "mode": "provenance"})
            else:
                ok = evidence_has_coc(note, idx.known_names)
                checks.append({"gt_id": e["id"], "path": note.path, "ok": ok, "mode": "coc"})
    else:
        for note in idx.notes:
            if not is_evidence_note(note):
                continue
            if is_archival_evidence(note):
                ok = evidence_has_provenance(note)
                checks.append({"path": note.path, "ok": ok, "mode": "provenance"})
            else:
                ok = evidence_has_coc(note, idx.known_names)
                checks.append({"path": note.path, "ok": ok, "mode": "coc"})

    if not checks:
        return {"id": "M02", "score": 0.0, "raw": {"complete": 0, "total": 0}, "details": checks}
    complete = sum(1 for c in checks if c.get("ok"))
    score = complete / len(checks)
    return {"id": "M02", "score": _clip(score), "raw": {"complete": complete, "total": len(checks)}, "details": checks}


def _match_hypothesis(gt_h: dict, idx: VaultIndex, threshold: float):
    aliases = [gt_h.get("id", ""), gt_h.get("statement", "")] + list(gt_h.get("aliases") or [])
    best_n, best_s = None, 0.0
    for note in idx.notes_of("hypothesis") + [n for n in idx.notes if n.zone.startswith("03-Hypotheses")]:
        blob = _note_search_blob(note)
        score = 0.0
        for a in aliases:
            if not a:
                continue
            if normalize(a) in normalize(blob):
                score = max(score, 0.92)
            score = max(score, similarity(a, note.title_guess), similarity(a, note.body[:400]))
        kind = str(note.frontmatter.get("hypothesis-kind") or note.frontmatter.get("hypothesis_kind") or "").lower()
        if gt_h.get("kind") and kind and kind != str(gt_h["kind"]).lower():
            score *= 0.85
        if score > best_s:
            best_n, best_s = note, score
    if best_s >= threshold:
        return best_n, best_s
    return None, best_s


def score_hypothesis_coverage(gt: dict, idx: VaultIndex, threshold: float) -> dict:
    items = [h for h in (gt.get("hypotheses") or []) if h.get("required", True)]
    if not items:
        return {"id": "M03", "score": 1.0, "raw": {}, "details": {}}
    matched = []
    for h in items:
        note, s = _match_hypothesis(h, idx, threshold)
        if note:
            matched.append({"gt_id": h["id"], "path": note.path, "sim": round(s, 3)})
    score = len(matched) / len(items)
    return {
        "id": "M03",
        "score": _clip(score),
        "raw": {"matched": len(matched), "total": len(items)},
        "details": {
            "matched": matched,
            "unmatched": [h["id"] for h in items if h["id"] not in {m["gt_id"] for m in matched}],
        },
    }


def score_counter_quality(gt: dict, idx: VaultIndex, threshold: float, min_chars: int = 40) -> dict:
    primaries = []
    seen_paths: set[str] = set()
    for note in idx.notes_of("hypothesis") + [n for n in idx.notes if "03-Hypotheses/Primary" in n.path.replace("\\", "/")]:
        if note.path in seen_paths:
            continue
        kind = str(note.frontmatter.get("hypothesis-kind") or note.frontmatter.get("hypothesis_kind") or "").lower()
        if kind == "primary" or "/Primary/" in note.path.replace("\\", "/"):
            primaries.append(note)
            seen_paths.add(note.path)

    gt_primaries = [h for h in (gt.get("hypotheses") or []) if h.get("kind") == "primary" and h.get("required", True)]
    if not primaries:
        score = 0.0 if gt_primaries else 1.0
        return {"id": "M04", "score": score, "raw": {"primaries": 0}, "details": {"note": "no primary hypotheses in vault"}}

    details = []
    scores = []
    for p in primaries:
        counter = p.frontmatter.get("counter-hypothesis") or p.frontmatter.get("counter_hypothesis")
        link_ok = False
        counter_note = None
        if counter:
            if isinstance(counter, list):
                link_ok = any(resolve_link(c, idx.known_names) for c in counter)
                for c in _as_list(counter):
                    stem = str(c).strip("[]").split("/")[-1].split("|")[0]
                    if stem in idx.by_stem:
                        counter_note = idx.by_stem[stem][0]
                        break
            else:
                link_ok = resolve_link(counter, idx.known_names)
                stem = str(counter).strip("[]").split("/")[-1].split("|")[0]
                if stem in idx.by_stem:
                    counter_note = idx.by_stem[stem][0]

        body = (counter_note.body if counter_note else "") or ""
        substantive = len(body.strip()) >= min_chars and normalize(body) != normalize(p.body)
        if counter_note and normalize(counter_note.title_guess) == normalize(p.title_guess):
            substantive = False

        theme_score = 0.5  # neutral if no GT theme
        # find GT primary match for themes
        gtp, _ = None, 0.0
        for h in gt_primaries:
            n, s = _match_hypothesis(h, idx, threshold)
            if n and n.path == p.path:
                gtp = h
                break
            # fuzzy via statement
            if similarity(h.get("statement", ""), p.title_guess + " " + p.body[:200]) >= threshold:
                gtp = h
                break
        if gtp and gtp.get("expected_counter_themes"):
            themes = gtp["expected_counter_themes"]
            blob = (counter_note.text if counter_note else str(counter) or "")
            hits = sum(
                1
                for t in themes
                if t
                and (
                    normalize(t) in normalize(blob)
                    or similarity(t, blob[:800]) >= 0.45
                    or any(tok and tok in normalize(blob) for tok in normalize(t).split() if len(tok) > 4)
                )
            )
            theme_score = hits / max(len(themes), 1)

        s = 0.40 * (1.0 if link_ok else 0.0) + 0.30 * (1.0 if substantive else 0.0) + 0.30 * theme_score
        scores.append(s)
        details.append(
            {
                "primary": p.path,
                "link_ok": link_ok,
                "substantive": substantive,
                "theme_score": round(theme_score, 3),
                "score": round(s, 3),
            }
        )
    return {"id": "M04", "score": _clip(sum(scores) / len(scores)), "raw": {"primaries": len(primaries)}, "details": details}


def score_timeline(gt: dict, idx: VaultIndex, threshold: float, date_tol_days: int = 1) -> dict:
    events = [e for e in (gt.get("timeline_events") or []) if e.get("required", True)]
    if not events:
        return {"id": "M05", "score": 1.0, "raw": {}, "details": {}}
    vault_events = idx.notes_of("timeline-event") + [
        n for n in idx.notes if n.zone.startswith("04-Timeline") and n.type != "alibi"
    ]
    matched = []
    for ge in events:
        best_s = 0.0
        best_path = None
        gdate = _parse_date(ge.get("timestamp", ""))
        for ve in vault_events:
            ts = str(ve.frontmatter.get("timestamp") or "")
            vdate = _parse_date(ts)
            date_ok = True
            if gdate and vdate:
                # year-only GT precision
                prec = ge.get("precision") or "day-only"
                if prec in ("year-only",):
                    date_ok = gdate.year == vdate.year
                elif prec in ("month-only",):
                    date_ok = gdate.year == vdate.year and gdate.month == vdate.month
                else:
                    date_ok = abs((gdate - vdate).days) <= date_tol_days
            elif gdate and not vdate:
                # allow year mention in body
                date_ok = str(gdate.year) in ve.text
            text_s = max(
                similarity(ge.get("summary", ""), ve.title_guess),
                similarity(ge.get("summary", ""), ve.body[:400]),
                similarity(ge.get("id", ""), ve.stem),
            )
            if alias_hit(ge.get("aliases") or [], ve.text, threshold=0.7):
                text_s = max(text_s, 0.88)
            s = text_s
            if not date_ok:
                s *= 0.5
            if s > best_s:
                best_s, best_path = s, ve.path
        if best_s >= threshold:
            matched.append({"gt_id": ge["id"], "path": best_path, "sim": round(best_s, 3)})
    score = len(matched) / len(events)
    return {
        "id": "M05",
        "score": _clip(score),
        "raw": {"matched": len(matched), "total": len(events)},
        "details": {
            "matched": matched,
            "unmatched": [e["id"] for e in events if e["id"] not in {m["gt_id"] for m in matched}],
        },
    }


def score_contradictions(gt: dict, idx: VaultIndex, threshold: float) -> dict:
    items = gt.get("contradictions") or []
    if not items:
        return {"id": "M06", "score": 1.0, "raw": {}, "details": {}}
    candidates = idx.notes_of("contradiction", "analysis") + [
        n for n in idx.notes if "contradict" in n.text.lower() or "تناقض" in n.text
    ]
    detected = []
    for c in items:
        aliases = [c.get("id", ""), c.get("description", "")] + list(c.get("aliases") or [])
        hit = False
        path = None
        for n in candidates + idx.notes:
            blob = n.text
            if alias_hit(aliases, blob, threshold=threshold) or any(
                similarity(a, n.title_guess) >= threshold for a in aliases if a
            ):
                hit = True
                path = n.path
                break
            for rid in c.get("related_ids") or []:
                if rid and rid in n.text:
                    hit = True
                    path = n.path
                    break
            if hit:
                break
        if hit:
            detected.append({"gt_id": c["id"], "path": path})
    score = len(detected) / len(items)
    return {
        "id": "M06",
        "score": _clip(score),
        "raw": {"detected": len(detected), "total": len(items)},
        "details": {
            "detected": detected,
            "missed": [c["id"] for c in items if c["id"] not in {d["gt_id"] for d in detected}],
        },
    }


def score_missing_evidence(gt: dict, idx: VaultIndex, threshold: float) -> dict:
    items = gt.get("missing_evidence") or gt.get("known_gaps") or []
    if not items:
        return {"id": "M07", "score": 1.0, "raw": {}, "details": {}}
    search_notes = [
        n
        for n in idx.notes
        if n.path.endswith("Coverage-Ledger.md")
        or n.zone in ("06-Outputs", "07-Cold-Case", "00-Scaffold")
        or "gap" in n.text.lower()
        or "فجوة" in n.text
        or "missing" in n.text.lower()
    ]
    blob_all = "\n".join(n.text for n in (search_notes or idx.notes))
    declared = []
    for g in items:
        aliases = [g.get("id", ""), g.get("description", "")] + list(g.get("aliases") or [])
        # also try significant tokens from description (gap phrases)
        desc = g.get("description") or ""
        tokens = [t for t in re.split(r"\W+", desc) if len(t) >= 5]
        phrase_ok = False
        if desc and normalize(desc) in normalize(blob_all):
            phrase_ok = True
        elif tokens:
            # require at least 2 distinctive tokens present
            present = sum(1 for t in tokens if normalize(t) in normalize(blob_all))
            phrase_ok = present >= min(2, len(tokens))
        if (
            alias_hit(aliases, blob_all, threshold=max(0.5, threshold - 0.05))
            or any(normalize(a) in normalize(blob_all) for a in aliases if a and len(a) > 3)
            or phrase_ok
        ):
            declared.append(g["id"])
    score = len(declared) / len(items)
    return {
        "id": "M07",
        "score": _clip(score),
        "raw": {"declared": len(declared), "total": len(items)},
        "details": {"declared": declared, "missed": [g["id"] for g in items if g["id"] not in declared]},
    }


def score_false_inference(gt: dict, idx: VaultIndex) -> dict:
    blob = idx.all_text_blob()
    hits = []
    forbidden = list(gt.get("forbidden_inferences") or [])
    for fi in forbidden:
        patterns = list(fi.get("match_patterns") or [])
        # Prefer explicit match_patterns; description alone is often instructional and causes false hits
        if not patterns:
            patterns = [fi.get("description", "")]
        # Skip very generic id tokens
        hit = False
        for pat in patterns:
            if not pat or len(str(pat).strip()) < 4:
                continue
            if not any_pattern_hit(blob, [pat]):
                continue
            # Negation window: if pattern appears only inside "do not / must not / never / not claim" clauses, skip
            nb = normalize(blob)
            np_ = normalize(pat)
            idx = nb.find(np_) if np_ else -1
            if idx >= 0:
                window = nb[max(0, idx - 40) : idx + len(np_) + 20]
                if any(
                    neg in window
                    for neg in (
                        "do not",
                        "dont",
                        "must not",
                        "never",
                        "not claim",
                        "not assert",
                        "not invent",
                        "not mark",
                        "without claiming",
                        "unestablished",
                        "not established",
                        "unsupported",
                        "out of scope",
                    )
                ):
                    continue
            hit = True
            break
        if hit:
            hits.append({"type": "inference", "id": fi.get("id"), "description": fi.get("description")})
    for fe in gt.get("forbidden_entities") or []:
        name = fe.get("name") or ""
        if name and normalize(name) in normalize(blob):
            # avoid matching inside ground-truth filenames etc. — vault only already
            hits.append({"type": "entity", "name": name, "reason": fe.get("reason")})
    if gt.get("group_entity_only"):
        # heuristic: many person notes with invented look — flag if Persons victims named beyond GT entities
        allowed = {normalize(e.get("name", "")) for e in (gt.get("entities") or [])}
        for n in idx.notes_of("person"):
            role = str(n.frontmatter.get("role") or "").lower()
            if role in ("victim", "passenger", "crew", "missing-person"):
                nm = normalize(n.title_guess)
                if nm and nm not in allowed and n.title_guess not in allowed:
                    # only flag if GT provided entity allow-list
                    if allowed:
                        hits.append({"type": "invented_person", "path": n.path, "name": n.title_guess})

    total = max(1, len(forbidden) + len(gt.get("forbidden_entities") or []) + (1 if gt.get("group_entity_only") else 0))
    # rate relative to forbidden item count, but each hit counts
    rate = _clip(len(hits) / total)
    score = _clip(1.0 - rate)
    return {"id": "M08", "score": score, "raw": {"hits": len(hits), "total_forbidden_units": total, "rate": rate}, "details": hits}


def score_confirmation_bias(gt: dict, idx: VaultIndex, threshold: float) -> dict:
    hyps = idx.notes_of("hypothesis") + [n for n in idx.notes if n.zone.startswith("03-Hypotheses")]
    primaries = []
    for n in hyps:
        kind = str(n.frontmatter.get("hypothesis-kind") or n.frontmatter.get("hypothesis_kind") or "").lower()
        if kind == "primary" or "/Primary/" in n.path.replace("\\", "/"):
            primaries.append(n)
    if primaries:
        with_counter = 0
        for p in primaries:
            c = p.frontmatter.get("counter-hypothesis") or p.frontmatter.get("counter_hypothesis")
            if c and (
                any(resolve_link(x, idx.known_names) for x in _as_list(c))
            ):
                with_counter += 1
        c1 = with_counter / len(primaries)
    else:
        c1 = 1.0 if not any(h.get("kind") == "primary" for h in (gt.get("hypotheses") or [])) else 0.0

    unsupported = 0
    conclusive_like = 0
    for p in primaries:
        level = str(p.frontmatter.get("support-level") or p.frontmatter.get("support_level") or "").lower()
        if level in ("strong", "conclusive"):
            conclusive_like += 1
            sup = p.frontmatter.get("supporting-notes") or p.frontmatter.get("supporting_notes") or []
            if not sup:
                unsupported += 1
    c2 = 1.0 if conclusive_like == 0 else 1.0 - (unsupported / conclusive_like)

    required_kinds = {h.get("kind") for h in (gt.get("hypotheses") or []) if h.get("required", True)}
    present_kinds = set()
    for n in hyps:
        kind = str(n.frontmatter.get("hypothesis-kind") or n.frontmatter.get("hypothesis_kind") or "").lower()
        if kind:
            present_kinds.add(kind)
    need = required_kinds & {"primary", "alternative", "counter"}
    c3 = 1.0
    if need:
        c3 = len(need & present_kinds) / len(need)

    rejected = [n for n in hyps if str(n.frontmatter.get("hypothesis-kind") or "").lower() == "rejected" or n.status == "rejected"]
    if rejected:
        with_reason = 0
        for n in rejected:
            rejects = n.frontmatter.get("rejects")
            if rejects or "سبب" in n.body or "reason" in n.body.lower():
                with_reason += 1
        c4 = with_reason / len(rejected)
    else:
        c4 = 1.0

    score = 0.35 * c1 + 0.30 * c2 + 0.20 * c3 + 0.15 * c4
    return {
        "id": "M09",
        "score": _clip(score),
        "raw": {"counters": c1, "no_unsupported_conclusive": c2, "multi_hyp": c3, "reject_reasons": c4},
        "details": {},
    }


def score_report_traceability(gt: dict, idx: VaultIndex, threshold: float) -> dict:
    claims = gt.get("report_must_cite") or []
    reports = list_report_notes(idx)
    # ignore pure scaffold placeholders
    reports = [r for r in reports if r.type in ("case-report", "court-file", "briefing", "cold-case-report", "recommendation", "") or "report" in r.path.lower() or "court" in r.path.lower()]
    if not claims:
        # if no GT claims, score presence of any report with ≥1 wikilink
        if not reports:
            return {"id": "M10", "score": 0.0, "raw": {"reports": 0}, "details": {"note": "no report notes"}}
        with_links = sum(1 for r in reports if extract_wikilinks(r.text))
        return {"id": "M10", "score": _clip(with_links / len(reports)), "raw": {"reports": len(reports), "with_links": with_links}, "details": {}}

    if not reports:
        return {"id": "M10", "score": 0.0, "raw": {}, "details": {"missed": [c["id"] for c in claims]}}

    blob = "\n".join(r.text for r in reports)
    traced = []
    for c in claims:
        claim = c.get("claim", "") or ""
        claim_present = (
            similarity(claim, blob[:8000]) >= threshold
            or normalize(claim) in normalize(blob)
            or alias_hit([claim, c.get("id", "")], blob, threshold=max(0.5, threshold - 0.05))
        )
        if not claim_present and claim:
            # token overlap fallback for short factual claims
            toks = [t for t in re.split(r"\W+", claim) if len(t) >= 4]
            if toks:
                hit = sum(1 for t in toks if normalize(t) in normalize(blob))
                claim_present = hit >= max(1, min(2, len(toks)))
        if not claim_present:
            continue
        must_ids = c.get("must_link_evidence_ids") or []
        if not must_ids:
            if extract_wikilinks(blob):
                traced.append(c["id"])
            continue
        # softer: any required evidence id appears in report text/links
        ok = any(eid in blob for eid in must_ids)
        if ok:
            traced.append(c["id"])
    score = len(traced) / len(claims)
    return {
        "id": "M10",
        "score": _clip(score),
        "raw": {"traced": len(traced), "total": len(claims)},
        "details": {"traced": traced, "missed": [c["id"] for c in claims if c["id"] not in traced]},
    }


def score_readiness_gate(
    gt: dict,
    idx: VaultIndex,
    skill_audit: Optional[dict] = None,
    violation_cap: int = 5,
) -> dict:
    violations = []
    # strong primary without support
    for n in idx.notes_of("hypothesis"):
        kind = str(n.frontmatter.get("hypothesis-kind") or n.frontmatter.get("hypothesis_kind") or "").lower()
        level = str(n.frontmatter.get("support-level") or n.frontmatter.get("support_level") or "").lower()
        if kind == "primary" and level in ("strong", "conclusive"):
            sup = n.frontmatter.get("supporting-notes") or n.frontmatter.get("supporting_notes") or []
            if not sup:
                violations.append({"code": "strong_primary_without_support", "path": n.path})
            counter = n.frontmatter.get("counter-hypothesis") or n.frontmatter.get("counter_hypothesis")
            if not counter:
                violations.append({"code": "primary_without_counter", "path": n.path})
        elif kind == "primary":
            counter = n.frontmatter.get("counter-hypothesis") or n.frontmatter.get("counter_hypothesis")
            if not counter or not any(resolve_link(x, idx.known_names) for x in _as_list(counter)):
                violations.append({"code": "primary_without_counter", "path": n.path})

    for n in idx.notes:
        if is_evidence_note(n) and n.status == "verified":
            archival = is_archival_evidence(n)
            ok = evidence_has_provenance(n) if archival else evidence_has_coc(n, idx.known_names)
            if not ok and source_kind_of(n) in ARCHIVAL_KINDS:
                ok = evidence_has_provenance(n)
            if not ok:
                violations.append({"code": "verified_without_source", "path": n.path})
        if n.zone == "01-Evidence" and n.status == "exploration":
            violations.append({"code": "exploration_in_evidence", "path": n.path})

    # court file while readiness fails
    court = [n for n in list_report_notes(idx) if "court" in n.path.lower() or n.type == "court-file"]
    rexp = gt.get("readiness_expectations") or {}
    if court and rexp.get("allow_final_report") is False:
        violations.append({"code": "court_file_against_expectation", "path": court[0].path})

    if skill_audit:
        for issue in skill_audit.get("issues") or []:
            if issue.get("severity") == "critical":
                violations.append({"code": "skill_audit_critical", "msg": issue.get("msg"), "path": issue.get("path")})

    raw = min(1.0, len(violations) / max(violation_cap, 1))
    score = _clip(1.0 - raw)
    return {"id": "M11", "score": score, "raw": {"violations": len(violations), "cap": violation_cap}, "details": violations[:50]}


def score_conclusion_calibration(gt: dict, idx: VaultIndex, threshold: float, matrix: dict) -> dict:
    truth = gt.get("truth_status") or "unknown"
    canonical = gt.get("canonical_conclusion") or ""
    # find favored primary
    primaries = []
    for n in idx.notes_of("hypothesis"):
        kind = str(n.frontmatter.get("hypothesis-kind") or n.frontmatter.get("hypothesis_kind") or "").lower()
        if kind == "primary":
            primaries.append(n)
    if not primaries:
        # look at reports
        reports = list_report_notes(idx)
        if truth in ("unknown", "cold") and not reports:
            return {"id": "M12", "score": 0.6, "raw": {"truth": truth, "note": "no primary"}, "details": {}}
        if truth in ("unknown", "cold"):
            return {"id": "M12", "score": 0.7, "raw": {"truth": truth}, "details": {}}
        return {"id": "M12", "score": 0.2, "raw": {"truth": truth, "note": "missing primary"}, "details": {}}

    # pick primary most similar to canonical or first
    best = primaries[0]
    best_s = 0.0
    for p in primaries:
        s = similarity(canonical, p.title_guess + " " + p.body[:300]) if canonical else 0.5
        if s > best_s:
            best, best_s = p, s
    level = str(best.frontmatter.get("support-level") or best.frontmatter.get("support_level") or "weak").lower()
    status = best.status

    # trap hypotheses
    trap_ids = [h for h in (gt.get("hypotheses") or []) if h.get("is_trap")]
    for th in trap_ids:
        n, s = _match_hypothesis(th, idx, threshold)
        if n and str(n.frontmatter.get("hypothesis-kind") or "").lower() == "primary":
            lvl = str(n.frontmatter.get("support-level") or "").lower()
            if lvl in ("strong", "conclusive") or n.status == "verified":
                return {
                    "id": "M12",
                    "score": 0.0,
                    "raw": {"truth": truth, "trap_accepted": True, "path": n.path},
                    "details": {},
                }

    if truth == "false_trap":
        # favored conclusion should be rejected / not conclusive
        if level in ("conclusive", "strong") and status != "rejected":
            return {"id": "M12", "score": 0.0, "raw": {"truth": truth, "level": level}, "details": {}}
        return {"id": "M12", "score": 1.0, "raw": {"truth": truth, "level": level}, "details": {}}

    allowed = matrix.get(truth) or matrix.get("unknown") or ["weak", "moderate"]
    if level in allowed or (truth in ("unknown", "cold") and status in ("cause-unknown",) or level == "cause-unknown"):
        score = 1.0
    else:
        # adjacency
        order = ["weak", "moderate", "strong", "conclusive"]
        if level in order and any(a in order for a in allowed):
            li = order.index(level)
            ai = min(abs(li - order.index(a)) for a in allowed if a in order)
            if ai == 1:
                score = 0.5
            elif li > max(order.index(a) for a in allowed if a in order):
                score = 0.0  # overconfident
            else:
                score = 0.6  # underconfident
        else:
            score = 0.3

    return {
        "id": "M12",
        "score": _clip(score),
        "raw": {"truth": truth, "level": level, "path": best.path, "allowed": allowed},
        "details": {},
    }


def weighted_case_score(metrics: dict[str, dict], weights: dict[str, float]) -> float:
    num = 0.0
    den = 0.0
    key_map = {
        "evidence_coverage": "evidence_coverage",
        "source_provenance_completeness": "source_provenance_completeness",
        "hypothesis_coverage": "hypothesis_coverage",
        "counter_hypothesis_quality": "counter_hypothesis_quality",
        "timeline_reconstruction": "timeline_reconstruction",
        "contradiction_detection": "contradiction_detection",
        "missing_evidence_detection": "missing_evidence_detection",
        "false_inference_rate": "false_inference_rate",
        "confirmation_bias_resistance": "confirmation_bias_resistance",
        "report_traceability": "report_traceability",
        "readiness_gate_violations": "readiness_gate_violations",
        "final_conclusion_calibration": "final_conclusion_calibration",
    }
    for k, w in weights.items():
        m = metrics.get(k) or metrics.get(key_map.get(k, k))
        if not m:
            continue
        num += float(w) * float(m.get("score", 0.0))
        den += float(w)
    return _clip(num / den) if den else 0.0
