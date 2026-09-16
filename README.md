# Sentinel Digest

**Digest self-hosted di bandi e avvisi pubblici.** Raccoglie da fonti pubbliche, filtra con le tue parole chiave, e ti manda solo quello che ti riguarda. Zero servizi esterni, zero dati che escono dalla tua macchina.

```
sentinel-digest -c config/config.yaml run
profilo=bandi-pmi scaricati=63 filtrati=3 nuovi=2 notificati=2 errori=0
```

---

## Perché

Chi cerca bandi, contributi e gare perde tempo a controllare a mano decine di siti.
I servizi commerciali partono da 30-80 €/mese e ti mandano tutto, indistinto.

Sentinel Digest gira **sulla tua macchina**, filtra con le tue regole, e costa zero.

## Caratteristiche

- **Self-hosted**: nessun SaaS, nessun account, nessun tracciamento. La config e i dati restano tuoi.
- **Zero dipendenze obbligatorie**: solo libreria standard Python. `PyYAML` è opzionale (leggi la config in JSON senza nemmeno quello).
- **Deduplica**: ogni avviso ha un UID stabile — non ti arriva due volte.
- **Multi-canale**: email (SMTP SSL/STARTTLS), Telegram, Slack, Discord, webhook generico, o solo file su disco.
- **Filtro serio**: includi/escludi, frasi intere con match sul confine di parola, pesi per far emergere ciò che conta, soglia minima di punteggio, età massima degli avvisi.
- **Fonti dichiarative**: RSS/Atom, o HTML di qualunque pagina indice (con selettore regex per le liste strutturate).

## Installazione

### Docker (consigliata)

```bash
git clone https://github.com/example/sentinel-digest.git
cd sentinel-digest

cp examples/config.example.yaml config/config.yaml
$EDITOR config/config.yaml          # metti le tue keyword

docker compose up -d
docker compose logs -f
```

Il container esegue la run ogni 24 ore. I digest finiscono in `./out/`.

### Senza Docker

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install ".[yaml]"

sentinel-digest -c config/config.yaml doctor   # diagnostica
sentinel-digest -c config/config.yaml test     # verifica le fonti
sentinel-digest -c config/config.yaml run      # esegui
```

### Cron (una volta al giorno, 07:00)

```cron
0 7 * * * cd /opt/sentinel-digest && .venv/bin/sentinel-digest -c config/config.yaml run >> var/run.log 2>&1
```

## Comandi

| Comando | Cosa fa |
|---|---|
| `doctor` | Diagnostica: permessi, fonti valide, notifier configurati |
| `test` | Interroga ogni fonte e mostra i primi item — **usalo prima di ogni run** |
| `run` | Raccoglie, filtra, deduplica, notifica |
| `run --dry-run` | Stampa il digest senza inviare né salvare stato |
| `run --all` | Include anche item già notificati |
| `stats` | Statistiche e coda dei non notificati |
| `export out.json` | Esporta lo storico in JSON |

## Configurazione

Tutto in un file YAML (o JSON). Le credenziali **non** stanno nel file:

```yaml
notify:
  - kind: smtp
    host: smtps.example.it
    port: 465
    tls: ssl
    user: "digest@example.it"
    password: "${SENTINEL_SMTP_PASSWORD}"   # dall'ambiente
    to: ["cliente@example.it"]
```

```bash
export SENTINEL_SMTP_PASSWORD='...'
```

### Filtro

```yaml
filter:
  include_logic: any        # "any" = basta una, "all" = tutte
  include:
    - "bando"
    - "avviso pubblico"     # frase intera
    - "re:contribut[oi]"    # regex esplicita
  exclude:
    - "graduatoria"
  weights:
    "contributo": 2.0       # alza il punteggio, ordina prima
  max_age_days: 45
  min_score: 1
```

### Aggiungere una fonte

```yaml
sources:
  - name: "Portale gare"
    kind: rss
    url: "https://example.it/feed.xml"
```

Per le PA che non hanno RSS, usa la pagina indice:

```yaml
  - name: "Comune - Bandi"
    kind: html
    url: "https://www.comune.example.it/bandi"
    base_url: "https://www.comune.example.it"
    item_pattern: '<a[^>]+href="(?P<url>[^"]+)"[^>]*>(?P<title>[^<]{15,200})</a>'
```

**Verifica sempre** con `sentinel-digest test` prima di affidarti a una fonte: un endpoint morto viene saltato senza rompere la run, ma meglio saperlo.

## Fonti verificate

Gli endpoint in `examples/config.example.yaml` sono testati e funzionanti:

- **AGID** — `https://www.agid.gov.it/it/rss.xml`
- **ANSA Economia** — `https://www.ansa.it/sito/notizie/economia/economia_rss.xml`
- **Il Sole 24 Ore** — `https://www.ilsole24ore.com/rss/italia.xml`

Molti portali istituzionali hanno cambiato struttura e i vecchi feed `/rss` o `?format=feed` rispondono **404**: vanno verificati caso per caso.

## API Python

```python
from sentinel_digest.engine import load_config, run

res = run(load_config("config/config.yaml"))
print(res.summary())      # profilo=... scaricati=... filtrati=... nuovi=...
print(res.errors)         # cosa è andato storto, senza eccezioni
```

## Test

```bash
pip install ".[dev]"
pytest -q
```

## Licenza

MIT — vedi [LICENSE](LICENSE).