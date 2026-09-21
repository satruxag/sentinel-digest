# Sentinel Digest — opportunità commerciali

Data ricerca: 2026-09-21. Regola: nessun numero di mercato inventato, nessun cliente dichiarato. Solo canali verificati con URL reale e domanda documentata.

---

## 1. Dove esiste domanda reale (evidenza raccolta)

| Canale | URL | Evidenza di domanda |
|---|---|---|
| r/commercialisti (Reddit) | https://www.reddit.com/r/commercialisti/ | Thread "Bandi e finanza agevolata: ve ne occupate?" — commercialisti che chiedono apertamente come fanno monitoraggio: https://www.reddit.com/r/commercialisti/comments/1r2m9bk/bandi_e_finanza_agevolata_ve_ne_occupte/ |
| r/commercialisti — promo autorizzate dai mod | https://www.reddit.com/r/commercialisti/comments/1s8otj8/autorizzato_mod_ho_creato_un_sito_gratuito_per/ | Post di terzi con tag "[Autorizzato Mod]" per un aggregatore bandi (BandIntelligence.it): il canale accetta presentazioni di tool, previo permesso mod |
| r/StartupFinanceItalia | https://www.reddit.com/r/StartupFinanceItalia/comments/1n3ma2l/come_muoversi_per_scovare_e_monitorare_bandi/ | Utente: "A monitorare i bandi sono una frana... mi sento perso e con la sensazione che potrebbe essermi sfuggito qualcosa" |
| r/impresa | https://www.reddit.com/r/impresa/ | 2,8k membri, PMI/imprenditori italiani; già discussioni su software self-hosted "a basso canone mensile" |
| r/PA_Italia | https://www.reddit.com/r/PA_Italia/comments/1sqz9q0/ho_creato_unai_che_analizza_i_bandi_di_gara_in_10/ | Precedente di presentazione tool bandi/gare ben accolto |
| r/ItaliaStartups | https://www.reddit.com/r/ItaliaStartups/ | Promozione ammessa solo con permesso dei mod (regole riportate da threadotter: https://threadotter.com/subreddit-rules/italiastartups) |
| awesome-selfhosted (directory) | https://github.com/awesome-selfhosted/awesome-selfhosted-data | Canale di distribuzione FOSS: PR con file software/<nome>.yml basato sul template .github/ISSUE_TEMPLATE/addition.md |
| selfh.st (directory self-hosted) | https://selfh.st/submit/ | Form "Submit Content" per segnalare progetti self-hosted |

Conferme dagli operatori di mercato (il monitoraggio è un servizio pagato, non un'ipotesi):
- TeamSystem Finanza d'Impresa è venduto ai commercialisti come piattaforma con "database aggiornato di opportunità di contributi e incentivi" per studio (https://www.studiolaporta.it/finanza-agevolata-e-gestione-bandi-studio-la-porta-al-fianco-delle-imprese-con-teamsystem).
- AGEVIA vende BandoPro, "l'unico software gestionale disegnato esclusivamente per i consulenti di finanza agevolata" (https://agevia.com/servizi).
- Bandit è una piattaforma per studi/consulenti con demo commerciale (https://www.landing.getbandit.it/).

Cosa NON ho trovato: nessun gruppo Facebook pubblico verificabile sui bandi (la ricerca su site:facebook.com non ha restituito risultati utili e i gruppi richiedono account). Nessun forum italiano aperto, attivo e dedicato esclusivamente a bandi/PMI con traffico misurabile.

---

## 2. Servizio a pagamento che si può offrire

Modello scelto: il titolare non incassa direttamente su una piattaforma terza — vende setup/consulenza su fattura, il cliente paga e ospita il software sulla propria macchina.

| Offerta | Cosa comprende | Prezzo suggerito |
|---|---|---|
| Setup e personalizzazione (una tantum) | Installazione Docker/cron, 5-10 fonti della regione/settore del cliente testate con `sentinel-digest test`, keyword e pesi scritti insieme al cliente, notifier email/Telegram configurato, run di prova verificata | 249-390 EUR una tantum (+90-150 EUR se il cliente vuole il presidio continuativo) |
| Digest su misura ricorrente (per azienda X) | 1-2 ore di intervista su settori/regioni/interessi; fonti e filtri configurati; consegna settimanale via email/Telegram | 49-99 EUR/mese per azienda |
| Pacchetto studi di consulenza | Profili multi-cliente, report per cliente, 3 profili | 150-250 EUR/mese |

Ancoraggio di prezzo: i SaaS concorrenti stanno 30-80 EUR/mese (dichiarato nel README del repo) e la fascia è coerente con TeamSystem/AGEVIA/Bandit, che vendono software di gestione pratica ai commercialisti. Il setup è tenuto sotto le 4 ore di lavoro per essere vendibile da soli.

Punto di forza vendibile, verificato nel codice: il tool è autosufficiente (Docker + cron), non richiede account, non fa uscire dati dalla macchina del cliente, e supporta email/Telegram/Slack/Discord/webhook (README, docker-compose.yml, examples/config.example.yaml).

---

## 3. Testi pronti (non pubblicare senza decisione del titolare)

- post-reddit-commercialisti.md — post per r/commercialisti, da inviare prima ai mod come modmail
- post-reddit-impresa.md — variante per r/impresa e r/StartupFinanceItalia
- messaggio-linkedin.md — messaggio diretto a consulenti di finanza agevolata
- pr-awesome-selfhosted.md — titolo, descrizione e corpo PR per la directory
- scheda-servizio.md — scheda offerta (setup + digest su misura) da usare in trattativa

## 4. Cosa serve dal titolare umano

1. Account Reddit con karma non nullo per postare in r/commercialisti / r/impresa / r/StartupFinanceItalia (non posso registrarne uno).
2. Invio della modmail di richiesta permesso prima di qualsiasi post promozionale.
3. Fork di awesome-selfhosted/awesome-selfhosted-data + apertura PR (il repo upstream non accetta push diretti).
4. Decisione su prezzo e perimetro (setup una tantum vs canone) prima di rispondere a qualsiasi interessato.
5. Un contatto email/dominio di appoggio per raccogliere le richieste: oggi Sentinel Digest non ha landing page né form.
