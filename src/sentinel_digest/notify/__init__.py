"""Invio del digest: stdout, file, SMTP, webhook (Telegram/Slack/Discord)."""

from __future__ import annotations

import json
import logging
import smtplib
import ssl
import urllib.request
from email.message import EmailMessage

from ..render import render_html, render_text

log = logging.getLogger(__name__)


class Notifier:
    def send(self, profile: str, matches, generated, html: str, text: str) -> bool:
        raise NotImplementedError


class FolderNotifier(Notifier):
    """Scrive il digest su disco: base per debug e per servirlo via web."""

    kind = "folder"

    def __init__(self, cfg: dict):
        from pathlib import Path

        self.dir = Path(cfg.get("path", "out"))
        self.dir.mkdir(parents=True, exist_ok=True)

    def send(self, profile, matches, generated, html, text) -> bool:
        stamp = generated.strftime("%Y%m%d-%H%M")
        (self.dir / f"{profile}-{stamp}.html").write_text(html, encoding="utf-8")
        (self.dir / f"{profile}-{stamp}.txt").write_text(text, encoding="utf-8")
        (self.dir / f"{profile}-latest.html").write_text(html, encoding="utf-8")
        log.info("digest scritto in %s", self.dir)
        return True


class StdoutNotifier(Notifier):
    kind = "stdout"

    def send(self, profile, matches, generated, html, text) -> bool:
        print(text)
        return True


class SmtpNotifier(Notifier):
    """SMTP con TLS implicito (465) o STARTTLS (587)."""

    kind = "smtp"

    def __init__(self, cfg: dict):
        self.host = cfg["host"]
        self.port = int(cfg.get("port", 465))
        self.user = cfg.get("user") or cfg.get("username")
        self.password = cfg.get("password") or ""
        self.sender = cfg.get("from") or self.user
        self.to = cfg["to"] if isinstance(cfg["to"], list) else [cfg["to"]]
        self.mode = (cfg.get("tls") or ("ssl" if self.port == 465 else "starttls")).lower()
        self.timeout = int(cfg.get("timeout", 30))

    def send(self, profile, matches, generated, html, text) -> bool:
        msg = EmailMessage()
        msg["Subject"] = f"[{profile}] {len(matches)} segnalazioni - {generated.strftime('%d/%m/%Y')}"
        msg["From"] = self.sender
        msg["To"] = ", ".join(self.to)
        msg.set_content(text)
        msg.add_alternative(html, subtype="html")

        ctx = ssl.create_default_context()
        if self.mode in ("ssl", "tls", "implicit"):
            with smtplib.SMTP_SSL(self.host, self.port, timeout=self.timeout, context=ctx) as s:
                if self.user:
                    s.login(self.user, self.password)
                s.send_message(msg)
        else:
            with smtplib.SMTP(self.host, self.port, timeout=self.timeout) as s:
                s.ehlo()
                s.starttls(context=ctx)
                s.ehlo()
                if self.user:
                    s.login(self.user, self.password)
                s.send_message(msg)
        log.info("digest inviato via SMTP a %s", ", ".join(self.to))
        return True


class WebhookNotifier(Notifier):
    """Telegram (sendMessage), Slack, Discord o webhook generico."""

    kind = "webhook"

    def __init__(self, cfg: dict):
        self.url = cfg["url"]
        self.format = (cfg.get("format") or "telegram").lower()
        self.chat_id = cfg.get("chat_id")
        self.max_len = int(cfg.get("max_len", 3900))
        self.user_agent = cfg.get("user_agent", "SentinelDigest/0.1")

    def _chunks(self, text: str) -> list[str]:
        if len(text) <= self.max_len:
            return [text]
        out, cur = [], ""
        for line in text.splitlines(True):
            if len(cur) + len(line) > self.max_len:
                out.append(cur)
                cur = ""
            cur += line
        if cur:
            out.append(cur)
        return out

    def send(self, profile, matches, generated, html, text) -> bool:
        headers = {"Content-Type": "application/json", "User-Agent": self.user_agent}
        for chunk in self._chunks(text):
            if self.format == "slack":
                payload = {"text": chunk}
            elif self.format == "discord":
                payload = {"content": chunk}
            elif self.format == "telegram":
                if not self.chat_id:
                    raise ValueError("webhook telegram: manca chat_id")
                payload = {
                    "chat_id": self.chat_id,
                    "text": chunk,
                    "disable_web_page_preview": True,
                }
            else:
                payload = {"profile": profile, "text": chunk, "items": len(matches)}
            req = urllib.request.Request(
                self.url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST"
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                if resp.status >= 300:
                    raise RuntimeError(f"webhook HTTP {resp.status}")
        log.info("digest inviato via webhook (%s)", self.format)
        return True


NOTIFIERS = {
    "folder": FolderNotifier,
    "stdout": StdoutNotifier,
    "smtp": SmtpNotifier,
    "webhook": WebhookNotifier,
}


# Campi obbligatori per ciascun notifier: servono anche al doctor, per
# accorgersi di una config incompleta prima della run.
REQUIRED_FIELDS = {"smtp": ("host", "to"), "webhook": ("url",)}


def valid_kinds() -> str:
    """Elenco dei kind validi in forma leggibile, per i messaggi all'utente.

    Non usare `sorted(NOTIFIERS)` nei messaggi: stampa la repr della lista
    (['folder', 'smtp', ...]), che per un utente finale e' rumore.
    """
    return ", ".join(sorted(NOTIFIERS))


def check_notifier(cfg: dict) -> str | None:
    """Verifica una voce `notify` senza costruirla. Ritorna None se ok,
    altrimenti il motivo, in italiano e gia' pronto da stampare."""
    kind = cfg.get("kind", "stdout")
    if kind not in NOTIFIERS:
        suggerimento = ""
        vicini = [k for k in NOTIFIERS if k.startswith(str(kind)[:3])]
        if vicini:
            suggerimento = f" - intendevi {vicini[0]!r}?"
        return (
            f"kind sconosciuto {kind!r}{suggerimento} "
            f"(kind validi: {valid_kinds()})"
        )
    mancanti = [k for k in REQUIRED_FIELDS.get(kind, ()) if not cfg.get(k)]
    if mancanti:
        return f"mancano i campi obbligatori: {', '.join(mancanti)}"
    return None


def build_notifier(cfg: dict) -> Notifier:
    kind = cfg.get("kind", "stdout")
    cls = NOTIFIERS.get(kind)
    if cls is None:
        raise ValueError(f"notifier non valido: {check_notifier(cfg)}")
    return cls(cfg)  # type: ignore[arg-type]


__all__ = [
    "Notifier", "FolderNotifier", "StdoutNotifier", "SmtpNotifier", "WebhookNotifier",
    "build_notifier", "check_notifier", "valid_kinds",
    "render_html", "render_text", "NOTIFIERS", "REQUIRED_FIELDS",
]
