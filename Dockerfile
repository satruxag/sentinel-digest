FROM python:3.12-slim

LABEL org.opencontainers.image.title="Sentinel Digest" \
      org.opencontainers.image.description="Digest self-hosted di bandi e avvisi pubblici" \
      org.opencontainers.image.licenses="MIT"

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    TZ=Europe/Rome

WORKDIR /app

# Solo pyproject + sorgenti: nessuna dipendenza binaria da compilare.
COPY pyproject.toml README.md ./
COPY src/ ./src/
RUN pip install --no-cache-dir ".[yaml]" \
 && apt-get update \
 && apt-get install -y --no-install-recommends gosu \
 && rm -rf /var/lib/apt/lists/* /tmp/*

# Config e dati vivono in volumi: l'immagine resta immutabile.
COPY examples/config.example.yaml /app/config/config.example.yaml

# Utente non privilegiato, con UID/GID configurabili al build.
# Serve per allinearsi ai volumi del host: vedi PUID/PGID in docker-compose.
ARG PUID=10001
ARG PGID=10001
RUN groupadd -g ${PGID} sentinel 2>/dev/null || true \
 && useradd -r -u ${PUID} -g ${PGID} -m sentinel \
 && mkdir -p /app/config /app/data /app/out \
 && chown -R sentinel:sentinel /app

# All'avvio allinea i permessi delle directory di lavoro ai volumi montati,
# poi scende ai privilegi dell'utente non privilegiato.
COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

VOLUME ["/app/config", "/app/data", "/app/out"]

ENV SENTINEL_UID=${PUID} \
    SENTINEL_GID=${PGID}

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
CMD ["-c", "/app/config/config.yaml", "run"]