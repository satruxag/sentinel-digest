"""CLI: sentinel-digest run|test|doctor|stats|export"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

from . import __version__
from .engine import load_config, run
from .sources import build_source
from .storage import Store


def _setup_log(verbose: bool) -> None:
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s %(levelname)-7s %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )


def cmd_run(args) -> int:
    config = load_config(args.config)
    if args.profile:
        config["profile"] = args.profile
    res = run(config, only_new=not args.all, dry_run=args.dry_run)
    print(res.summary())
    for e in res.errors:
        print(f"  ! {e}", file=sys.stderr)
    return 0


def cmd_test(args) -> int:
    """Prova le fonti senza scrivere stato né notificare."""
    config = load_config(args.config)
    fails = 0
    for scfg in config.get("sources") or []:
        name = scfg.get("name", scfg.get("kind"))
        try:
            src = build_source(scfg)
            items = src.safe_fetch()
        except Exception as exc:  # noqa: BLE001
            print(f"[FAIL] {name}: {exc}")
            fails += 1
            continue
        status = "OK  " if items else "VUOTO"
        print(f"[{status}] {name}: {len(items)} item")
        for it in items[:3]:
            when = it.published.strftime("%d/%m/%Y") if it.published else "n.d."
            print(f"         - {when} {it.title[:90]}")
            print(f"           {it.url[:110]}")
        if not items:
            fails += 1
    return 1 if fails else 0


def cmd_doctor(args) -> int:
    """Diagnostica: config, fonti, notifier, permessi di scrittura."""
    config = load_config(args.config)
    problems = 0
    print(f"Sentinel Digest {__version__}")
    print(f"profilo: {config.get('profile', 'default')}")

    conv = Path(config.get("store", {}).get("path", "data/x.db")).parent
    try:
        conv.mkdir(parents=True, exist_ok=True)
        probe = conv / ".write-test"
        probe.write_text("ok")
        probe.unlink()
        print(f"[OK  ] store scrivibile: {conv}")
    except Exception as exc:  # noqa: BLE001
        print(f"[FAIL] store non scrivibile: {exc}")
        problems += 1

    sources = config.get("sources") or []
    print(f"fonti configurate: {len(sources)}")
    if not sources:
        problems += 1
    for scfg in sources:
        name = scfg.get("name", scfg.get("kind"))
        try:
            build_source(scfg)
            print(f"[OK  ] fonte valida: {name} ({scfg.get('kind')})")
        except Exception as exc:  # noqa: BLE001
            print(f"[FAIL] fonte {name}: {exc}")
            problems += 1

    f = config.get("filter") or {}
    if not (f.get("include") or []):
        print("[WARN] nessuna keyword di include: verrebbe notificato tutto")
    print(f"include={len(f.get('include') or [])} exclude={len(f.get('exclude') or [])}")

    for ncfg in config.get("notify") or []:
        kind = ncfg.get("kind")
        missing = [k for k in {"smtp": ["host", "to"], "webhook": ["url"]}.get(kind, []) if not ncfg.get(k)]
        if missing:
            print(f"[FAIL] notifier {kind}: mancano {missing}")
            problems += 1
        else:
            print(f"[OK  ] notifier {kind}")

    print(f"{'PROBLEMI: ' + str(problems) if problems else 'TUTTO OK'}")
    return 1 if problems else 0


def cmd_stats(args) -> int:
    config = load_config(args.config)
    profile = config.get("profile", "default")
    store = Store(config.get("store", {}).get("path", f"data/{profile}.db"))
    print(json.dumps(store.stats(), indent=2, ensure_ascii=False))
    pending = store.pending(max_age_days=args.days)
    print(f"in attesa di notifica (ultimi {args.days}gg): {len(pending)}")
    for row in pending[:10]:
        print(f"  {row['first_seen'][:16]} score={row['score']:.1f} {row['title'][:80]}")
    store.close()
    return 0


def cmd_export(args) -> int:
    config = load_config(args.config)
    profile = config.get("profile", "default")
    store = Store(config.get("store", {}).get("path", f"data/{profile}.db"))
    n = store.export_json(args.out)
    store.close()
    print(f"esportati {n} record in {args.out}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="sentinel-digest",
        description="Raccoglie bandi e avvisi pubblici e te li manda filtrati.",
    )
    p.add_argument("--version", action="version", version=f"sentinel-digest {__version__}")
    p.add_argument("-c", "--config", default="config/config.yaml", help="file di configurazione")
    p.add_argument("-v", "--verbose", action="store_true")
    sub = p.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("run", help="esegui una raccolta e invia il digest")
    r.add_argument("--all", action="store_true", help="includi anche item già visti")
    r.add_argument("--dry-run", action="store_true", help="stampa senza inviare né salvare")
    r.add_argument("--profile", help="override del profilo")
    r.set_defaults(func=cmd_run)

    t = sub.add_parser("test", help="verifica che le fonti rispondano")
    t.set_defaults(func=cmd_test)

    d = sub.add_parser("doctor", help="diagnostica configurazione")
    d.set_defaults(func=cmd_doctor)

    s = sub.add_parser("stats", help="statistiche e coda non notificata")
    s.add_argument("--days", type=int, default=7)
    s.set_defaults(func=cmd_stats)

    e = sub.add_parser("export", help="esporta lo storico in JSON")
    e.add_argument("out", nargs="?", default="export.json")
    e.set_defaults(func=cmd_export)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    _setup_log(args.verbose)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())