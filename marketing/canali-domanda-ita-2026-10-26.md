# Canali e prezzo — verifica del 2026-10-26

Continua `canali-domanda-ita-2026-10-19.md`. Novità di questo giro: **la regola di r/impresa letta
davvero** (fino a ieri non era leggibile) e **il primo prezzo pubblico di un concorrente B2B**.
Nessuna registrazione effettuata, nessun contenuto pubblicato: serve il titolare umano.

---

## 1. r/impresa — canale NUOVO, con la regola letta nero su bianco

- URL: https://www.reddit.com/r/impresa/ — 3.7K iscritti, sub "Public: anyone can view, post,
  and comment", creato lug 2023. Pubblico vero di titolari di PMI italiane, non speculatori.
- **Le 5 regole sono state lette** su https://www.reddit.com/r/impresa/about/ (l'HTML di quella
  pagina si è caricato; `/about/rules.json` resta 403). Citazione letterale della regola 3:

  > "**No pubblicità!** Per evitare che il sub diventi esclusivamente una vetrina di ad, è vietato
  > fare post pubblicitari di attività. Anche velati, copywriterosi, linkedinosi, o 'scrivetemi in
  > privato'."

- **Conseguenza operativa, non interpretabile**: il testo `post-reddit-impresa.md` è **a rischio
  rimozione così com'è**. Finisce con "Se lo provi e mi dici quali fonti mancano... non vendo nulla
  e non raccolgo iscrizioni" + link al repo: è la forma esatta che la regola vieta ("velati",
  "linkedinosi"). Il testo va rifatto come **domanda**, non come presentazione di prodotto, e
  senza link nel corpo.
- Perché resta il canale migliore nonostante questo: la regola vieta il post pubblicitario, non la
  **risposta pertinente**. Lì c'è il thread `1x54ag5` (vedi §2) dove la domanda è posta
  esplicitamente e la risposta utile non è pubblicità.
- Nota di merito: la regola 1 esclude chi ha "partita IVA ma non fa impresa" → il pubblico di
  r/impresa è il **compratore finale (PMI)**, non lo studio. Il canale per lo studio resta
  r/commercialisti (26K iscritti, wiki `Regolamento` su `/wiki/index/regolamento`, non ancora
  letta perché 403).

## 2. Domanda misurata, con le citazioni (thread r/impresa `1x54ag5`)

`https://www.reddit.com/r/impresa/comments/1x54ag5/chi_gestisce_una_pmi_come_scopre_i_bandi_a_cui/`
— "Chi gestisce una PMI, come scopre i bandi a cui può accedere?". Titolo e corpo letti; il corpo
è di un altro sviluppatore che sta costruendo la stessa cosa e chiede feedback. **I commenti non
sono leggibili** (la stessa URL via `old.reddit.com` dà 403): non riporto né upvote né numero di
commenti, non li ho.

Perché conta: un imprenditore commenta *"Avevo pensato anch'io che potesse essere una soluzione
interessante da proporre al mercato. Ho sentito più volte, da diversi imprenditori e associazioni
di categoria, della necessità di sviluppare un supporto di questo tipo"* — cioè **la domanda è
dichiarata dal lato dell'offerta**, da più di una persona. Attenzione: la stessa frase prosegue con
*"se vuoi parlarne o collaborare, mandami un messaggio"* → è un concorrente/concorrente-potenziale,
non un cliente. Va trattato come tale.

Due obiezioni di merito, sempre dal thread, che l'offerta deve assorbire e non negare:
- *"in Italia [le imprese] non accedono a bandi perché l'imprenditore medio non investe... solo a
  fronte di contributi a fondo perduto per percentuali superiori al 60% MINIMO"*;
- un altro commento: *"per accedere devi già essere abbastanza strutturato e ordinato. Vincere un
  bando implica controlli e non sempre sono facili"*.
- E il nome di un concorrente che non avevamo: **"CONTRIBUTI EUROPA"** (§3).

## 3. Contributi Europa — PRIMO prezzo pubblico trovato in questa fascia

`https://www.contributieuropa.com/abbonamento-professional/` (pagina letta il 2026-10-26, HTTP 200):

- **Professional: 24,99 € + IVA / mese**, oppure **249 € + IVA / anno** (pagamento carta/PayPal/bonifico).
- Target dichiarato testualmente: *"Consulenti in finanza agevolata; Studi che vogliono ottimizzare
  tempi e processi; Commercialisti e liberi professionisti che vogliono offrire servizi per la
  finanza agevolata"*.
- Feature che contano per il posizionamento: matching automatico su **fino a 50 profili cliente**,
  elenchi dinamici salvati, **report PDF brandizzati col logo dello studio**, accesso alla
  documentazione ufficiale, richiesta di supporto al loro network di consulenti.
- Sul sito dichiarano *"oltre 800 misure attive"* e, sul piano Premium, una **"GARANZIA NESSUN
  BANDO: garantiamo nei 12 mesi almeno un Bando a cui puoi aderire, altrimenti ti rimborsiamo
  5,75 €"** — quest'ultima è la loro pagina, riportata perché dice quanto poco valgano le garanzie
  di risultato in questo mercato.
- Esistono anche piani verticali a prezzo pubblico nello shop: corsi in **5 moduli da 180 €**
  ciascuno, percorso completo **720 €** (era 900 €).

**Correzione al quadro precedente**: il 2026-10-05 avevo scritto che nessun concorrente pubblica
prezzi. Non è più vero: **Contributi Europa è il benchmark pubblico nella fascia "studio"**.
Contributi Europa **non è self-hosted** (portale + area riservata + account): la differenza con
Sentinel Digest resta quella, non il prezzo.

## 4. Prezzo aggiornato — conseguenza del §3

Il listino reale, adesso che è noto, dice questo:
- fascia bassa (professionista singolo, tool nudo): **Bando Easy 12–69 €/mese** (già verificato il 10-05);
- fascia studio, multi-cliente, con report brandizzati: **Contributi Europa 24,99 €/mese** (249 €/anno)
  e **Trovabando Professional 50–133 €/mese**;
- quindi il **tier "studio" sta a 25–70 €/mese**, non a 60–150 €/mese come stimato il 10-19.

Offerta corretta di conseguenza (nessuna cifra inventata, sono i due listini sopra):
1. **Setup & self-hosting assistito, una tantum — 249–390 € per studio.** Non è in concorrenza
   frontale col SaaS: è l'unico modo per avere il digest **dentro casa**, senza che i dati dei
   clienti passino da un portale di terzi.
2. **Configurazione verticale riusabile — 90–200 € per verticale** (fonti + filtri + soglie di un
   settore/regione), vendibile una volta e riusabile.
3. **Canone di manutenzione fonti — 25–49 €/mese per studio**, cioè **sotto** il Professional di
   Contributi Europa e giustificato dal fatto che è manutenzione tecnica, non una licenza: se una
   PA cambia struttura e la fonte si rompe, è quello che il canone copre. È l'unico prezzo
   difendibile, perché contro "gratis e self-hosted" non si vende il software, si vende il lavoro.

La scheda `scheda-servizio.md` va riallineata: oggi dice "49–99 €/mese per azienda / 150–250 €/mese
per studi", che è sopra il listino reale dello studio.

## 5. Testo pronto — aggiornato alle regole di r/impresa (§1)

Il file `post-reddit-impresa.md` esistente **non è pubblicabile** su r/impresa come post: viola la
regola 3. Sostituirlo con una **domanda**, che è il contenuto che la regola non vieta:

Titolo: `Come tenete traccia dei bandi che cambiano ogni settimana?` (nessuna parola commerciale, nessun link nel corpo)

Ciao. Gestisco una piccola attività e sto provando a mettere ordine sul monitoraggio: in Italia le
informazioni stanno su decine di portali diversi (nazionale, regionale, camerale, più le pagine
indice dei singoli enti) e mi capita di scoprire bandi già chiusi.

Voi come fate oggi? Fate ricerche a mano, vi affidate al commercialista, o avete un metodo che
regge nel tempo? E soprattutto: che cosa vi fa perdere più tempo — trovare i bandi, o capire se
la vostra azienda ci rientra?

Ve lo chiedo perché sto costruendo uno strumento mio per farlo in automatico, quindi ho interesse
a capire cosa serve davvero e cosa invece è tempo perso. Non ho nulla da vendere e non raccolgo
contatti: mi interessa solo capire se il problema è sentito come lo sento io.

Poi, **solo nei commenti** e solo se qualcuno chiede "cosa stai usando", si risponde con una riga e
il link al repo. Il regolamento vieta il post, non la risposta pertinente.

## 6. Cosa serve dal titolare umano (nessuna di queste posso farla io)

1. **Account Reddit con karma reale** — un account nuovo, solo per postare, viene rimosso da AutoMod
   (già concluso il 10-19, riconfermato).
2. **Modmail a r/commercialisti** per il permesso e il tag `[Autorizzato Mod]` (meccanismo verificato
   su 5 thread, non è una regola letta).
3. **Riscrivere il testo a mano** — il contro-esempio Economo (`r/commercialisti/comments/1rzm1ap/`,
   0 punti, 21 commenti ostili al "testo da ChatGPT") resta la prova che questo pubblico fiuta il
   testo generato.
4. **Decisione sul canale**: r/impresa (risposta/domanda, pubblico PMI) oppure r/commercialisti
   (post autorizzato, pubblico studio). Sono due offerte diverse: al primo si vende setup+canone
   PMI, al secondo il white-label per lo studio.
5. **Leggere il `Regolamento` di r/commercialisti** (`/wiki/index/regolamento`): da qui risponde 403,
   dal browser dell'umano si legge.

## Cosa NON ho potuto verificare

- Commenti e metriche di `1x54ag5` su r/impresa: 403 anche via `old.reddit.com`. Il corpo del post
  sì, i commenti no → non riporto numeri.
- Regolamento di r/commercialisti: 403 senza sessione autenticata.
- Qualsiasi gruppo Facebook: non indicizzato, non leggibile senza account (riconfermato, è un
  risultato e non una lacuna).
