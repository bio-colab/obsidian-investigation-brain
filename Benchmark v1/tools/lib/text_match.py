from __future__ import annotations

import re
import unicodedata
from difflib import SequenceMatcher
from typing import Iterable, Optional


def normalize(text: str) -> str:
    if not text:
        return ""
    t = unicodedata.normalize("NFKC", str(text)).lower().strip()
    t = re.sub(r"\s+", " ", t)
    t = re.sub(r"[^\w\s\-./:]", "", t, flags=re.UNICODE)
    return t


def token_set(text: str) -> set[str]:
    return {tok for tok in re.split(r"[\s_/.\-]+", normalize(text)) if len(tok) > 1}


def similarity(a: str, b: str) -> float:
    na, nb = normalize(a), normalize(b)
    if not na or not nb:
        return 0.0
    if na == nb:
        return 1.0
    if na in nb or nb in na:
        return max(0.85, SequenceMatcher(None, na, nb).ratio())
    # hybrid: sequence + token Jaccard
    seq = SequenceMatcher(None, na, nb).ratio()
    ta, tb = token_set(na), token_set(nb)
    jacc = (len(ta & tb) / len(ta | tb)) if (ta or tb) else 0.0
    return 0.55 * seq + 0.45 * jacc


def best_match(
    query: str,
    candidates: Iterable[str],
    threshold: float = 0.55,
) -> tuple[Optional[str], float]:
    best_s, best_score = None, 0.0
    for c in candidates:
        s = similarity(query, c)
        if s > best_score:
            best_s, best_score = c, s
    if best_score >= threshold:
        return best_s, best_score
    return None, best_score


def any_pattern_hit(text: str, patterns: Iterable[str]) -> bool:
    blob = normalize(text)
    for p in patterns:
        p = (p or "").strip()
        if not p:
            continue
        # support simple substring or /regex/
        if p.startswith("/") and p.endswith("/") and len(p) > 2:
            try:
                if re.search(p[1:-1], blob, flags=re.I):
                    return True
            except re.error:
                if normalize(p[1:-1]) in blob:
                    return True
        elif normalize(p) in blob:
            return True
    return False


def alias_hit(query_aliases: Iterable[str], haystack: str, threshold: float = 0.72) -> bool:
    h = haystack or ""
    for a in query_aliases:
        if not a:
            continue
        if normalize(a) and normalize(a) in normalize(h):
            return True
        if similarity(a, h) >= threshold:
            return True
    return False
