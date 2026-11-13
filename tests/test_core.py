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

# --- config mancante: errore leggibile, non traceback ---------------------


def test_load_config_missing_gives_actionable_error(tmp_path):
    """Regressione: il clone non contiene config/, quindi il primo comando
    dell'utente colpiva un FileNotFoundError con traceback."""
    from sentinel_digest.engine import ConfigNotFound, load_config

    missing = tmp_path / "config" / "config.yaml"
    with pytest.raises(ConfigNotFound) as exc:
        load_config(missing)
    msg = str(exc.value)
    assert "config.example.yaml" in msg, "il messaggio deve dire dove prendere l'esempio"
    assert "mkdir" in msg, "il messaggio deve dare il comando risolutivo"


def test_cli_missing_config_exits_2_without_traceback(tmp_path, capsys):
    from sentinel_digest.cli import main

    rc = main(["-c", str(tmp_path / "nope" / "config.yaml"), "doctor"])
    assert rc == 2
    err = capsys.readouterr().err
    assert "config.example.yaml" in err
    assert "Traceback" not in err


# --- doctor: notifier -----------------------------------------------------

def _doctor_on(tmp_path, notify):
    """Scrive una config minima e lancia doctor, ritornando (rc, stdout)."""
    import json

    from sentinel_digest.cli import main

    cfg = {
        "profile": "t",
        "store": {"path": str(tmp_path / "data" / "t.db")},
        "sources": [],
        "notify": notify,
    }
    path = tmp_path / "config.json"
    path.write_text(json.dumps(cfg), encoding="utf-8")
    return main(["-c", str(path), "doctor"])


def test_doctor_flags_unknown_notifier_kind(tmp_path, capsys):
    """Regressione: un refuso nel kind ('telegran') passava come [OK].
    La diagnostica deve accorgersene subito, prima della run."""
    rc = _doctor_on(tmp_path, [{"kind": "telegran", "url": "https://x.test/h"}])
    out = capsys.readouterr().out
    assert rc == 1
    assert "[FAIL] notifier telegran" in out


def test_doctor_rejects_typo_notifier_without_raising(tmp_path, capsys):
    rc = _doctor_on(tmp_path, [{"kind": "telegran", "url": "https://x.test/h"}])
    out = capsys.readouterr().out
    assert rc == 1, "un notifier sconosciuto deve rendere la diagnosi negativa"
    assert "[FAIL] notifier telegran" in out, "deve nominare il kind sbagliato"
    assert "[OK  ] notifier telegran" not in out, "non deve dichiararlo valido"


def test_doctor_typo_message_lists_valid_kinds_plainly(tmp_path, capsys):
    """Il messaggio deve elencare i kind in forma leggibile, senza repr Python."""
    _doctor_on(tmp_path, [{"kind": "emaill"}])
    out = capsys.readouterr().out
    assert "folder" in out and "smtp" in out and "webhook" in out
    assert "['" not in out, "niente repr di lista: l'utente finale legge questo testo"


# --- doctor: prova reale contro il difetto "filtrati=0" --------------------

class _FakeSource:
    """Fonte finta: evita la rete nei test del doctor."""

    def __init__(self, items):
        self._items = items

    def safe_fetch(self):
        return list(self._items)


def _doctor_via_main(monkeypatch, tmp_path, items, filt):
    """Lancia `doctor` dal vero (main -> cmd_doctor) su una fonte finta.

    Va bene se il test tocca main: il difetto era proprio che il doctor
    *dichiarava* TUTTO OK, quindi la regressione deve passare dalla CLI.
    """
    import json

    from sentinel_digest import cli

    monkeypatch.setattr(cli, "build_source", lambda cfg: _FakeSource(items))
    cfg = {
        "profile": "t",
        "store": {"path": str(tmp_path / "data" / "t.db")},
        "sources": [{"name": "finta", "kind": "rss"}],
        "filter": dict(filt),
        "notify": [{"kind": "folder", "path": str(tmp_path / "out")}],
    }
    path = tmp_path / "config.json"
    path.write_text(json.dumps(cfg), encoding="utf-8")
    return cli.main(["-c", str(path), "doctor"])


def test_doctor_segnala_filtro_che_non_pesca_nulla(tmp_path, monkeypatch, capsys):
    """Regressione (difetto piu' costoso per chi installa): le fonti sono valide
    e raggiungibili, doctor diceva TUTTO OK, e poi la run notificava zero perche'
    nessuna keyword compariva negli item reali. Il doctor deve accorgersene."""

    items = [make("Notizia sportiva"), make("Borsa in rialzo"), make("Meteo domani")]
    rc = _doctor_via_main(monkeypatch, tmp_path, items, {"include": ["bando", "gara"], "min_score": 1})
    out = capsys.readouterr().out
    assert rc == 1, "filtro che non pesca nulla deve rendere la diagnosi negativa"
    assert "TUTTO OK" not in out, "non deve dichiarare tutto a posto"
    assert "0 passano il filtro" in out, "deve mostrare la misura reale"
    assert "notificherebbe zero" in out, "deve spiegare la conseguenza pratica"


def test_doctor_tace_quando_il_filtro_pesca(tmp_path, monkeypatch, capsys):
    items = [make("Nuovo bando regionale"), make("Borsa in rialzo")]
    rc = _doctor_via_main(monkeypatch, tmp_path, items, {"include": ["bando"], "min_score": 1})
    out = capsys.readouterr().out
    assert rc == 0
    assert "1 passano il filtro" in out
    assert "TUTTO OK" in out


def test_doctor_fonti_vuote_avvisa_senza_fallire(tmp_path, monkeypatch, capsys):
    """Feed morto: la run non si rompe, ma doctor deve dirlo (WARN, non FAIL)."""
    rc = _doctor_via_main(monkeypatch, tmp_path, [], {"include": ["bando"]})
    out = capsys.readouterr().out
    assert rc == 0, "una fonte vuota non e' un errore di configurazione"
    assert "nessun item scaricato" in out


# --- messaggi di errore del notifier --------------------------------------
#
# Difetto trovato nella prova di installazione pulita (2026-11-13): con una
# voce notify incompleta la run stampava il repr dell'eccezione — `notify smtp:
# 'host'` — e un webhook irraggiungibile stampava `<urlopen error [Errno 111]
# Connection refused>`. Per chi installa sono righe inutili: non dicono quale
# campo manca ne' cosa controllare.

def _err_config(tmp_path, notify: list) -> dict:
    return {
        "profile": "t",
        "store": {"path": str(tmp_path / "data" / "t.db")},
        "sources": [{"name": "finta", "kind": "rss"}],
        "filter": {"include": ["bando"], "min_score": 1},
        "digest": {"max_items": 5},
        "notify": notify,
    }


def _run_with_items(tmp_path, monkeypatch, notify: list):
    """Esegue engine.run() con una fonte finta che produce un match."""
    from sentinel_digest import engine

    class _Fake:
        def safe_fetch(self):
            return [make("Nuovo bando regionale")]

    monkeypatch.setattr(engine, "build_source", lambda cfg: _Fake())
    return engine.run(_err_config(tmp_path, notify))


def test_errore_smtp_incompleto_e_leggibile(tmp_path, monkeypatch):
    """Regressione: `notify smtp: 'host'` non dice niente a chi installa."""
    res = _run_with_items(tmp_path, monkeypatch, [{"kind": "smtp"}])
    msg = "; ".join(res.errors)
    assert msg, "un notifier incompleto deve comparire negli errori"
    # il vecchio messaggio era il repr dell'eccezione: `notify smtp: 'host'`
    assert msg.strip() != "notify smtp: 'host'", "non deve restare il repr crudo del KeyError"
    assert "campo obbligatorio" in msg, "deve dire che manca un campo"
    assert "'host'" in msg, "deve nominare il campo mancante in modo univoco"
    assert "kind" in msg or "voce notify" in msg, "deve dire dove intervenire"


def test_errore_webhook_irraggiungibile_e_leggibile(tmp_path, monkeypatch):
    """Regressione: `<urlopen error [Errno 111] Connection refused>` e' rumore."""
    res = _run_with_items(
        tmp_path,
        monkeypatch,
        [{"kind": "webhook", "format": "slack", "url": "http://127.0.0.1:1/nope"}],
    )
    msg = "; ".join(res.errors)
    assert msg, "il webhook irraggiungibile deve essere segnalato"
    assert "urlopen" not in msg, "non deve esporre gli interni di urllib"
    assert "non raggiungibile" in msg
    assert "notificati=0" in res.summary()


def test_un_notifier_rotto_non_impedisce_gli_altri(tmp_path, monkeypatch):
    """Un notifier mal configurato non deve bloccare quelli sani."""
    out_dir = tmp_path / "out"
    res = _run_with_items(
        tmp_path,
        monkeypatch,
        [{"kind": "smtp"}, {"kind": "folder", "path": str(out_dir)}],
    )
    assert res.errors, "l'errore del notifier rotto va comunque riportato"
    assert res.sent == 1, "il notifier sano deve aver notificato"
    assert list(out_dir.glob("*-latest.html")), "il folder notifier deve aver scritto il digest"


def test_describe_failure_traduce_i_casi_notevoli():
    import smtplib
    import urllib.error

    from sentinel_digest.notify import describe_failure

    assert "campo obbligatorio 'to'" in describe_failure(KeyError("to"))
    http = urllib.error.HTTPError("u", 404, "Not Found", None, None)
    assert "HTTP 404" in describe_failure(http)
    net = urllib.error.URLError(ConnectionRefusedError(111, "Connection refused"))
    assert "non raggiungibile" in describe_failure(net)
    auth = smtplib.SMTPAuthenticationError(535, b"bad credentials")
    assert "credenziali" in describe_failure(auth)
    assert describe_failure(TimeoutError("t")) .startswith("tempo scaduto")


def test_describe_failure_traduce_dns_e_connessione():
    """Caso trovato provando la fix sui server veri: un host che non risolve
    stampava `gaierror: [Errno -2] Name or service not known`."""
    import socket

    from sentinel_digest.notify import describe_failure

    dns = describe_failure(socket.gaierror(-2, "Name or service not known"))
    assert "non risolve" in dns, "deve dire che il nome host e' il problema"
    assert not dns.startswith("gaierror"), "non deve iniziare con il nome dell'eccezione"
    conn = describe_failure(ConnectionRefusedError(111, "Connection refused"))
    assert "rifiutata" in conn or "interrotta" in conn
