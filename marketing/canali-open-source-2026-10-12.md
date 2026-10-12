# Canali di distribuzione per Sentinel Digest — verifica del 2026-10-12

Tutte le regole sotto sono state lette sulle fonti ufficiali il 2026-10-12.
Nessuna registrazione effettuata, nessun contenuto pubblicato: serve il titolare umano.

## Stato del progetto (dato di fatto, non stimato)

- Primo commit: **2026-09-16**. Quindi Sentinel Digest ha **~26 giorni**.
- Tag git presenti: **nessuno**. Release GitHub: **nessuna**.
- Questi due dati decidono l'ammissibilità ai canali sotto. Sono la scoperta principale di questo giro.

## 1. awesome-selfhosted — OGGI NON AMMISSIBILE (gate temporale)

- Canale: https://github.com/awesome-selfhosted/awesome-selfhosted
- Regole reali lette su https://github.com/awesome-selfhosted/awesome-selfhosted-data/blob/master/CONTRIBUTING.md
  (il file CONTRIBUTING.md �� stato spostato dal repo lista al repo `-data`).
- **Regola bloccante, testo letterale dalla fonte**: *"Our guidelines require that Any software
  project you are adding was first released more than 4 months ago. This count initiates only
  after a release has been created"*.
- Sentinel Digest non ha **nessun tag/release** → respinto oggi, indipendentemente dalla qualità.
  Il conteggio dei 4 mesi parte dal **primo tag**, non dal primo commit.
- Criteri di esclusione (sezione "What does not qualify"): software che dipende da un cloud
  specifico; app desktop/mobile/CLI che richiede un programma di sincronizzazione separato;
  librerie/SDK; piattaforme PaaS; tool generici di deployment; porting. **Sentinel Digest non
  ricade in nessuna di queste** → una volta passato il gate temporale è ammissibile.
- Come si sottomette: PR su `software/sentinel-digest.yml` (kebab-case) con template
  `.github/ISSUE_TEMPLATE/addition.md`; oppure issue se non si vuole fare PR.
- Regola nuova e importante: *"Machine/LLM-generated contributions are not allowed and will result
  in a ban."* → la PR va scritta e firmata dal titolare umano, non generata.
- **Azione concreta**: creare un tag/release **oggi** per far partire il contatore; risottomettere
  dal **2027-02** (4 mesi dal primo tag).

## 2. r/selfhosted — ammissibile OGGI, ma solo nel megathread

- Canale: https://www.reddit.com/r/selfhosted/
- Megathread corrente (settimana 08 Oct 2026):
  https://www.reddit.com/r/selfhosted/comments/1x145j7/new_project_megathread_week_of_08_oct_2026/
- **Regola, testo dalla fonte**: *"This weekly thread is the new official home for sharing your new
  projects (younger than three months)... all new projects can only be posted here. Standalone new
  project posts will be removed."*
- Sentinel Digest ha ~26 giorni → **rientra perfettamente** nella finestra "younger than three months".
  Finestra utile: fino a **~2026-12-16** (3 mesi dal primo commit); oltre, non più "new project".
- Cadenza: nuovo thread ogni **venerdì**, ma si può commentare qualsiasi giorno.
- Template obbligatorio richiesto dal thread: Project Name / Repo Link / Description / Deployment /
  **AI Involvement** (trasparenza sull'uso di AI dichiarata esplicitamente).
- Richiede: release effettiva scaricabile + documentazione minima di installazione (Docker/Docker-compose).
  Il repo ha `Dockerfile` e `docker-compose.yml` → requisito coperto.
- Serve: **account Reddit con karma** (gli account nuovi con link esterni vengono rimossi). Nessuna
  registrazione fatta.

## 3. Show HN (Hacker News) — ammissibile, ma non è il pubblico giusto

- Regole ufficiali lette su https://news.ycombinator.com/showhn.html
- Testo letterale: *"Show HN is for something you've made that other people can play with."* e
  *"Please make it easy for users to try your thing out, ideally without barriers such as signups"*.
- Sentinel Digest è eseguibile subito (Docker/pip) senza signup → **ammissibile tecnicamente**.
- Ma: HN è pubblico tecnico internazionale in inglese. **Zero PMI italiane.** Da usare solo per
  visibilità su GitHub/stelle, non per trovare clienti. Priorità bassa.

## 4. r/commercialisti — il canale con domanda reale (confermato dal giro precedente)

- Canale: https://www.reddit.com/r/commercialisti/
- Regola verificata: si pubblica **solo con tag `[Autorizzato Mod]`** (permesso esplicito dei mod).
  Reddit blocca lo scraping diretto delle regole (HTTP 403 su `/about/rules`), quindi la prova
  resta empirica: post di progetti gratuiti nel sub portano quel tag.
- Esempi reali osservati: un progetto gratuito di monitoraggio bandi (bandintelligence.it) ha
  pubblicato con `[Autorizzato Mod]` raccogliendo upvote e commenti operativi; thread
  "Calcolatore gratuito" con tag `(autorizzato mod)`.
- **Azione richiesta**: modmail di richiesta permesso **prima** di postare. Il testo pronto esiste
  già in `marketing/post-reddit-commercialisti-2026-10-05.md`.

## 5. Concorrente open-source diretto trovato oggi (nuovo, non noto prima)

- **BandiRadar** — https://github.com/mayai-it/bandiradar — MIT, Python, creato 2026-06-04,
  102 commit, pacchetto PyPI `bandiradar` v0.20.0: https://pypi.org/project/bandiradar
- Fa la stessa cosa di Sentinel Digest (monitora bandi/incentivi italiani, matching su profilo
  aziendale, CLI) **con in più**: matcher a due stadi con LLM opzionale, 9 fonti live senza API key,
  benchmark ANAC, MCP server, self-healing crawl.
- **Modello di business dichiarato nella sua stessa README**: *open-core* — il motore è MIT e
  pubblico, mentre `bandiradar-pro` (dashboard web, **canali di consegna**, multi-tenant, hosting
  gestito, scheduling SaaS) è privato e a pagamento.
- **Traduzione onesta per Sentinel Digest**: il modello "gratis il motore, si paga la consegna
  gestita" è già stato scelto da un concorrente nella stessa nicchia → conferma che la *filtered
  delivery* è la parte vendibile, non la raccolta. Ma il segnale di trazione è debolissimo:
  il repo ha **2 stelle GitHub** (dato dalla scheda agentmods, 2026-10-12) dopo 4 mesi → in questa
  nicchia l'open source **non porta utenti da solo**. Non contare su GitHub come canale di vendita.

## 6. Il segmento che paga, verificato oggi

- **Fondi+** — https://fondipiu.com/ — dichiara esplicitamente come target *"commercialisti e
  consulenti di finanza agevolata"*, con trial 30 giorni. Argomento di vendita testuale:
  *"Scouting bandi ammissibili per cliente: prima 2–4 ore di ricerca manuale → con Fondi+ <2 minuti"*.
- **Contributi Europa** abbonamento Professional per consulenti/studi associati:
  https://it.linkedin.com/posts/contributi-europa_finanzaagevolata-consulenza-bandi-activity-7389654454616088576-5jm9
- **Bandi Smart, Bando Easy, Trovabando**: fascia 12–133 €/mese (da verifica del 2026-10-05).
- Conclusione: chi **fattura la consulenza** paga per risparmiare ore per cliente. Chi è la PMI
  finale, no. Il compratore è lo **studio/consulente**, non l'impresa.

## Cosa NON ho potuto verificare

- Regole ufficiali scritte di r/commercialisti e r/selfhosted: Reddit risponde 403 allo scraping.
  Le regole di r/commercialisti restano basate su prova empirica (tag osservato), non sul testo dei mod.
- Nessun gruppo Facebook italiano realmente aperto e verificabile: i risultati sono pagine di
  consulenti commerciali (Partner d'Impresa, CNA Bologna, Confcommercio) o un gruppo chiuso
  "Soldi alle Aziende" (https://www.facebook.com/groups/1717828265166195/) di cui non ho potuto
  leggere le regole. **Buco confermato**: nessun forum italiano aperto di PMI trovato.
