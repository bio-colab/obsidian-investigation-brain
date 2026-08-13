from __future__ import annotations

import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None  # type: ignore

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n?", re.DOTALL)
WIKILINK_RE = re.compile(r"\[\[([^\]]+?)(?:\|[^\]]+)?\]\]")

EVIDENCE_TYPES = {
    "physical-evidence",
    "digital-evidence",
    "testimonial",
    "documentary",
    "financial-record",
    "wiretap-evidence",
    "audio-visual-evidence",
    "data-analysis",
    "informant-testimony",
}

ARCHIVAL_KINDS = {
    "public-archive",
    "archival",
    "official-archive",
    "declassified",
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
    "90-Reference-Sources",
    "99-Attachments",
)


@dataclass
class Note:
    path: str
    zone: str
    frontmatter: dict[str, Any]
    body: str
    text: str

    @property
    def type(self) -> str:
        return str(self.frontmatter.get("type", "")).strip().lower()

    @property
    def status(self) -> str:
        return str(self.frontmatter.get("status", "")).strip().lower()

    @property
    def stem(self) -> str:
        return Path(self.path).stem

    @property
    def title_guess(self) -> str:
        for line in self.body.splitlines():
            line = line.strip()
            if line.startswith("#"):
                return re.sub(r"^#+\s*", "", line).strip()
        return self.stem


@dataclass
class VaultIndex:
    root: Path
    notes: list[Note] = field(default_factory=list)
    by_stem: dict[str, list[Note]] = field(default_factory=lambda: defaultdict(list))
    by_type: dict[str, list[Note]] = field(default_factory=lambda: defaultdict(list))
    known_names: set[str] = field(default_factory=set)

    def notes_of(self, *types: str) -> list[Note]:
        out: list[Note] = []
        for t in types:
            out.extend(self.by_type.get(t.lower(), []))
        return out

    def all_text_blob(self) -> str:
        return "\n".join(n.text for n in self.notes)


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
    data: dict[str, Any] = {}
    if yaml is not None:
        try:
            loaded = yaml.safe_load(m.group(1)) or {}
            if isinstance(loaded, dict):
                data = loaded
        except Exception:
            data = {}
    body = text[m.end() :]
    return data, body


def collect_known_names(root: Path) -> set[str]:
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


def resolve_link(link: Any, known: set[str]) -> bool:
    if link is None:
        return False
    pure = str(link).strip().strip("[]")
    pure = pure.split("#")[0].split("|")[0].strip()
    if not pure:
        return False
    if pure in known or pure.replace("\\", "/") in known:
        return True
    last = pure.split("/")[-1]
    return last in known


def extract_wikilinks(text: str) -> list[str]:
    out = []
    for m in WIKILINK_RE.finditer(text or ""):
        pure = m.group(1).strip().split("#")[0].split("|")[0].strip()
        if pure:
            out.append(pure)
    return out


def load_vault(vault: Path) -> VaultIndex:
    vault = Path(vault)
    if not vault.is_dir():
        raise FileNotFoundError(f"Vault not found: {vault}")
    idx = VaultIndex(root=vault, known_names=collect_known_names(vault))
    for md in sorted(vault.rglob("*.md")):
        if any(part.startswith(".") for part in md.parts):
            continue
        try:
            rel = md.relative_to(vault).as_posix()
        except ValueError:
            continue
        try:
            text = md.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        fm, body = parse_frontmatter(text)
        note = Note(
            path=rel,
            zone=detect_zone(rel),
            frontmatter=fm,
            body=body,
            text=text,
        )
        idx.notes.append(note)
        idx.by_stem[note.stem].append(note)
        if note.type:
            idx.by_type[note.type].append(note)
    return idx


def is_evidence_note(note: Note) -> bool:
    if note.type in EVIDENCE_TYPES:
        return True
    if note.zone == "01-Evidence" and note.type not in ("chain-of-custody", "source-provenance"):
        return True
    return False


def evidence_has_coc(note: Note, known: set[str]) -> bool:
    coc = note.frontmatter.get("chain-of-custody") or note.frontmatter.get("chain_of_custody")
    if coc:
        if isinstance(coc, list):
            return any(resolve_link(c, known) for c in coc)
        return resolve_link(coc, known)
    # body pointer
    if "chain-of-custody" in note.body.lower() or "سلسلة الحفظ" in note.body:
        links = extract_wikilinks(note.body)
        if any(resolve_link(l, known) for l in links):
            return True
    return False


def evidence_has_provenance(note: Note) -> bool:
    sp = note.frontmatter.get("source-provenance") or note.frontmatter.get("source_provenance")
    if isinstance(sp, dict):
        archive = sp.get("archive")
        rid = sp.get("record-id") or sp.get("record_id") or sp.get("url")
        return bool(archive and rid)
    if isinstance(sp, str) and sp.strip():
        return True
    sk = str(note.frontmatter.get("source-kind") or note.frontmatter.get("source_kind") or "").lower()
    if sk in ARCHIVAL_KINDS and ("source-provenance" in note.text.lower() or "archive:" in note.text.lower()):
        # weak body presence
        return "archive:" in note.text.lower() and (
            "record-id" in note.text.lower() or "url:" in note.text.lower() or "http" in note.text.lower()
        )
    return False


def source_kind_of(note: Note) -> str:
    return str(note.frontmatter.get("source-kind") or note.frontmatter.get("source_kind") or "").strip().lower()


def is_archival_evidence(note: Note, gt_source_kind: Optional[str] = None) -> bool:
    sk = source_kind_of(note) or (gt_source_kind or "")
    return sk in ARCHIVAL_KINDS


def list_report_notes(idx: VaultIndex) -> list[Note]:
    return [n for n in idx.notes if n.zone == "06-Outputs" or n.path.startswith("06-Outputs/")]


def status_histogram(idx: VaultIndex) -> dict[str, int]:
    c: Counter[str] = Counter()
    for n in idx.notes:
        c[n.status or "(missing)"] += 1
    return dict(c)
