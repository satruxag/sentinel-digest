"""Rendering del digest in HTML e testo, senza dipendenze."""

from __future__ import annotations

import html
from datetime import datetime

from .filtering import Match


def _fmt_date(item) -> str:
    if not item.published:
        return "data n.d."
    return item.published.strftime("%d/%m/%Y")


def render_text(matches: list[Match], profile: str, generated: datetime, base_url: str = "") -> str:
    lines = [
        f"DIGEST {profile.upper()} - {generated.strftime('%d/%m/%Y %H:%M')}",
        f"{len(matches)} segnalazioni",
        "=" * 62,
        "",
    ]
    for i, m in enumerate(matches, 1):
        it = m.item
        lines.append(f"{i}. {it.title}")
        meta = [it.source, _fmt_date(it)]
        if it.region:
            meta.append(it.region)
        lines.append("   " + " | ".join(meta))
        if it.summary:
            lines.append("   " + it.summary[:300])
        lines.append(f"   {it.url}")
        if m.hits:
            lines.append(f"   match: {', '.join(m.hits[:8])}")
        lines.append("")
    if base_url:
        lines.append(f"-- Sentinel Digest | {base_url}")
    return "\n".join(lines)


def render_html(matches: list[Match], profile: str, generated: datetime, base_url: str = "") -> str:
    rows = []
    for m in matches:
        it = m.item
        meta = " · ".join(
            x for x in [html.escape(it.source), _fmt_date(it), html.escape(it.region or "")] if x
        )
        summary = (
            f'<p style="margin:6px 0 0;color:#444;font-size:14px;line-height:1.45">'
            f"{html.escape(it.summary[:400])}</p>"
            if it.summary
            else ""
        )
        hits = (
            '<p style="margin:6px 0 0;font-size:12px;color:#7a6a00">'
            + " ".join(
                f'<span style="background:#fff6cc;padding:1px 6px;border-radius:3px">{html.escape(h)}</span>'
                for h in m.hits[:8]
            )
            + "</p>"
            if m.hits
            else ""
        )
        rows.append(
            f"""
        <tr><td style="padding:14px 16px;border-bottom:1px solid #e6e6e6">
          <a href="{html.escape(it.url)}" style="color:#0b5ed7;font-weight:600;font-size:16px;
             text-decoration:none;line-height:1.3">{html.escape(it.title)}</a>
          <div style="margin-top:4px;font-size:12px;color:#777">{meta}</div>
          {summary}{hits}
        </td></tr>"""
        )

    body = "".join(rows) or (
        '<tr><td style="padding:24px;color:#777">Nessuna nuova segnalazione in questo periodo.</td></tr>'
    )
    footer = (
        f'<p style="margin:16px 0 0;font-size:12px;color:#999">Sentinel Digest &middot; '
        f'{html.escape(base_url or "self-hosted")}</p>'
        if True
        else ""
    )
    return f"""<!doctype html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Digest {html.escape(profile)}</title></head>
<body style="margin:0;background:#f4f5f7;font-family:-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif">
<table width="100%" cellpadding="0" cellspacing="0"><tr><td align="center" style="padding:24px 12px">
<table width="640" cellpadding="0" cellspacing="0"
       style="background:#fff;border-radius:8px;overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,.08)">
  <tr><td style="background:#0f172a;color:#fff;padding:18px 16px">
    <div style="font-size:19px;font-weight:700">Digest {html.escape(profile.title())}</div>
    <div style="font-size:13px;color:#c3cbd8;margin-top:3px">
      {generated.strftime('%d/%m/%Y %H:%M')} &middot; {len(matches)} segnalazioni</div>
  </td></tr>
  {body}
  <tr><td style="padding:14px 16px;background:#fafbfc">{footer}</td></tr>
</table></td></tr></table></body></html>"""