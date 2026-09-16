"""Stato persistente: evita di rinotificare lo stesso item."""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path

from ..models import Item


class Store:
    """SQLite: zero dipendenze, un file, backup banale."""

    def __init__(self, path: str | Path = "data/sentinel.db"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.path), timeout=30)
        self.conn.execute("PRAGMA journal_mode=WAL")
        self._migrate()

    def _migrate(self) -> None:
        self.conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS seen (
                uid        TEXT PRIMARY KEY,
                source     TEXT NOT NULL,
                title      TEXT NOT NULL,
                url        TEXT NOT NULL,
                first_seen TEXT NOT NULL,
                sent_at    TEXT,
                score      REAL DEFAULT 0
            );
            CREATE INDEX IF NOT EXISTS idx_seen_sent ON seen(sent_at);
            CREATE TABLE IF NOT EXISTS runs (
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                started  TEXT NOT NULL,
                finished TEXT,
                fetched  INTEGER DEFAULT 0,
                matched  INTEGER DEFAULT 0,
                sent     INTEGER DEFAULT 0,
                errors   TEXT
            );
            """
        )
        self.conn.commit()

    # --- run bookkeeping -------------------------------------------------
    def start_run(self) -> int:
        cur = self.conn.execute(
            "INSERT INTO runs (started, errors) VALUES (?, '')",
            (datetime.now(timezone.utc).isoformat(),),
        )
        self.conn.commit()
        assert cur.lastrowid is not None
        return int(cur.lastrowid)

    def finish_run(self, run_id: int, fetched: int, matched: int, sent: int, errors: str = "") -> None:
        self.conn.execute(
            "UPDATE runs SET finished=?, fetched=?, matched=?, sent=?, errors=? WHERE id=?",
            (datetime.now(timezone.utc).isoformat(), fetched, matched, sent, errors[:4000], run_id),
        )
        self.conn.commit()

    # --- dedup -----------------------------------------------------------
    def is_seen(self, uid: str) -> bool:
        cur = self.conn.execute("SELECT 1 FROM seen WHERE uid=?", (uid,))
        return cur.fetchone() is not None

    def is_new(self, item: Item) -> bool:
        return not self.is_seen(item.uid)

    def mark(self, item: Item, score: float = 0.0, sent: bool = False, first_seen: str | None = None) -> None:
        """Registra un item. `first_seen` esplicito serve ai test e alle importazioni storiche."""
        now = datetime.now(timezone.utc).isoformat()
        self.conn.execute(
            """INSERT INTO seen (uid, source, title, url, first_seen, sent_at, score)
               VALUES (?,?,?,?,?,?,?)
               ON CONFLICT(uid) DO UPDATE SET score=excluded.score,
                 sent_at=COALESCE(seen.sent_at, excluded.sent_at)""",
            (item.uid, item.source, item.title, item.url, first_seen or now,
             now if sent else None, score),
        )
        self.conn.commit()

    def pending(self, max_age_days: int = 7) -> list[dict]:
        """Item mai notificati (utile per digest successivi o recupero)."""
        cutoff = (datetime.now(timezone.utc) - timedelta(days=max_age_days)).isoformat()
        cur = self.conn.execute(
            "SELECT uid, source, title, url, first_seen, score FROM seen "
            "WHERE sent_at IS NULL AND first_seen >= ? ORDER BY score DESC, first_seen DESC",
            (cutoff,),
        )
        cols = [c[0] for c in cur.description]
        return [dict(zip(cols, row)) for row in cur.fetchall()]

    def stats(self) -> dict:
        total = self.conn.execute("SELECT COUNT(*) FROM seen").fetchone()[0]
        sent = self.conn.execute("SELECT COUNT(*) FROM seen WHERE sent_at IS NOT NULL").fetchone()[0]
        last = self.conn.execute(
            "SELECT started, finished, fetched, matched, sent FROM runs ORDER BY id DESC LIMIT 1"
        ).fetchone()
        return {
            "seen_total": total,
            "seen_notified": sent,
            "last_run": (
                {"started": last[0], "finished": last[1], "fetched": last[2],
                 "matched": last[3], "sent": last[4]}
                if last
                else None
            ),
        }

    def prune(self, keep_days: int = 180) -> int:
        cutoff = (datetime.now(timezone.utc) - timedelta(days=keep_days)).isoformat()
        cur = self.conn.execute("DELETE FROM seen WHERE first_seen < ?", (cutoff,))
        self.conn.commit()
        return cur.rowcount

    def export_json(self, path: str | Path) -> int:
        rows = self.conn.execute("SELECT * FROM seen").fetchall()
        cols = [c[0] for c in self.conn.execute("SELECT * FROM seen LIMIT 1").description]
        data = [dict(zip(cols, r)) for r in rows]
        Path(path).write_text(json.dumps(data, indent=2), encoding="utf-8")
        return len(data)

    def close(self) -> None:
        self.conn.close()
