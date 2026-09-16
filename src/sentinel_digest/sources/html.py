"""Fonte HTML: estrae link+testo da una pagina indice (liste di bandi/avvisi).

Serve per le PA che non espongono RSS. Regole dichiarative nel config:
- item_selector: selettore CSS del contenitore di ogni voce
- title_selector / link_selector / date_selector: opzionali
"""

from __future__ import annotations

import re

from ..models import Item, parse_date
from .base import Source, register
from .rss import _strip_html


@register
class HtmlListSource(Source):
    kind = "html"

    def fetch(self) -> list[Item]:
        import urllib.request

        url = self.options["url"]
        base = self.options.get("base_url", url)
        timeout = int(self.options.get("timeout", 25))
        limit = int(self.options.get("limit", 50))
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": self.options.get(
                    "user_agent", "SentinelDigest/0.1 (+self-hosted feed reader)"
                )
            },
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            html = resp.read().decode(resp.headers.get_content_charset() or "utf-8", "replace")

        pattern = self.options.get("item_pattern")
        if pattern:
            # modalità regex: cattura href + testo per ogni match
            items = self._from_regex(html, pattern, base, limit)
        else:
            items = self._from_css(html, base, limit)
        return items

    def _from_regex(self, html: str, pattern: str, base: str, limit: int) -> list[Item]:
        from urllib.parse import urljoin

        items: list[Item] = []
        for match in re.finditer(pattern, html, re.I | re.S):
            href = match.group("url") if "url" in (match.groupdict() or {}) else match.group(1)
            label = match.group("title") if "title" in (match.groupdict() or {}) else (
                match.group(2) if match.lastindex and match.lastindex >= 2 else ""
            )
            if not href:
                continue
            title = _strip_html(label) or _strip_html(href)
            items.append(
                Item(
                    source=self.name,
                    title=title[:300],
                    url=urljoin(base, href),
                    region=self.options.get("region", ""),
                    tags=list(self.options.get("tags") or []),
                )
            )
            if len(items) >= limit:
                break
        return items

    def _from_css(self, html: str, base: str, limit: int) -> list[Item]:
        from html.parser import HTMLParser
        from urllib.parse import urljoin

        # parser minimale senza dipendenze: raccoglie <a href> con testo
        class LinkCollector(HTMLParser):
            def __init__(self) -> None:
                super().__init__()
                self.links: list[tuple[str, str]] = []
                self._href: str | None = None
                self._buf: list[str] = []

            def handle_starttag(self, tag, attrs):
                if tag == "a":
                    d = dict(attrs)
                    self._href = d.get("href")
                    self._buf = []

            def handle_data(self, data):
                if self._href is not None:
                    self._buf.append(data)

            def handle_endtag(self, tag):
                if tag == "a" and self._href is not None:
                    text = _strip_html(" ".join(self._buf))
                    if text and len(text) > 12:
                        self.links.append((self._href, text))
                    self._href = None

        parser = LinkCollector()
        parser.feed(html)
        items: list[Item] = []
        for href, text in parser.links:
            if href.startswith(("mailto:", "javascript:", "#")):
                continue
            items.append(
                Item(
                    source=self.name,
                    title=text[:300],
                    url=urljoin(base, href),
                    region=self.options.get("region", ""),
                    tags=list(self.options.get("tags") or []),
                )
            )
            if len(items) >= limit:
                break
        return items