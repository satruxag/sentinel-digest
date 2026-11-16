# Testi pronti — 2026-11-16

Tre pezzi: (A) i campi per il form di selfhosttools.com, (B) la modmail unificata per r/impresa
e r/commercialisti, (C) il post per r/ItaliaStartups in formato "riepilogo".

Regola d'uso, valida per tutti: **non pubblicare e non inviare nulla da soli**. Serve la mano
del titolare (account Reddit / invio form). Non dichiarare clienti né numeri: il prodotto non
ha utenti, e dirlo è ciò che lo rende credibile su questi sub.

---

## A) Form selfhosttools.com — https://selfhosttools-suggest.paperform.co/

Nessun account richiesto. Campi tipici di una directory self-hosted; qui i valori da incollare.

- **Name:** Sentinel Digest
- **Tagline (≈60 caratteri):** «Bandi e avvisi pubblici italiani, filtrati via email o Telegram»
- **Repo URL:** https://github.com/satruxag/sentinel-digest
- **License:** MIT
- **Deploy method:** Docker Compose (e cron, senza Docker)
- **Replaces / similar to:** gli aggregatori a abbonamento di bandi italiani (nessuno da nominare
  per esteso: indicare solo «SaaS di monitoraggio bandi»)
- **Category:** Small Business / Automation
- **Descrizione breve (1-2 frasi):**
  «Tool self-hosted che scarica bandi e avvisi pubblici da fonti che dichiari tu (RSS o pagine
  indice), li filtra con le tue keyword e ti manda un digest via email o Telegram. Nessun
  account, nessun dato raccolto: gira sulla tua macchina.»
- **Descrizione lunga (paragrafo):**
  «In Italia i bandi utili stanno su decine di portali tra nazionale, regionale e camerale. Sentinel
  Digest non tenta di riscriverli: prende le fonti che gli dichiari, le controlla con un run
  giornaliero, filtra per keyword e pesi, deduplica con un UID stabile e consegna solo ciò che ti
  riguarda. Rimanda sempre alla fonte ufficiale. Licenza MIT, Docker Compose, config di esempio
  inclusa. Progetto nuovo: cerca riscontri sulle fonti mancanti nella tua regione o settore.»
- **Pricing model:** Free (MIT, self-hosted)
- **Hai una versione hosted/pagata?** No (servizio di setup su richiesta, non un hosted)
- **Logo/screenshot:** da preparare (256×256+ PNG) — il form li chiede; se assenti, inviare comunque.

Nota: se il form chiede un link di ritorno o un badge, **non** procedere senza decisione del
titolare (sporca il README del repo pubblico).

---

## B) Modmail unificata — r/impresa E r/commercialisti

Entrambi i sub **ammettono la promozione previa autorizzazione dei mod** (r/commercialisti:
il post `1s8otj8` è titolato `[Autorizzato Mod]`; r/impresa: "quando in dubbio chiedi ai mod
prima di pubblicare autopromozione"). Serve un account Reddit umano con karma: qui è solo leggibile.

```
Salve mod, sono lo sviluppatore di Sentinel Digest, un tool open source (MIT) self-hosted per
seguire bandi e avvisi pubblici. Non è un servizio: gira sulla macchina di chi lo usa, non
raccoglie dati e non ha account. Ho visto che avete autorizzato post simili (aggregatori di
bandi) e credo possa servire a chi segue PMI e contributi. Vi chiedo se posso pubblicare un
post di presentazione, dichiarando che il progetto è mio, senza link nel testo e senza
pubblicità a pagamento. Se preferite di no, lo rispetto.
```

## B-bis) Post (max 8 righe) — SOLO dopo autorizzazione, valido per entrambi i sub

```
Sono lo sviluppatore di Sentinel Digest, un tool open source che seguo io stesso.
Raccoglie bandi e avvisi dalle fonti pubbliche che gli indichi (RSS o pagine indice), li
filtra con le tue parole chiave e ti manda solo quelli che ti riguardano, via email o Telegram.
A differenza degli aggregatori non riscrive i requisiti (che poi non tornano): ti rimanda
sempre alla fonte ufficiale; e gira sul tuo computer, quindi l'anagrafica clienti non esce
dallo studio. È nuovo, non ha utenti, licenza MIT, nessun dato raccolto.
Se lo provi e mi dici quali fonti mancano per il tuo territorio/settore, lo adatto volentieri:
non vendo nulla, cerco solo riscontri reali.
```

Link al repo **solo** se qualcuno lo chiede in risposta, mai nel primo post.

---

## C) Post r/ItaliaStartups (formato "riepilogo", come `1x8bgtj`)

Anche qui serve il permesso mod. Formato: elenco pragmatico, non pitch.

Titolo: `Riepilogo bandi aperti per PMI/Partite IVA — e un tool open source per non ricontrollarli a mano`

```
Riepilogo rapido delle occasioni aperte ora (fonte: pagine ufficiali, non le riscrivo qui:
il mio punto è proprio rimandare alla fonte).

- MIMIT Investimenti Sostenibili 4.0: 75% spese, 35% fondo perduto + 40% agevolato (Mezzogiorno)
- Marchi+ / Disegni+ 2026: fino all'80% per tutela proprietà industriale
- Voucher internazionalizzazione (varie Regioni): contributi per fiere B2B

Il collo di bottiglia non è trovarli, è il ricontrollo quotidiano su decine di portali.
Ho scritto Sentinel Digest per questo: self-hosted, MIT, prende le fonti che dichiari (RSS o
pagine indice), le filtra con le tue keyword e manda un digest via email o Telegram, senza
raccogliere dati. È nuovo, non ha utenti, non vendo nulla: se lo provi e mi dici quali fonti
mancano nella tua Regione, aggiorno gli esempi.
https://github.com/satruxag/sentinel-digest
```
