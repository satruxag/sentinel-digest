"""Interfaccia fonte + registro. Ogni fonte ritorna una lista di Item."""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Iterable

from ..models import Item

log = logging.getLogger(__name__)

SOURCES: dict[str, type["Source"]] = {}


def register(cls: type["Source"]) -> type["Source"]:
    SOURCES[cls.kind] = cls
    return cls


class Source(ABC):
    """Una fonte di avvisi pubblici."""

    kind: str = "base"

    def __init__(self, name: str, options: dict | None = None):
        self.name = name
        self.options = options or {}

    @abstractmethod
    def fetch(self) -> Iterable[Item]:
        """Ritorna gli item correnti della fonte."""

    def safe_fetch(self) -> list[Item]:
        """Non fa mai fallire l'intera run per colpa di una singola fonte."""
        try:
            items = list(self.fetch())
            log.info("fonte %s (%s): %d item", self.name, self.kind, len(items))
            return items
        except Exception as exc:  # noqa: BLE001
            log.warning("fonte %s (%s) fallita: %s", self.name, self.kind, exc)
            return []


def build_source(cfg: dict) -> Source:
    kind = cfg.get("kind", "rss")
    cls = SOURCES.get(kind)
    if cls is None:
        raise ValueError(f"tipo di fonte sconosciuto: {kind!r} (disponibili: {sorted(SOURCES)})")
    return cls(name=cfg.get("name", kind), options=cfg)
