"""Fonte RSS/Atom generica: copre la maggior parte delle PA e dei portali gare."""

from __future__ import annotations

import xml.etree.ElementTree as ET

from ..models import Item, parse_date
from .base import Source, register

ATOM = "{http://www.w3.org/2005/Atom}"
CONTENT = "{http://purl.org/rss/1.0/modules/content/}"


def _text(node, *paths: str) -> str:
    for path in paths:
        found = node.find(path)
        if found is not None and (found.text or "").strip():
            return (found.text or "").strip()
    return ""


@register
class RssSource(Source):
    kind = "rss"

    def fetch(self) -> list[Item]:
        import urllib.request

        url = self.options["url"]
        timeout = int(self.options.get("timeout", 20))
        limit = int(self.options.get("limit", 50))
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": self.options.get(
                    "user_agent",
                    "SentinelDigest/0.1 (+https://github.com/; self-hosted feed reader)",
                ),
                "Accept": "application/rss+xml, application/atom+xml, application/xml, text/xml, */*",
            },
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            payload = resp.read()

        try:
            root = ET.fromstring(payload)
        except ET.ParseError:
            # feed con BOM/enconding dichiarato male: riprova senza dichiarazione
            cleaned = payload.decode("utf-8", "replace").lstrip("\ufeff")
            root = ET.fromstring(cleaned)

        entries = root.findall(".//item") or root.findall(f".//{ATOM}entry")
        items: list[Item] = []
        for e in entries[:limit]:
            title = _text(e, "title", f"{ATOM}title")
            link = _text(e, "link", f"{ATOM}link")
            if not link:
                ln = e.find(f"{ATOM}link")
                if ln is not None:
                    link = ln.get("href", "")
            published = parse_date(
                _text(e, "pubDate", f"{ATOM}updated", f"{ATOM}published", "dc:date")
            )
            summary = _text(
                e, "description", "summary", f"{ATOM}summary", f"{ATOM}content", f"{CONTENT}encoded"
            )
            if not title or not link:
                continue
            items.append(
                Item(
                    source=self.name,
                    title=_strip_html(title, clean=False)[:300],
                    url=link,
                    published=published,
                    summary=_strip_html(summary)[:600],
                    region=self.options.get("region", ""),
                    tags=list(self.options.get("tags") or []),
                )
            )
        return items


def _strip_html(text: str, clean: bool = True) -> str:
    """Toglie i tag. Con clean=True applica anche la pulizia dei boilerplate."""
    import html
    import re

    text = re.sub(r"(?is)<(script|style).*?</\1>", " ", text)
    text = re.sub(r"(?s)<[^>]+>", " ", text)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return _clean_summary(text) if clean else text


def _clean_summary(text: str) -> str:
    """Rimuove dal sommario gli artefatti tipici dei feed delle PA.

    Molti CMS istituzionali concatenano autore, email e data prima del testo
    vero: qui si tagliano email, URL nudi e boilerplate iniziale.
    """
    import re

    text = re.sub(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)*[^\s]*", " ", text)
    text = re.sub(r"https?://\S+", " ", text)
    text = re.sub(r"\b(?:lun|mar|mer|gio|ven|sab|dom)[a-zà-ù]*[\s,]+\d{1,2}[/ ]\w{3,9}[/ ]?\d{0,4}\s*[-–]?\s*\d{0,2}:?\d{0,2}", " ", text, flags=re.I)
    text = re.sub(r"^\s*(?:false|true|null)\s+", " ", text, flags=re.I)
    text = re.sub(r"\s+", " ", text).strip(" -|·,")
    # Molti feed PA concatenano metadati (autore, data, categoria) prima del testo
    # vero. Se riconosciamo il pattern, teniamo solo la parte dopo l'ultimo marcatore.
    markers = ["IGF Italia", "Leggi tutto", "Continua a leggere", "Scopri di pi"]
    for mk in markers:
        idx = text.find(mk)
        if idx > 0:
            tail = text[idx:]
            if len(tail) > 120:
                text = tail
                break
    if len(text) < 40:
        return ""
    return text
