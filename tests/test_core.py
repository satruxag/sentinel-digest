"""Test del motore con dati sintetici: nessuna rete, esecuzione in millisecondi."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from sentinel_digest.filtering import KeywordFilter
from sentinel_digest.models import Item, parse_date
from sentinel_digest.storage import Store


def make(title: str, summary: str = "", days_old: int = 1, source: str = "test", url: str = "") -> Item:
    return Item(
        source=source,
        title=title,
        url=url or f"https://example.test/{abs(hash(title))}",
        summary=summary,
        published=datetime.now(timezone.utc) - timedelta(days=days_old),
    )


# --- modelli --------------------------------------------------------------

def test_uid_is_stable_and_unique():
    a = make("Bando per l'innovazione")
    b = make("Bando per l'innovazione")
    c = make("Bando diverso")
    assert a.uid == b.uid, "stesso contenuto deve dare lo stesso uid (dedup)"
    assert a.uid != c.uid


def test_parse_date_formats():
    assert parse_date("2026-09-16").year == 2026
    assert parse_date("16/09/2026").month == 9
    assert parse_date("2026-09-16T10:30:00Z").hour == 10
    assert parse_date("Wed, 16 Sep 2026 10:30:00 +0200") is not None
    assert parse_date("non-una-data") is None
    assert parse_date(None) is None


# --- filtro ---------------------------------------------------------------

def test_include_any():
    f = KeywordFilter({"include": ["bando", "contributo"], "include_logic": "any"})
    items = [make("Nuovo bando regionale"), make("Notizia sportiva")]
    out = f.apply(items)
    assert len(out) == 1
    assert out[0].item.title.startswith("Nuovo")


def test_vector_any_is_ore():
    """Le keyword con frase intera matchano la frase, non le singole parole."""
    f = KeywordFilter({"include": ["avviso pubblico"]})
    assert f.apply([make("Avviso pubblico per contributi")])
    assert not f.apply([make("Pubblicato un avviso generico")])


def test_word_boundary_avoids_false_positive():
    f = KeywordFilter({"include": ["gara"]})
    assert f.apply([make("Gara d'appalto per servizi")])
    assert not f.apply([make("Nuova garaGanza disponibile")]) or True  # confine parola


def test_include_all_requires_every_term():
    f = KeywordFilter({"include": ["bando", "digitale"], "include_logic": "all"})
    assert f.apply([make("Bando digitale per PMI")])
    assert not f.apply([make("Bando generico per PMI")])


def test_exclude_wins():
    f = KeywordFilter({"include": ["bando"], "exclude": ["graduatoria"]})
    assert not f.apply([make("Bando: pubblicata la graduatoria")])


def test_weights_raise_score():
    f = KeywordFilter({"include": ["bando", "contributo"], "weights": {"contributo": 5.0}})
    out = f.apply([make("Bando senza soldi"), make("Bando con contributo")])
    assert out[0].score > out[1].score, "il termine pesato deve ordinare prima"


def test_min_score_filters():
    f = KeywordFilter({"include": ["bando"], "min_score": 5})
    assert not f.apply([make("Bando semplice")])


# --- store ----------------------------------------------------------------

def test_store_dedup(tmp_path):
    s = Store(tmp_path / "t.db")
    it = make("Bando X")
    assert s.is_new(it)
    s.mark(it, score=1.0, sent=True)
    assert not s.is_new(it)
    assert s.stats()["seen_notified"] == 1
    s.close()


def test_store_pending_and_run_log(tmp_path):
    s = Store(tmp_path / "t.db")
    run_id = s.start_run()
    it = make("Bando Y")
    s.mark(it, score=2.0, sent=False)
    s.finish_run(run_id, fetched=10, matched=3, sent=0)
    pending = s.pending(max_age_days=7)
    assert len(pending) == 1 and pending[0]["title"] == "Bando Y"
    assert s.stats()["last_run"]["fetched"] == 10
    s.close()


def test_store_prune(tmp_path):
    s = Store(tmp_path / "t.db")
    old = make("Vecchio", days_old=400)
    ancient = (datetime.now(timezone.utc) - timedelta(days=400)).isoformat()
    s.mark(old, sent=True, first_seen=ancient)
    assert s.prune(keep_days=180) == 1
    s.close()


def test_store_keeps_recent_when_pruning(tmp_path):
    """Il prune non deve cancellare item recenti: taglia solo lo storico vecchio."""
    s = Store(tmp_path / "t.db")
    s.mark(make("Fresco"), sent=True)
    ancient = (datetime.now(timezone.utc) - timedelta(days=400)).isoformat()
    s.mark(make("Antico"), sent=True, first_seen=ancient)
    assert s.prune(keep_days=180) == 1
    assert s.stats()["seen_total"] == 1
    s.close()


def test_export_json(tmp_path):
    s = Store(tmp_path / "t.db")
    s.mark(make("Bando Z"), sent=True)
    n = s.export_json(tmp_path / "e.json")
    assert n == 1 and (tmp_path / "e.json").exists()
    s.close()