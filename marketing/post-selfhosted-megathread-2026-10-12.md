# Post pronto — r/selfhosted "New Project Megathread" (settimana del 2026-10-08)

Da pubblicare come **commento** nel megathread corrente, non come post autonomo
(le regole: i post di progetto fuori dal megathread vengono rimossi).
Megathread: https://www.reddit.com/r/selfhosted/comments/1x145j7/new_project_megathread_week_of_08_oct_2026/

Serve: account Reddit con karma minimo (altrimenti AutoMod rimuove i link). Non pubblicare da account nuovo.
Il template del thread chiede: Project Name / Repo Link / Description / Deployment / AI Involvement.

---

**Text (inglese, per il pubblico di r/selfhosted):**

Project Name: Sentinel Digest

Repo Link: https://github.com/satruxag/sentinel-digest

Description: Self-hosted digest of Italian public grants and tenders. Pulls from public RSS/HTML sources, filters with your own keyword rules, and sends only what matches — by email, Telegram, Slack, Discord, webhook, or plain file. Deduplication via stable UID, so nothing arrives twice. Built for small Italian businesses and accountants who currently check dozens of sites by hand. It's MIT, has no accounts, no telemetry, and sends no data anywhere. Honest note: it's new (~1 month), standard-library-only, and it is not a list provider — the public portals already give the raw lists for free; the point here is the filtered delivery on the channel you already use.

Deployment: Python 3, standard library only (PyYAML optional). `git clone` + `cp examples/config.example.yaml config/config.yaml` + `docker compose up -d`, or `pip install` and run the CLI. Config is a single YAML/JSON file.

AI Involvement: None. No LLM in the code path, no model calls, no AI-generated code in the repo (I can confirm this because I wrote and tested it directly).

---

## Versione italiana (se il canale fosse un forum/community IT)

Sentinel Digest — digest self-hosted di bandi e avvisi pubblici italiani.
https://github.com/satruxag/sentinel-digest
Legge fonti pubbliche (RSS/HTML), filtra con le tue parole chiave e ti manda solo quello che ti
riguarda: email, Telegram, Slack, Discord, webhook o file. Deduplica su UID stabile. MIT, nessun
account, nessun tracciamento, nessun dato che esce dalla tua macchina. È nuovo (circa un mese) e
"honest disclosure": non è un elenco di bandi — quelli i portali pubblici li danno già gratis;
il valore è la consegna filtrata dove la usi già. Docker o pip, config in un solo file YAML.
Nessun uso di AI nel codice.
