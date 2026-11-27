"""Copertura per sources/html.py e render.py: nessuna rete, nessuna dipendenza."""

from __future__ import annotations

from datetime import datetime, timezone

T0 = datetime(2026, 10, 23, 6, 0, tzinfo=timezone.utc)

from sentinel_digest.filtering import Match
from sentinel_digest.models import Item
from sentinel_digest.render import render_html, render_text
from sentinel_digest.sources.html import HtmlListSource

HTML_INDEX = """
<html><body>
  <ul class="bandi">
    <li><a href="/bando/123">Bando contributi digitalizzazione PMI 2026</a></li>
    <li><a href="https://altra.pa.it/avviso/9">Avviso pubblico per la formazione dei dipendenti</a></li>
    <li><a href="mailto:ufficio@comune.it">Scrivi all'ufficio bandi del comune</a></li>
    <li><a href="#top">Torna su nella pagina indice dei bandi</a></li>
  </ul>
</body></html>
"""


# --- sources/html.py: modalita' regex ---------------------------------------

def test_html_regex_estrae_url_relativi_e_assoluti():
    src = HtmlListSource(
        "Comune - Bandi",
        {
            "url": "https://www.comune.example.it/bandi",
            "base_url": "https://www.comune.example.it",
            "item_pattern": r'<a[^>]+href="(?P<url>[^"]+)"[^>]*>(?P<title>[^<]{15,200})</a>',
        },
    )
    items = src._from_regex(
        HTML_INDEX,
        r'<a[^>]+href="(?P<url>[^"]+)"[^>]*>(?P<title>[^<]{15,200})</a>',
        "https://www.comune.example.it",
        50,
    )
    urls = [i.url for i in items]
    assert "https://www.comune.example.it/bando/123" in urls, "href relativo va risolto sul base_url"
    assert "https://altra.pa.it/avviso/9" in urls, "href assoluto va lasciato intatto"
    assert items[0].title == "Bando contributi digitalizzazione PMI 2026"
    assert all(i.source == "Comune - Bandi" for i in items)


def test_html_regex_rispetta_limit():
    src = HtmlListSource("X", {"url": "https://x.test/"})
    items = src._from_regex(
        HTML_INDEX, r'<a[^>]+href="(?P<url>[^"]+)"[^>]*>(?P<title>[^<]{15,200})</a>', "https://x.test/", 2
    )
    assert len(items) == 2


# --- sources/html.py: modalita' CSS/link-scan -------------------------------

def test_html_css_salta_mailto_anchor_e_link_corti():
    src = HtmlListSource(
        "Comune", {"url": "https://www.comune.example.it/bandi", "base_url": "https://www.comune.example.it"}
    )
    items = src._from_css(HTML_INDEX, "https://www.comune.example.it", 50)
    urls = [i.url for i in items]
    assert "https://www.comune.example.it/bando/123" in urls
    assert not any(u.startswith("mailto:") for u in urls), "mailto non e' un bando"
    assert not any(u.endswith("#top") for u in urls), "ancora interna non e' un bando"
    # il testo dell'ancora '#top' e' < 12 caratteri di contenuto utile -> escluso
    assert all(len(i.title) > 12 for i in items)


def test_html_css_rispetta_limit():
    src = HtmlListSource("Comune", {"url": "https://x.test/"})
    items = src._from_css(HTML_INDEX, "https://x.test/", 1)
    assert len(items) == 1


# --- render.py --------------------------------------------------------------

def _match(title="Bando per l'innovazione <PMI>", summary="", hits=None, published=True):
    it = Item(
        source="Comune & Co",
        title=title,
        url="https://example.test/bando?a=1&b=2",
        summary=summary,
        region="Lazio",
        published=datetime(2026, 10, 23, tzinfo=timezone.utc) if published else None,
    )
    return Match(item=it, score=2.0, hits=hits or ["bando"])


def test_render_text_intestazione_e_conteggio():
    out = render_text([_match(), _match("Avviso PNRR")], "bandi-pmi", T0)
    assert "DIGEST BANDI-PMI" in out
    assert "2 segnalazioni" in out
    assert "match: bando" in out


def test_render_text_senza_fonti_non_aggiunge_footer():
    out = render_text([_match()], "p", T0)
    assert "Sentinel Digest |" not in out
    out2 = render_text([_match()], "p", T0, base_url="https://x.test")
    assert "Sentinel Digest | https://x.test" in out2


def test_render_text_lista_vuota_e_data_assente():
    out = render_text([_match(published=False)], "p", T0)
    assert "data n.d." in out
    empty = render_text([], "p", T0)
    assert "0 segnalazioni" in empty


def test_render_html_esegue_escape_di_titolo_e_url():
    out = render_html([_match()], "p", T0)
    assert "<PMI>" not in out, "il titolo deve essere escapato"
    assert "&lt;PMI&gt;" in out
    assert "?a=1&amp;b=2" in out, "l'URL deve essere escapato"


def test_render_html_html_struttura_e_stato_vuoto():
    out = render_html([_match()], "bandi-pmi", T0, base_url="https://x.test")
    assert out.startswith("<!doctype html>")
    assert "Digest Bandi-Pmi" in out
    assert "https://x.test" in out
    empty = render_html([], "p", T0)
    assert "Nessuna nuova segnalazione" in empty


# --- notify: spezzatura del digest per i canali con limite di lunghezza ------
# Telegram rifiuta i messaggi oltre ~4096 char con "message is too long": se il
# digest non viene spezzato la notifica fallisce in silenzio per l'utente.

from sentinel_digest.notify import WebhookNotifier


def _chunker(max_len):
    return WebhookNotifier(
        {"url": "http://127.0.0.1:1/hook", "format": "telegram", "chat_id": "1", "max_len": max_len}
    )


def test_chunks_riga_lunga_viene_spezzata_e_non_supera_il_limite():
    """Un URL di bando con parametri e' UNA riga piu' lunga del limite."""
    n = _chunker(100)
    url_lungo = "https://pa.example.it/bando?id=" + "A" * 400
    chunks = n._chunks(url_lungo)
    assert all(len(c) <= 100 for c in chunks), f"chunk oltre max_len: {[len(c) for c in chunks]}"
    assert all(chunks), "nessun chunk vuoto da inviare"
    assert "".join(chunks) == url_lungo, "la spezzatura non deve perdere caratteri"


def test_chunks_nessun_blocco_vuoto_in_testa_quando_la_prima_riga_sfonda():
    n = _chunker(100)
    chunks = n._chunks("X" * 250)
    assert chunks[0] != "", "il taglio ingenuo emetteva un primo chunk vuoto"


def test_chunks_spezzatura_reale_del_digest():
    """Caso misurato: digest reale con URL lungo, max_len=100."""
    long_url = "https://www.example-pa.it/bandi/avviso?id=" + "A" * 400
    it = Item(source="Comune", title="Bando " + "x" * 120, url=long_url)
    m = Match(item=it, score=1, hits=["bando"])
    txt = render_text([m], "p", T0)
    chunks = _chunker(100)._chunks(txt)
    assert all(len(c) <= 100 for c in chunks), "un chunk supera il limite -> Telegram rifiuta"
    assert all(chunks), "nessun chunk vuoto"
    assert "".join(chunks) == txt, "il digest riconcatenato deve essere identico"


def test_chunks_testo_corto_resta_una_sola_parte():
    n = _chunker(3900)
    assert n._chunks("riga breve") == ["riga breve"]
