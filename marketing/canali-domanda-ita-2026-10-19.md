# Canali dove esiste domanda — verifica del 2026-10-19

Complementa `canali-open-source-2026-10-12.md` (che copriva awesome-selfhosted, r/selfhosted,
Show HN). Qui la novità è il **canale B2B italiano**, che è quello dove sta la domanda che paga.

Nessuna registrazione effettuata, nessun contenuto pubblicato. Serve il titolare umano.

---

## 1. r/commercialisti — canale CONFERMATO, con meccanismo preciso

Il giro precedente lo dava per "probabile". Ora il meccanismo è verificato su più thread reali.

**Il meccanismo, dedotto da prove ripetute (non dal testo dei mod: Reddit risponde 403 su
`/about/rules` e sull'endpoint `.json`):** si pubblica solo dopo autorizzazione dei mod, e il
tag `[Autorizzato Mod]` nel titolo è l'autorizzazione. Non è una regola letta: è un pattern
osservato su **5 thread indipendenti**, di persone diverse, su mesi diversi.

Thread reali con quel tag (URL verificati il 2026-10-19):

- `https://www.reddit.com/r/commercialisti/comments/1s8otj8/` — BandIntelligence.it, aggregatore
  bandi gratuito per PMI. Tag `[Autorizzato Mod]`, tono "ho risolto un mio problema, feedback gradito".
- `https://www.reddit.com/r/commercialisti/comments/1s3h0zn/` — `[AUTORIZZATO MOD]` tool locale XML→PDF.
- `https://www.reddit.com/r/commercialisti/comments/1o07x4z/` — `(autorizzato mod)` calcolatore fiscale.
- `https://www.reddit.com/r/commercialisti/comments/1m0e8ir/` — `[autorizzato MOD]` AMA.
- `https://www.reddit.com/r/commercialisti/comments/1rzm1ap/` — Economo, gestionale contabile
  **commerciale**, pubblicato SENZA tag: "0 points, 21 comments". Vedi §3, è il contro-esempio utile.

**Conclusione operativa**: il tag non è opzionale per evitare la rimozione, ma è anche il modo in
cui un tool auto-prodotto passa. La richiesta di permesso ai mod va fatta prima, via modmail.
Il testo pronto esiste già: `post-reddit-commercialisti-2026-10-05.md`.

---

## 2. Il caso BandIntelligence — il segnale più forte trovato finora

`https://bandintelligence.it` — HTTP 200 al 2026-10-19. Progetto **indipendente e gratuito**,
quasi identico per funzione a Sentinel Digest (aggrega bandi da fonti ufficiali, schede
requisiti/importi/scadenze, alert). Dichiara in homepage: **756 bandi attivi**, 556 a fondo
perduto, **40 fonti ufficiali monitorate**, 20 regioni.

Perché conta, in breve:

1. È **gratuito e senza registrazione** → conferma che il prodotto "base" ha valore zero come
   bene vendibile. La gratificazione è già occupata.
2. Pubblica **dati aperti** (`/dati-aperti`, HTTP 200: API JSON su `/api/search`, `/api/bandi/<slug>`,
   `/api/barometro`, server MCP su `/api/mcp`; licenza CC BY 4.0). Esiste un concorrente più
   maturo che regala anche l'accesso programmatico.
3. Il suo post su r/commercialisti ha ricevuto il tag dei mod → **quel canale accetta questo tipo
   di annuncio**. Questo è il fatto che sblocca la pubblicazione per Sentinel Digest.

**Non verificabile**: quanti upvote/commenti abbia ricevuto quel post. Reddit risponde 403 sia
all'HTML sia a `.json` senza sessione autenticata. Non invento il numero.

---

## 3. Il contro-esempio che vale più di un successo: Economo

`https://www.reddit.com/r/commercialisti/comments/1rzm1ap/` (21 mar 2026), autore u/Lorenzo_buz,
gestionale contabile commerciale per PMI. Pubblicato **senza** tag `[Autorizzato Mod]`:
**0 punti, 21 commenti**, e i commenti sono ostili — *"Siccome le tue risposte sono praticamente
tutte create da chatgpt o simili, non oso immaginare il tuo (Vibe) codice..."*, *"Quindi software
da singolo sviluppatore garantisce sicurezza, rispetto delle norme..."*.

Lezione per Sentinel Digest: questo pubblico **fiuta il testo generato e lo punisce**, e diffida
del "software di un singolo che tocca dati fiscali". Due conseguenze concrete:

- il testo di presentazione va scritto (o almeno riscritto a mano) dal titolare umano;
- il messaggio deve puntare su **"i vostri dati restano sulla vostra macchina, non c'è un servizio
  che li vede"**. È l'unico argomento che un commercialista non può replicare al concorrente SaaS.

Un secondo thread, `https://www.reddit.com/r/commercialisti/comments/1sl5vro/` ("Sto pensando di
sviluppare un tool per commercialisti"), ha **19 commenti** di professionisti che spiegano cosa non
funziona nei gestionali attuali: è materiale di ricerca sulla domanda, gratis, già raccolto.

---

## 4. Concorrenti — cosa è dichiarato sui loro siti (letto il 2026-10-19)

- **Fondi+** (`https://fondipiu.com/`) — target dichiarato testualmente: *"commercialisti e
  consulenti di finanza agevolata"*. Claim: *"Scouting bandi ammissibili per cliente: prima 2–4 ore
  di ricerca manuale → con Fondi+ <2 minuti"*. Trial: **30 giorni gratis, senza carta**. **Prezzo:
  non dichiarato** — il trial serve a raccogliere contatti prima di fissarlo. Opera come
  **Dynamia SRL, P.IVA 14861180967**.
- **Trovabando Professional** (`https://www.trovabando.it/professional/`) — target: commercialisti
  e consulenti. Dichiara *"oltre 210 enti eroganti"*. Feature distintiva: **il report PDF esce con
  il logo e i colori dello studio**, cioè il consulente lo rivende come proprio. Modello:
  *"abbonamenti trimestrali o annuali"*. **Prezzo: non dichiarato** sulla pagina letta.
- **Bandi Smart** (`https://bandismart.it/`) — FACONSULTING S.R.L., P.IVA IT10590171210. Alert e
  monitoraggio, target ampio (imprese, professionisti, enti). **Prezzo: non dichiarato** (verificato
  con curl: nessuna occorrenza di importi in pagina). Una seconda entità, `bandismart.com`, è in
  **waitlist** con *"Stiamo definendo i piani di abbonamento"* → il mercato è in fase di
  formazione del prezzo.
- **BandiAI** (`https://bandiai.eu/pricing`) — pagina pricing **senza prezzi**; i contatori
  ("0+ bandi monitorati") sono segnaposti non valorizzati → prodotto non ancora popolato.
- **Agevolando** (`https://www.agevolando.eu/`) — "all-in-one" database bandi + consulenza.
  **Prezzo: non dichiarato** (nuovo, non presente nei giri precedenti).

**Fatto rilevante**: sui siti dei cinque concorrenti principali **nessun prezzo è pubblico**.
Per Sentinel Digest non c'è quindi un listino da battere, solo una fascia stimata dai giri
precedenti (12–133 €/mese).

---

## 5. Servizio a pagamento che NON richiede di incassare — proposta

Il vincolo è "senza essere io a incassare". La struttura che lo rispetta è **agenzia/white-label**,
ed è esattamente quella che Trovabando ha già scelto (report con il logo dello studio): il cliente
del consulente non deve mai sapere che sotto c'è uno strumento di terzi.

Tre formule, dalla più leggera alla più solida, tutte fatturabili dal consulente al SUO cliente:

1. **Setup & self-hosting assistito** — installo Sentinel Digest sulla macchina dello studio
   (Docker), configuro le fonti, le parole chiave e i canali di consegna. Una tantum.
   Fascia ragionevole: **150–400 € per studio**, una volta sola. È lavoro tecnico, non richiede
   che il cliente paghi un abbonamento a me.
2. **Digest settimanale "in white label"** — io scrivo la regola di filtro e le fonti per un
   profilo tipo (es. "PMI manifatturiera lombarda"), il consulente riceve il digest e lo rigira
   ai suoi clienti come proprio. Canone **60–150 €/mese per studio**, che il consulente
   ricarica sui suoi assistiti.
3. **Template di configurazione verticale** — pacchetto di config (fonti + filtri + soglie) per
   un settore, venduto una volta e riusabile. **80–200 € per verticale**.

Il punto economico: il consulente fa pagare al cliente ore di consulenza. Se il digest gli fa
risparmiare la ricerca manuale che Fondi+ quantifica in *"2–4 ore per cliente"*, anche 100 €/mese
sono una frazione di una sola ora fatturata. **Non è un prezzo per la PMI finale.** Il compratore
è lo studio, e va scritto così nell'offerta.

---

## 6. Cosa NON ho trovato (risultato, non fallimento)

**Non esiste un forum italiano aperto di PMI sui bandi.** Confermato due volte, in due giri
diversi (2026-10-12 e oggi). Le discussioni avvengono su gruppi Facebook chiusi con approvazione
dei mod e canali Telegram a scrittura limitata, non indicizzati e non leggibili senza account.
Chi vende a questo pubblico passa da LinkedIn uno-a-uno o dai commercialisti, non da un forum
pubblico. La conseguenza pratica è che **il canale Reddit r/commercialisti non è "uno dei tanti":
è l'unico canale pubblico verificato dove questa domanda è raggiungibile.**

## Cosa NON ho potuto verificare

- Testo letterale delle regole dei sub: Reddit 403 su `/about/rules` e su `.json`. Il meccanismo
  del tag è dedotto da pattern osservati, non da una regola letta.
- Metriche (upvote/commenti) del post BandIntelligence: 403.
- Prezzi reali dei concorrenti: **nessuno li pubblica**. "Non dichiarato" è il dato, non una lacuna
  della ricerca.
