"""Modello dati comune a tutte le fonti."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any


@dataclass
class Item:
    """Un avviso/bando normalizzato, indipendente dalla fonte."""

    source: str
    title: str
    url: str
    published: datetime | None = None
    summary: str = ""
    region: str = ""
    tags: list[str] = field(default_factory=list)
    raw: dict[str, Any] = field(default_factory=dict)

    @property
    def uid(self) -> str:
        """Identificatore stabile: stessa notizia -> stesso uid tra le run."""
        basis = f"{self.source}|{self.url}|{self.title}".encode("utf-8")
        return hashlib.sha256(basis).hexdigest()[:32]

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["published"] = self.published.isoformat() if self.published else None
        d["uid"] = self.uid
        d.pop("raw", None)
        return d

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "Item":
        pub = d.get("published")
        return cls(
            source=d["source"],
            title=d["title"],
            url=d["url"],
            published=datetime.fromisoformat(pub) if pub else None,
            summary=d.get("summary", ""),
            region=d.get("region", ""),
            tags=list(d.get("tags") or []),
        )

    @property
    def age_days(self) -> float:
        if not self.published:
            return 0.0
        now = datetime.now(timezone.utc)
        pub = self.published
        if pub.tzinfo is None:
            pub = pub.replace(tzinfo=timezone.utc)
        return max(0.0, (now - pub).total_seconds() / 86400)


def parse_date(value: str | None) -> datetime | None:
    """Tollerante: accetta ISO, RFC822 e i formati usati dalle PA italiane."""
    if not value:
        return None
    value = value.strip()
    candidates = [
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
        "%d/%m/%Y %H:%M",
        "%d/%m/%Y",
        "%a, %d %b %Y %H:%M:%S %z",
        "%a, %d %b %Y %H:%M:%S %Z",
    ]
    for fmt in candidates:
        try:
            dt = datetime.strptime(value, fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt
        except ValueError:
            continue
    try:
        from email.utils import parsedate_to_datetime

        dt = parsedate_to_datetime(value)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except Exception:
        return None
