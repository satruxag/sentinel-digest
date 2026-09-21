# PR per awesome-selfhosted

Repository di destinazione: https://github.com/awesome-selfhosted/awesome-selfhosted-data
Criteri verificati: software libero (MIT, ok), self-hostabile (ok), non dipendente da SaaS proprietario (ok), mantenuto attivamente, prima release da più di 4 mesi (verificare la data: il primo commit risulta di settembre 2026, quindi la data minima potrebbe non essere ancora raggiunta — controllare prima di aprire la PR).
Regole da rispettare: un solo software per PR, file in kebab-case, PRIMA cercare nelle issue/PR esistenti che non sia già presente, niente termini ridondanti nella descrizione (no "open source", no "self-hosted" — sono impliciti nella lista).

File da creare: `software/sentinel-digest.yml`, basato sul template `.github/ISSUE_TEMPLATE/addition.md`.

Contenuto del file:

```yaml
name: Sentinel Digest
website_url: https://github.com/satruxag/sentinel-digest
description: Aggregates public notices and funding calls from RSS or HTML index pages, filters them by user-defined keywords and sends a digest by email, Telegram, Slack, Discord or webhook.
licenses:
  - MIT
platforms:
  - Python
  - Docker
tags:
  - Feed Readers
  - Miscellaneous
source_code_url: https://github.com/satruxag/sentinel-digest
```

Titolo PR suggerito:
Add Sentinel Digest

Corpo PR suggerito:

- Un solo software in questa PR: Sentinel Digest.
- Cercato in issue e PR, aperte e chiuse: nessuna voce esistente con questo nome.
- Licenza MIT (file LICENSE nel repo).
- Installazione: Docker Compose oppure venv Python; nessuna dipendenza obbligatoria oltre alla standard library.
- Documentazione di installazione: nel README del repository.
- Attività di sviluppo: attiva (vedi commit history).
- Categoria scelta: Feed Readers (aggregatore con consegna via digest). In alternativa Miscellaneous, se i maintainer preferiscono.

---

Nota per il titolare: il canale è legittimo e gratuito, ma richiede un fork e una PR da un account GitHub. Non pubblicare l'annuncio come fosse già accettato: la settimana di attesa dopo l'approvazione è parte del processo della lista.
