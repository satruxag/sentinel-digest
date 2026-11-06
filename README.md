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
git clone https://github.com/satruxag/sentinel-digest.git
cd sentinel-digest

mkdir -p config                    # il clone non include config/ (non è nel repo)
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

sentinel-digest -c config/config.yaml doctor   # diagnostica + prova reale del filtro
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
| `doctor` | Diagnostica: permessi, fonti valide, notifier configurati, **e conta quanti item del momento passano davvero il filtro** |
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

### La trappola numero uno: fonti vive, filtro che non pesca

I feed di notizie generaliste (`ANSA Economia`, `Il Sole 24 Ore`) sono ottimi
per provare l'installazione, ma non pubblicano bandi: con le keyword di esempio
pescano **2 item su 64**, e un `include` solo un po' piu' stretto pesca **zero**.
In quel caso la run non da' errore: risponde `filtrati=0` e non notifica niente,
che per chi ha appena installato e' indistinguibile da "il prodotto non funziona".

Per questo `doctor` ora scarica gli item reali e conta quanti passano il filtro:

```
prova reale: 64 item scaricati adesso, 0 passano il filtro
  include=5 exclude=1 min_score=1 max_age_days=45
[FAIL] il filtro non pesca nessuno dei 64 item scaricati adesso: con questa
       config la run notificherebbe zero. Rilassa le keyword di include
       (o abbassa min_score).
```

Se il filtro pesca poco, `doctor` te lo dice prima che sia `run` a farlo.
Per un digest di bandi vero, aggiungi fonti che pubblicano bandi
(vedi sotto) invece di allargare le keyword a caso.

## Fonti verificate

Gli endpoint in `examples/config.example.yaml` sono testati e funzionanti
(ultima verifica: 23/10/2026, con `sentinel-digest test`):

- **Unioncamere** — `https://www.unioncamere.gov.it/rss`
- **ANSA Economia** — `https://www.ansa.it/sito/notizie/economia/economia_rss.xml`
- **Il Sole 24 Ore** — `https://www.ilsole24ore.com/rss/italia.xml`

### Fonti che pubblicano bandi (non solo notizie)

I tre feed sopra servono a verificare che l'installazione funzioni: sono
notizie generaliste, non bandi. Per un digest utile aggiungi portali che
pubblicano avvisi. Questi rispondono e hanno item correnti che parlano di
bandi (verificati il 06/11/2026, conteggio sulla parola "bando" negli item
del momento):

- **Fondazione Cariplo** — `https://www.fondazionecariplo.it/feed` — 10 item, 8 con "bando"
- **Fondazione con il Sud** — `https://www.fondazioneconilsud.it/rss/` — 10 item, 3 con "bando"
- **Fondazione CRC** — `https://www.fondazionecrc.it/feed` — 12 item, 1 con "bando"
- **Federculture** — `https://www.federculture.it/feed` — 10 item, bollettino bandi cultura

Le fondazioni sono le piu' affidabili come fonte di bandi: pubblicano il
bando come titolo, quindi il filtro lo pesca con una keyword sola.

Verifica i titoli con `sentinel-digest test` prima di aggiungerli: molti
portali PA espongono `/rss` che risponde **HTTP 200 con una pagina HTML**,
non un feed — il parser li scarta e la fonte risulta vuota.

Attenzione: gli endpoint pubblici cambiano senza avviso. Il feed AGID
(`https://www.agid.gov.it/it/rss.xml`) risponde ancora **HTTP 200 ma con una pagina HTML
di manutenzione**, non con l'RSS: un caso da manuale di fonte che sembra viva e non lo è.
Molti portali istituzionali hanno cambiato struttura e i vecchi feed `/rss` o `?format=feed`
rispondono **404**: vanno verificati caso per caso.

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