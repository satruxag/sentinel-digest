# Canali, prezzo e testi — verifica del 2026-11-09

Continua `canali-domanda-ita-2026-11-02.md`, `canali-domanda-ita-2026-10-26.md`.

**Cambio tecnico importante**: in questo giro **Reddit è tornato leggibile** (estrazione pagina
completa via Firecrawl, non più 403 come nei giri precedenti). Ho quindi potuto leggere alla fonte
due thread che valgono più di ogni lista di directory: sono domanda **provata**, non ipotizzata.

---

## 1. DOMANDA PROVATA — thread r/commercialisti (il canale B2B che conta)

### 1a. `1s8otj8` — "Ho creato un sito gratuito per monitorare tutti i bandi e incentivi per le PMI italiane"

- URL: https://reddit.com/r/commercialisti/comments/1s8otj8/
- Tono titolo: **`[Autorizzato Mod]`** → in r/commercialisti la promozione di un proprio prodotto
  **è ammessa se autorizzata dai moderatori**. È la prova che il canale esiste e come si accede.
- Risultato reale: **~58 punti, 23 commenti**. Cioè: il prodotto "aggregatore bandi per PMI" è
  **un problema che i commercialisti riconoscono come proprio**, e un post ben fatto su questo
  tema non viene cancellato.
- Il prodotto concorrente citato è **BandIntelligence.it**, esplicitamente "gratis, senza
  registrazione", "73+ fonti ufficiali", con dashboard e newsletter. L'autore risponde ai
  commenti e reitera aggiungendo feature richieste (filtro no-profit, filtro cultura, alert email).

**Cosa ci dicono i commenti (sono la parte più utile):**
- `u/Open_Jump_5300`: chiede *"un piano intermedio al pro solo per chi ha bisogno del bollettino
  bandi via mail con i criteri di ricerca impostati dall'utente"* → **è letteralmente il nostro
  prodotto**. Lui lo chiede come feature di un sito; noi lo vendiamo come self-hosted.
- `u/Edward_Harlock`: *"utilissima per me che lavoro già su 2-3 progetti diversi. Attendo con
  ansia il piano Pro"* → **esiste gente che pagherebbe un piano a pagamento** per questo.
- `u/Optimal_Doctor7690` (dato fondante, critica al concorrente): il concorrente mostra requisiti
  sintetici che **poi non corrispondono** alla pagina ufficiale del bando. → È il punto debole
  strutturale del concorrente: dati estratti e riassunti, che si rivelano sbagliati. Il nostro
  vantaggio: **noi non riassumiamo, filtriamo e rimandiamo alla fonte**. Va detto nel pitch.
- `u/Solid_Adeptness_43`: critica "p.iva in calce, privacy fatta con chatgpt... AI slop imo".
  → Il pubblico di commercialisti è **allergico all'AI slop**. Un post onesto scritto a mano da
  una persona reale è esso stesso un vantaggio competitivo.

### 1b. `1wn3ov2` — "Automatizzato la ricerca bandi per i commercialisti che seguono la mia azienda"

- URL: https://reddit.com/r/commercialisti/comments/1wn3ov2/
- Questa è **la versione-servizio** del nostro prodotto, già descritta da un terzo (non
  commercialista, lavorava con due studi). Testo originale chiave:
  > *"Mi sono quindi fatto mandare una mail a settimana, già pronta da inoltrare, che dice per
  > ogni bando: quali dei tuoi clienti possono fare domanda e fino a quando... incrocia ogni
  > bando con l'anagrafica clienti (ATECO, sede, forma giuridica, dipendenti)... Arriva come
  > email già impaginata: la leggi e la mandi ai clienti così com'è."*
  > *"I due studi che lo usano sembrano contenti."*
- Poi chiede apertamente: *"Un recap settimanale del genere lo usereste?... Lo vedreste di più
  come servizio interno o come qualcosa da rivendere ai clienti? Se qualcuno vuole provare
  questa cosa in maniera gratuita per 2-3 mesi, scrivetemi pure."*
- Commenti (2, thread piccolo — non è un successo di upvote, ma la **descrizione del servizio
  è oro**):
  - `u/tallá`: *"altro bandosubito, provo io"* → c'è un concorrente che si muove sullo stesso
    terreno, già in questo thread.
  - Critica più importante del giro, di settore: *"il bando lo trovi anche a mano, poi il cliente
    non fa domanda perché è **quasi tutto a rimborso e deve anticipare lui**. E occhio
    all'anagrafica ATECO negli studi, spesso è **vecchia di anni** e il match ti salta senza che
    te ne accorga."*
    → **Due vincoli reali da recepire nel servizio**: (1) il bando trovato non basta, va segnalato
    se richiede anticipo di cassa; (2) il matching per ATECO va validato contro anagrafica
    aggiornata, altrimenti produce falsi positivi.

**Conclusione della sezione**: la domanda è **provata da terzi**, non dedotta. Esiste almeno un
concorrente gratuito generalista (BandIntelligence.it) e almeno un concorrente-servizio
(autore di `1wn3ov2`). Il nostro spazio difendibile **non** è "un altro aggregatore": è
**self-hosted (i dati restano nelle mani dello studio)** + **nessun riassunto, solo filtro con
link alla fonte** (evita il difetto di BandIntelligence) + **preavviso su anticipo di cassa**
(il vero motivo per cui i clienti non fanno domanda).

---

## 2. CANALE NUOVO VERIFICATO — self-hosted.directory

- URL invio: **https://self-hosted.directory/submit** — curl: **HTTP 200**. NON è una pagina
  informativa: è un form vero, ma **richiede il login** ("Sign in required", "You must be signed
  in to submit projects, corrections, or deployment notes").
- La directory pubblica il numero di stelle GitHub di ogni progetto e filtra per
  `FOSS only`, `Docker`, `K8s`, `Low-Resource VPS`. Non dichiara una soglia minima di stelle
  (a differenza di opensaas.directory, §3).
- Categoria pertinente: **Automation** o **Newsletter & Mailing** (esistono entrambe).
- **Perché conta**: è una directory self-hosted **in crescita**, con pubblicazione automatica
  delle metriche GitHub → ogni visitatore vede un progetto "nuovo" con 0 stelle come tale. Non
  è il pubblico PMI/commercialisti (è smanettoni), ma è il canale **più facile** tra quelli
  trovati: un form + un account, nessuna soglia dichiarata.

## 3. CANALE VERIFICATO E **OGGI NON AMMISSIBILE** — opensaas.directory

- URL invio: **https://opensaas.directory/projects/new** — curl: **HTTP 200**, form con account.
- Linee guida lette alla fonte (https://opensaas.directory/guidelines), requisiti **espliciti**:
  - *"At least 50 GitHub stars"* — **verificato automaticamente contro l'URL del repo**;
  - repo pubblico con licenza reale (MIT ok);
  - davvero self-hostabile (Dockerfile/compose);
  - *"commits or releases within roughly the last year"* (ok: ultimo commit 2026-11-06);
  - *"Below the star threshold. Repos under 50 stars don't yet have enough of a track record —
    resubmit once they clear it."*
- **Stato Sentinel Digest al 2026-11-09** (verificato con `gh repo view`): **0 stelle, 0 fork**,
  creato 2026-09-16, **nessun tag**. → **NON ammissibile oggi**, stessa identica barriera di
  awesome-selfhosted: serve prima fare stelle.
- L'unica deroga prevista: *"Fast-growing young projects under the star threshold are considered
  case by case if there's a strong signal of real traction — mention it in your submission."*
  Oggi non c'è alcun segnale di trazione da menzionare, quindi non si applica.

## 4. Cosa serve dal titolare umano (aggiornato)

1. **r/commercialisti — modmail di richiesta autorizzazione**, come nel caso `[Autorizzato Mod]`.
   Il regolamento della wiki del sub è **esplicito**: *"Ogni messaggio promozionale proveniente da
   questi soggetti è del tutto autoreferenziale"* e i servizi fiscali online sono **OT** nel sub.
   La via praticabile è **chiedere prima ai mod** con un messaggio breve e onesto, come ha fatto
   l'autore di BandIntelligence.it. Serve account Reddit con karma (Reddit è leggibile da qui ma
   **non è scrivibile da un agente**: va fatto da una persona).
2. **Taggare `v0.1.0`** (`git tag v0.1.0 && git push --tags`): sblocca sia il conteggio dei 4 mesi
   di awesome-selfhosted, sia è il prerequisito perché le directory mostrino una release.
3. **self-hosted.directory**: creare un account e compilare il form (una persona).
4. **selfh.st**: compilare il modulo (invariato dal giro precedente, serve una persona).
5. **opensaas.directory**: **non fare nulla ora** — tornare quando il repo supera 50 stelle.

---

### Non verificato in questo giro (dichiarato, non dedotto)
- Il testo integrale delle **regole di r/commercialisti** (leggibile solo la wiki; le "rules"
  complete e le modalità esatte di modmail non strisciate riga per riga).
- Se self-hosted.directory accetti progetti senza release taggata o senza Docker.
- Numero di stelle corrente di BandIntelligence.it (non ricavabile senza login GitHub).
