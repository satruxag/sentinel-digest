"""Espansione di ${VAR} nella config: le credenziali restano fuori dal file."""

from __future__ import annotations

import os
import re

_PATTERN = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}")


def expand_env(value):
    """Sostituisce ${VAR} con os.environ[VAR] ricorsivamente su dict/list/str.

    Una variabile mancante resta invariata: la config si carica comunque e
    il notifier fallirà con un errore chiaro invece di rompere la run.
    """
    if isinstance(value, dict):
        return {k: expand_env(v) for k, v in value.items()}
    if isinstance(value, list):
        return [expand_env(v) for v in value]
    if isinstance(value, str):
        return _PATTERN.sub(lambda m: os.environ.get(m.group(1), m.group(0)), value)
    return value