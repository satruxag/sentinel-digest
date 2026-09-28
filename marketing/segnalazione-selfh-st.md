# Segnalazione a selfh.st (directory self-hosted) — testo pronto

Canale: https://selfh.st/submit/ (form "Submit Content", pagina verificata esistente)
Alternativa: repo dati https://github.com/selfhst/selfhst_apps (o awesome-selfhosted/awesome-selfhosted-data)
Stato: NON inviato. Richiede account/compilazione dal titolare umano.

---

## Presentazione (max 8 righe, italiano)

Sentinel Digest raccoglie bandi, contributi e avvisi pubblici italiani da fonti RSS/HTML,
li filtra con parole chiave, pesi e soglie, e manda un digest via email o Telegram.
E' self-hosted: nessun account, nessun SaaS, nessun dato che esce dalla macchina.
Licenza MIT. Zero dipendenze obbligatorie oltre alla libreria standard Python.
Gira in Docker o cron e deduplica gli avvisi con UID stabili.
E' un progetto nuovo, con pochi utenti: chi lo prova contribuisce a farlo crescere.
Repo: https://github.com/satruxag/sentinel-digest

---

## Descrizione breve (per i campi del form / metadati directory)

Nome: Sentinel Digest
Tipo: Self-hosted application
Licenza: MIT
Linguaggio: Python
Categoria suggerita: Feed & Digest / Monitoring / Notifications
Tag: rss, digest, notifications, italy, public-tenders, self-hosted, no-telemetry
Notifier supportati: email (SMTP), Telegram, Slack, Discord, webhook, file
Dipendenze obbligatorie: nessuna (Python standard library; PyYAML opzionale)
Deploy: Docker Compose (run ogni 24h) oppure cron di sistema

## Cosa dichiarare e cosa no

DICHIARARE: licenza MIT, self-hosted, nessun tracciamento, nessun servizio esterno
obbligatorio, progetto nuovo e senza base utenti, repo pubblico.
NON DICHIARARE: utenti, download, clienti, risparmi o numeri di mercato — non sono
verificati e non vanno inventati.

## Nota di ammissibilita'

awesome-selfhosted richiede tipicamente che il progetto sia maturo (criterio storico
"release >4 mesi, attivita' recente"): da verificare sulla guida ufficiale prima del PR.
selfh.st/apps non ha questa soglia dichiarata e resta il canale piu' rapido per un
progetto appena pubblicato.
