"""Citation span validation — CLAUSE's trust core (DEC-006).

A citation is VERIFIED only if it exists in the source policy text.
Matching is exact-substring after conservative normalization (whitespace collapse,
unicode quote/dash unification). We normalize both sides identically and map the
match back to a character span in the ORIGINAL text so the UI can highlight it.

Failed citations are returned with verified=False and span=None — the UI renders
them as rejected. They are never silently dropped (CLAUDE.md hard rule 2).
"""
from __future__ import annotations
import re

_TRANSLATE = str.maketrans({
    "\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"',
    "\u2013": "-", "\u2014": "-", "\u00a0": " ",
})


def _normalize(text: str) -> tuple[str, list[int]]:
    """Return normalized text and a map: normalized index -> original index."""
    text = text.translate(_TRANSLATE)
    out: list[str] = []
    index_map: list[int] = []
    prev_space = False
    for i, ch in enumerate(text):
        if ch.isspace():
            if prev_space:
                continue
            out.append(" ")
            index_map.append(i)
            prev_space = True
        else:
            out.append(ch.lower())
            index_map.append(i)
            prev_space = False
    return "".join(out), index_map


def find_span(source: str, quote: str) -> tuple[int, int] | None:
    """Locate `quote` in `source`; return (start, end) in ORIGINAL source coords, or None."""
    quote = quote.strip()
    if not quote:
        return None
    norm_src, idx_map = _normalize(source)
    norm_q, _ = _normalize(quote)
    norm_q = norm_q.strip()
    pos = norm_src.find(norm_q)
    if pos == -1:
        return None
    start = idx_map[pos]
    end_norm = pos + len(norm_q) - 1
    end = idx_map[end_norm] + 1
    return (start, end)


def validate_points(policy: str, points: list[dict]) -> list[dict]:
    """Annotate each decision point with verified/span. Order preserved."""
    validated = []
    for p in points:
        span = find_span(policy, str(p.get("citation", "")))
        validated.append({**p, "verified": span is not None, "span": list(span) if span else None})
    return validated
