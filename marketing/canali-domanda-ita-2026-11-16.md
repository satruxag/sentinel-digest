# Canali di domanda reali — 2026-11-16

Novità di questo giro rispetto al 2026-11-09: la domanda è **provata da terzi** su più sub,
e sono emersi **canali di pubblicazione senza registrazione** e un **dato di prezzo di mercato**
che contraddice parte del listino in `scheda-servizio.md`.

## 1. Domanda provata (thread reali, leggibili)

- `r/impresa` — `1x54ag5` "Chi gestisce una PMI, come scopre i bandi a cui può accedere?"
  https://www.reddit.com/r/impresa/comments/1x54ag5/
  Il post è stato rimosso dai filtri Reddit ma i **commenti restano**: un terzo (`u/micardisplus`)
  dice «è una domanda che mi sono fatto più spesso… ho sentito più volte da imprenditori e
  associazioni della necessità di un supporto così»; un altro cita **CONTRIBUTI EUROPA** come
  soluzione esistente; un altro ancora raccomanda il «Commercialista di finanza agevolata».
  → Conferma doppia: (a) il bisogno è sentito e dichiarato da terzi, (b) l'incumbent noto è
  Contributi Europa — informazione utile, non un ostacolo: significa che il mercato esiste.

- `r/commercialisti` — `1s8otj8` (già noto) e `1wn3ov2` (già noto) restano i riferimenti
  "autorevoli": il primo è `[Autorizzato Mod]`, quindi la promozione è ammessa previa modmail.

- `r/ItaliaStartups` — `1x8bgtj` "Riepilogo veloce dei bandi e contributi a fondo perduto in
  apertura tra fine Ottobre e Novembre 2026 per PMI e Partite IVA".
  https://www.reddit.com/r/ItaliaStartups/comments/1x8bgtj/
  → Formato "riepilogo periodico" che il sub gradisce: un digest è esattamente la stessa forma.
  Pubblico affine al nostro, ma serve il permesso mod (regola del sub).

Nessuno di questi thread è spam: sono domande vere con risposte vere. Il canale �� maturo.

## 2. Canali di pubblicazione: novità operative

### a) selfhosttools.com — PUBBLICABILE SENZA ACCOUNT (novità)
- https://selfhosttools.com/ (HTTP 200 verificato con curl)
- Ha **226 tool**, 17 categorie, tra cui **"Small Business" (52 tool)** — il pubblico PMI/consulenza.
- Il bottone "Submit a tool" punta a un **modulo esterno Paperform**:
  https://selfhosttools-suggest.paperform.co/ (HTTP 200 verificato, **nessun login richiesto**).
- Il sito dichiara: «We review every submission within 48 hours. **No account needed.**»
- Requisiti impliciti: nome, tagline, descrizione, **repo URL, licenza esatta (MIT)**, deploy (Docker).
- → È il canale **più azionabile emerso finora**: zero registrazione, zero account, solo il form.
  Da compilare a mano dal titolare (io non invio form a nome suo).

### b) self-hosted.directory — richiede account + badge di ritorno (già noto, riconfermato)
- https://self-hosted.directory/submit — free tier richiede un **badge link-back** sul sito
  (se rimosso, ti depubblicano) e revisione fino a 30 giorni; tier Basic 9,9 USD / Pro 29,9 USD
  una tantum. **Non lo consiglio ora**: il badge sporca il README e il rapporto costo/beneficio
  è peggiore del punto (a).

### c) opensaas.directory — ancora NON ammissibile
- https://opensaas.directory/ — 142+ progetti, soglia implicita di **visibilità/stelle**.
  Con 0 stelle il progetto non ha trazione: **rimandare**.

### d) openalternative.co — richiede login
- https://openalternative.co/submit → redirect a `/auth/login` (verificato). Serve account.
  Directory a pagamento/verificata: rimandare finché non esiste una release taggata.

## 3. Intuito di prezzo (correzione importante)

Questa settimana è emerso un secondo listino concorrente, **Bando Easy**
(https://www.bandoeasy.it/studi-finanza-agevolata), che cambia il quadro:

- Piano **Freelance da 60 EUR/mese** (fino a 25 clienti); la pagina FAQ cita anche **«€100 al mese»**
  per il piano studio. Un'altra pagina dello stesso sito parla di **«tutti i piani a partire da
  12 EUR/mese»** per la parte imprese.
- Posizionamento dichiarato: «il sistema operativo per studi specializzati in finanza agevolata»,
  con match automatico cliente-bando, PDF white-label, storico de minimis.
- Aggregatore **incentivimpresa.it** (https://www.incentivimpresa.it/monitoraggio-bandi-automatico-consulenti)
  cita «piattaforme dedicate **da 1.500 euro/anno**» per il monitoraggio automatico strutturato.
- **Banchedati.biz** (https://www.banchedati.biz/abbonamenti-appalti): piani appalti
  **54 / 108 EUR/mese** (Studio Professionale / Impresa).

Conseguenza per `scheda-servizio.md`:
- L'Offerta B a **49-99 EUR/mese** è **in linea** col mercato basso (Bando Easy Freelance 60).
- L'Offerta B a **150-250 EUR/mese per studi** è **sopra** la fascia media dei concorrenti
  "leggeri" (54-108 EUR/mese), ma **sotto** le piattaforme strutturate (1.500 EUR/anno ≈ 125 EUR/mese).
  → Restare nella fascia 120-180 EUR/mese per gli studi, non 250.
- L'Offerta A una tantum (249-390 EUR) resta valida come *una tantum*: è la forma che evita il
  confronto diretto con gli abbonamenti mensili e con l'obiezione "ma è MIT, lo scarico gratis".

## 4. Testo pronto

`presentazione-2026-11-16.md` contiene:
- (A) Il testo per il **form Paperform di selfhosttools.com** (non è un post: sono campi).
- (B) La **modmail unificata** valida per r/impresa E per r/commercialisti (stessa regola:
  chiedere prima ai mod).
- (C) Il post r/ItaliaStartups, formato "riepilogo" in linea con `1x8bgtj`.

## 5. Cosa serve dal titolare umano

1. Compilare il form selfhosttools.com (2 minuti, nessun account) — **l'unica azione veramente
   a costo zero e immediata**.
2. Modmail a r/impresa e r/commercialisti (serve account Reddit con karma: non scrivibile da qui).
3. `git tag v0.1.0 && git push --tags` — sblocca sia awesome-selfhosted sia la credibilità
   "release" richiesta da opensaas/openalternative.
