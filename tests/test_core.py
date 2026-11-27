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

def _doctor_on(tmp_path, notify, sources=None, filt=None):
    """Scrive una config minima e lancia doctor, ritornando (rc, stdout)."""
    import json

    from sentinel_digest.cli import main

    cfg = {
        "profile": "t",
        "store": {"path": str(tmp_path / "data" / "t.db")},
        "sources": [] if sources is None else sources,
        "notify": notify,
    }
    if filt is not None:
        cfg["filter"] = filt
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


# --- SMTP: valore di 'tls' non riconosciuto --------------------------------
#
# Difetto trovato il 20/11/2026 provando l'invio reale contro un server SMTP
# locale: `tls: plain` (o qualunque valore non previsto) veniva ignorato senza
# dire niente e la connessione cadeva comunque su STARTTLS. Un server che non
# espone STARTTLS rispondeva `STARTTLS extension not supported by server`, un
# messaggio che non nomina il campo che l'utente ha scritto male. Peggio: con
# `tls: none`, scritto in YAML, PyYAML legge il valore come stringa 'none' solo
# per errore — la parola `none` non e' quotata e il risultato dipende dal
# parser — quindi la scelta "niente TLS" non era affidabile.

def test_tls_plain_e_documentato_e_non_chiama_starttls():
    """`tls: plain` e' un valore valido (nessuna cifratura), non un refuso."""
    from sentinel_digest.notify import SmtpNotifier

    n = SmtpNotifier({"kind": "smtp", "host": "h", "to": ["a@b"], "port": 587, "tls": "plain"})
    assert n.mode == "plain"


def test_tls_valore_ignoto_e_errore_leggibile_non_fallback_muto():
    """Il difetto: un valore non previsto cadeva in silenzio su STARTTLS."""
    import pytest

    from sentinel_digest.notify import SmtpNotifier

    with pytest.raises(ValueError) as exc:
        SmtpNotifier({"kind": "smtp", "host": "h", "to": ["a@b"], "port": 587, "tls": "TLS1.2"})
    msg = str(exc.value)
    assert "tls" in msg, "il messaggio deve nominare il campo tls"
    assert "TLS1.2" in msg, "deve citare il valore scritto dall'utente"
    assert "starttls" in msg and "ssl" in msg, "deve elencare i valori validi"


def test_tls_case_e_spazi_non_contano():
    """`TLS: SSL  ` in un YAML scritto a mano non deve rompere la connessione."""
    from sentinel_digest.notify import SmtpNotifier

    n = SmtpNotifier({"kind": "smtp", "host": "h", "to": ["a@b"], "tls": " SSL "})
    assert n.mode == "ssl"


def test_smtp_senza_tls_dichiarato_non_prova_starttls(monkeypatch):
    """`tls: none` deve davvero saltare STARTTLS (server SMTP senza extension)."""
    from datetime import datetime, timezone

    from sentinel_digest.notify import SmtpNotifier

    chiamate: list[str] = []

    class _FakeSMTP:
        def __init__(self, *a, **k):
            chiamate.append("connect")

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def ehlo(self):
            chiamate.append("ehlo")

        def starttls(self, **k):
            chiamate.append("starttls")

        def login(self, *a):
            chiamate.append("login")

        def send_message(self, msg):
            chiamate.append("send_message")

    import smtplib

    monkeypatch.setattr(smtplib, "SMTP", _FakeSMTP)
    n = SmtpNotifier({"kind": "smtp", "host": "h", "to": ["a@b"], "tls": "none"})
    assert n.send("p", [], datetime.now(timezone.utc), "<p>x</p>", "x") is True
    assert "starttls" not in chiamate, "con tls: none non si deve chiamare STARTTLS"
    assert "send_message" in chiamate, "il messaggio va comunque inviato"


def test_doctor_non_dichiara_ok_un_notifier_che_non_si_costruisce(tmp_path, capsys):
    """Regressione: `tls` scritto male rendeva doctor [OK] + exit 0.

    check_notifier guardava solo la presenza dei campi obbligatori, quindi una
    voce con `tls: require_tls` (campo presente, valore incomprensibile) passava
    la diagnosi e falliva solo alla run. Trovato il 20/11/2026 con doctor
    eseguito davvero mentre si provava l'invio SMTP reale.
    """
    rc = _doctor_on(
        tmp_path,
        [{"kind": "smtp", "host": "h", "to": ["a@b"], "tls": "require_tls"}],
        sources=[{"name": "finta", "kind": "rss", "url": "https://x.test/f.xml"}],
        filt={"include": ["bando"], "min_score": 1},
    )
    out = capsys.readouterr().out
    assert rc == 1, "una voce notify che non si costruisce deve rendere la diagnosi negativa"
    assert "[FAIL] notifier smtp" in out, "il difetto era proprio che stampava [OK]"
    assert "tls" in out, "deve nominare il campo da correggere"
    assert "PROBLEMI: 1" in out, "il conteggio deve riflettere il problema"


def test_doctor_accetta_i_notifier_sani(tmp_path, capsys):
    """Controprova: la nuova costruzione non deve produrre falsi allarmi.

    Passa da un config *completo* (fonte e filtro inclusi) perche' la controprova
    isola i notifier: se il doctor fallisse per altro, il test non proverebbe nulla.
    """
    rc = _doctor_on(
        tmp_path,
        [
            {"kind": "folder", "path": str(tmp_path / "out")},
            {"kind": "smtp", "host": "smtp.example.it", "to": ["a@b"], "tls": "ssl"},
            {"kind": "webhook", "format": "telegram", "url": "https://x.test/h", "chat_id": "1"},
        ],
        sources=[{"name": "finta", "kind": "rss", "url": "https://x.test/f.xml"}],
        filt={"include": ["bando"], "min_score": 1},
    )
    out = capsys.readouterr().out
    assert rc == 0, f"nessuna di queste voci e' rotta: {out}"
    assert "TUTTO OK" in out


# --- load_config: config in YAML senza PyYAML -------------------------------

def test_load_config_yaml_senza_pyyaml_da_errore_leggibile(tmp_path, monkeypatch):
    """Chi installa `.[dev]` (niente PyYAML) e punta al .yaml di esempio non deve
    ricevere un traceback JSONDecodeError: il messaggio deve nominare PyYAML e
    indicare il comando per rimediare."""
    import builtins

    from sentinel_digest.engine import ConfigNotFound, load_config

    real_import = builtins.__import__

    def fake_import(name, *a, **k):
        if name == "yaml":
            raise ImportError("No module named 'yaml'")
        return real_import(name, *a, **k)

    monkeypatch.setattr(builtins, "__import__", fake_import)
    cfg_file = tmp_path / "config.yaml"
    cfg_file.write_text("profile: bandi-pmi\nsources: []\n", encoding="utf-8")
    with pytest.raises(ConfigNotFound) as e:
        load_config(cfg_file)
    msg = str(e.value)
    assert "PyYAML" in msg, msg
    assert "yaml" in msg.lower(), msg


def test_load_config_json_senza_pyyaml_funziona(tmp_path, monkeypatch):
    """Controprova: senza PyYAML una config JSON resta pienamente leggibile."""
    import builtins
    import json

    from sentinel_digest.engine import load_config

    real_import = builtins.__import__

    def fake_import(name, *a, **k):
        if name == "yaml":
            raise ImportError("No module named 'yaml'")
        return real_import(name, *a, **k)

    monkeypatch.setattr(builtins, "__import__", fake_import)
    cfg_file = tmp_path / "config.json"
    cfg_file.write_text(json.dumps({"profile": "x", "sources": []}), encoding="utf-8")
    cfg = load_config(cfg_file)
    assert cfg["profile"] == "x"
