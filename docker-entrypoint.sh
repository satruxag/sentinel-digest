#!/bin/sh
# Entrypoint: sistema i permessi dei volumi, poi esegue come utente non privilegiato.
#
# Perché serve: i volumi montati dal host appartengono spesso a root o a un UID
# diverso. Senza questo passaggio la run fallisce con "Permission denied" su
# data/ e out/ — un problema che si manifesta solo in Docker, mai in locale.
set -e

UID_TARGET="${SENTINEL_UID:-10001}"
GID_TARGET="${SENTINEL_GID:-10001}"

if [ "$(id -u)" = "0" ]; then
    for d in /app/config /app/data /app/out; do
        if [ -d "$d" ]; then
            # Assegna la proprietà senza toccare i file già presenti nel volume.
            chown "$UID_TARGET:$GID_TARGET" "$d" 2>/dev/null || true
        fi
    done
    # Scende ai privilegi dell'utente applicativo e riesegue questo script.
    exec gosu "$UID_TARGET:$GID_TARGET" "$0" "$@"
fi

exec sentinel-digest "$@"