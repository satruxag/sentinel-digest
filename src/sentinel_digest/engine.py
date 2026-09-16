"""Motore: carica il profilo, raccoglie, filtra, deduplica, notifica."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from .filtering import Match, KeywordFilter
from .models import Item
from .notify import build_notifier, render_html, render_text
from .sources import build_source
from .storage import Store

log = logging.getLogger(__name__)

DEFAULT_CONFIG = "config/config.yaml"


@dataclass
class RunResult:
    profile: str
    fetched: int = 0
    matched: int = 0
    new: int = 0
    sent: int = 0
    errors: list[str] = field(default_factory=list)
    matches: list[Match] = field(default_factory=list)

    def summary(self) -> str:
        return (
            f"profilo={self.profile} scaricati={self.fetched} filtrati={self.matched} "
            f"nuovi={self.new} notificati={self.sent} errori={len(self.errors)}"
        )


def load_config(path: str | Path) -> dict:
    """YAML se disponibile, altrimenti JSON. Espande ${VAR} dall'ambiente."""
    from .envsubst import expand_env

    p = Path(path)
    text = p.read_text(encoding="utf-8")
    try:
        import yaml  # type: ignore

        data = yaml.safe_load(text) or {}
    except ImportError:
        import json

        data = json.loads(text)
    return expand_env(data)


def collect(config: dict) -> tuple[list[Item], list[str]]:
    items: list[Item] = []
    errors: list[str] = []
    for scfg in config.get("sources") or []:
        try:
            src = build_source(scfg)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"config fonte {scfg.get('name')}: {exc}")
            continue
        got = src.safe_fetch()
        if not got:
            errors.append(f"fonte {scfg.get('name')} senza item")
        items.extend(got)
    return items, errors


def run(config: dict, only_new: bool = True, dry_run: bool = False) -> RunResult:
    profile = config.get("profile", "default")
    store = Store(config.get("store", {}).get("path", f"data/{profile}.db"))
    res = RunResult(profile=profile)
    run_id = store.start_run()
    generated = datetime.now(timezone.utc)

    try:
        items, errs = collect(config)
        res.errors.extend(errs)
        res.fetched = len(items)
        log.info("scaricati %d item da %d fonti", len(items), len(config.get("sources") or []))

        flt = KeywordFilter(config)
        matches = flt.apply(items)
        res.matched = len(matches)
        log.info("filtrati %d item", len(matches))

        max_age = int((config.get("filter") or {}).get("max_age_days", 30))
        selected: list[Match] = []
        for m in matches:
            if m.item.published and m.item.age_days > max_age:
                continue
            if only_new and store.is_seen(m.item.uid):
                continue
            selected.append(m)

        res.new = len(selected)
        res.matches = selected
        log.info("nuovi da notificare: %d", len(selected))

        limit = int((config.get("digest") or {}).get("max_items", 40))
        to_send = selected[:limit]

        if not to_send and not (config.get("digest") or {}).get("send_empty", False):
            log.info("nessuna novita': notifica saltata")
            store.finish_run(run_id, res.fetched, res.matched, 0, "; ".join(res.errors))
            return res

        text = render_text(to_send, profile, generated, config.get("base_url", ""))
        html = render_html(to_send, profile, generated, config.get("base_url", ""))

        if dry_run:
            print(text)
            store.finish_run(run_id, res.fetched, res.matched, 0, "; ".join(res.errors))
            return res

        sent_ok = 0
        for ncfg in config.get("notify") or []:
            try:
                notifier = build_notifier(ncfg)
                if notifier.send(profile, to_send, generated, html, text):
                    sent_ok += 1
            except Exception as exc:  # noqa: BLE001
                res.errors.append(f"notify {ncfg.get('kind')}: {exc}")
                log.warning("notify %s fallito: %s", ncfg.get("kind"), exc)

        res.sent = len(to_send) if sent_ok else 0
        for m in to_send:
            store.mark(m.item, score=m.score, sent=bool(sent_ok))
        store.finish_run(run_id, res.fetched, res.matched, res.sent, "; ".join(res.errors))
        return res
    finally:
        store.close()
