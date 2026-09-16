"""Filtro keyword: include/esclude con supporto a frasi e regex."""

from __future__ import annotations

import re
from dataclasses import dataclass

from ..models import Item


@dataclass
class Match:
    item: Item
    score: float
    hits: list[str]


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower())


def _compile_terms(terms: list[str]) -> list[tuple[str, re.Pattern]]:
    out = []
    for t in terms:
        t = t.strip()
        if not t:
            continue
        if t.startswith("re:"):
            out.append((t[3:], re.compile(t[3:], re.I)))
        elif " " in t:
            out.append((t, re.compile(re.escape(t), re.I)))
        else:
            # parola singola: match sul confine di parola (evita "gas" in "gasolio")
            out.append((t, re.compile(rf"\b{re.escape(t)}\b", re.I)))
    return out


class KeywordFilter:
    def __init__(self, config: dict):
        f = config.get("filter", config)
        self.include = _compile_terms(list(f.get("include") or []))
        self.exclude = _compile_terms(list(f.get("exclude") or []))
        self.include_logic = (f.get("include_logic") or "any").lower()
        self.weights: dict[str, float] = {
            str(k).lower(): float(v) for k, v in (f.get("weights") or {}).items()
        }
        self.min_score = float(f.get("min_score", 0))

    def match(self, item: Item) -> Match | None:
        haystack = _norm(f"{item.title} {item.summary} {' '.join(item.tags)}")

        for term, rx in self.exclude:
            if rx.search(haystack):
                return None

        hits: list[str] = []
        for term, rx in self.include:
            if rx.search(haystack):
                hits.append(term)

        if self.include:
            if self.include_logic == "all" and len(hits) < len(self.include):
                return None
            if self.include_logic == "any" and not hits:
                return None

        score = float(len(hits))
        for hit in hits:
            score += self.weights.get(hit.lower(), 0.0)
        score += self.weights.get(item.source.lower(), 0.0) * 0.5

        if score < self.min_score:
            return None
        return Match(item=item, score=score, hits=hits)

    def apply(self, items: list[Item]) -> list[Match]:
        matches = [m for m in (self.match(i) for i in items) if m]
        matches.sort(key=lambda m: (-m.score, -(m.item.published.timestamp() if m.item.published else 0)))
        return matches
