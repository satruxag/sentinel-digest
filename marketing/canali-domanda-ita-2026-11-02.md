# Canali, prezzo e testi — verifica del 2026-11-02

Continua `canali-domanda-ita-2026-10-26.md`. Giro di verifica: **Reddit resta irraggiungibile da
questo host** (403 anche su `about.json` e sulla ricerca, con UA da browser), quindi nessun dato
Reddit nuovo. In compenso sono stati **verificati per la prima volta con curl gli endpoint reali**
di due canali (selfh.st e formazioneturismo.com) e **letti i requisiti alla fonte** di
awesome-selfhosted. Nessuna registrazione, nessun contenuto pubblicato.

---

## 1. CANALE NUOVO — selfh.st (directory + newsletter self-hosted, ~35.000 lettori)

- URL di invio: **https://selfh.st/submit/** — verificato ora con curl: **HTTP 200** (61 KB).
- Non è una pagina informativa: è un modulo reale (**Formbricks**, "Submit Content"), con **tre
  destinazioni distinte**:
  1. `Self-Host Weekly` (la newsletter settimanale)
  2. `selfh.st/apps` (la directory di software self-hosted, https://selfh.st/apps/)
  3. `Icon Request`
- La newsletter dichiara **35.000+ lettori** (https://selfh.st/) — è il pubblico esatto di Sentinel
  Digest: gente che installa da sé, non compratori di SaaS.
- Il contatto diretto è https://selfh.st/contact/ (HTTP 200), con email/Bluesky/Mastodon pubblici.
- **Perché conta**: è l'unico canale trovato che ha (a) un modulo di invio aperto e funzionante,
  (b) un pubblico in target, (c) una categoria ovvia per il prodotto. Non serve karma né account
  con anzianità: si compila un form.
- **Rischio dichiarato**: la newsletter è curata, non un elenco automatico. Un invio può essere
  ignorato. Non ho verificato se accettano progetti senza release taggata (vedi §3).

## 2. CANALE NUOVO (di nicchia) — forum.formazioneturismo.com

- URL: https://www.formazioneturismo.com/forums/ — verificato con curl: **HTTP 200** (156 KB),
  forum **XenForo** vivo, con registrazione via **Google o Facebook OAuth** (nessuna email
  aziendale richiesta).
- Ha un **albero di sezioni dedicato ai bandi**, non generico:
  `bandi-abilitazione-accompagnatore-turistico`, `bandi-esame-direttore-tecnico-agenzia-viaggi`,
  `campania-bandi-e-discussioni-esame-direttore-tecnico-agenzia-viaggi`, più
  `contabilita-tasse-e-imposte-alberghi-e-turismo`.
- **Limite onesto**: è **turismo-specifico** (hotel, agenzie viaggi, B&B, property manager), non un
  forum PMI generalista. Il valore è che *quelle* imprese cercano bandi e hanno commercialisti che
  non capiscono il loro settore (thread `66963` letto: "mi sono confrontato con diversi
  commercialisti e non ne hanno idea").
- Da leggere prima di postare: regolamento del forum (`/forums/help/terms` e le regole di sezione).

## 3. awesome-selfhosted — VERIFICATO: NON ANCORA AMMISSIBILE

Requisito letto alla fonte, repo dati corretto
(https://github.com/awesome-selfhosted/awesome-selfhosted-data/blob/master/CONTRIBUTING.md):

> "Any software project you are adding was first released more than 4 months ago."

Verifica sul repo Sentinel Digest (`git log`, `git tag`):
- **nessun tag, nessuna release** (`git tag -l` → vuoto);
- primo commit **2026-09-16**.
→ con il conteggio che parte *solo dopo la prima release taggata*, oggi **non è ammissibile**. Serve
prima taggare una release (es. `v0.1.0`) e poi aspettare 4 mesi. **Azione concreta per il titolare:**
`git tag v0.1.0 && git push --tags` adesso, così la finestra inizia a decorrere.

Altri requisiti rilevanti già letti: "non-working software may be removed", "unmaintained software
without an active community may be removed", **"Machine/LLM-generated contributions are not allowed
and will result in a ban"** → la PR va scritta e firmata a mano dal titolare, non generata.

## 4. Prezzo concorrenti — secondo listino pubblico verificato

Letto ora su https://info.agevolando.eu/prezzi/ (HTTP 200):

- **Essential** — una sola provincia — **119 EUR + IVA / anno**
- **Standard** — micro, piccole e medie imprese — **297 EUR + IVA / anno** (alert automatici via
  email quando l'azienda risulta idonea; demo gratuita su https://opendemo.agevolando.eu/)
- **ProfilaPro** — commercialisti, consulenti, agenzie — **697 EUR + IVA / anno** (su richiesta)
- Extra: analisi iniziale di un esperto a **39 EUR + IVA** invece di 150 EUR (bonus post-abbonamento)

Incrociato con il dato della scorsa settimana (Contributi Europa Professional **24,99 EUR+IVA/mese =
~249 EUR+IVA/anno**), il quadro è coerente:

- **PMI singola: 120–300 EUR/anno** è il prezzo di mercato del solo *alert*. Il nostro una tantum di
  **249–390 EUR** è quindi una tantum, non un abbonamento: va comunicato come tale o sembra caro.
- **Studio/consulente: 700 EUR/anno** per il tier professionale. La licenza di 249–390 EUR/anno
  (già in `scheda-servizio.md`) è **sotto il mercato** e difendibile.
- Nessuno dei due è self-hosted: entrambi sono SaaS con i dati del cliente sui loro server. Questo
  resta l'unico argomento che i concorrenti **non possono** copiare.

## 5. Testo pronto — invio a selfh.st (max 8 righe, in inglese: la directory è internazionale)

Da incollare nel modulo su https://selfh.st/submit/ (sezione **selfh.st/apps**) o da inviare a
`Ethan` via https://selfh.st/contact/. **Da rivedere a mano dal titolare prima dell'invio.**

```
Sentinel Digest — self-hosted digest of Italian public grants and notices.
Collects from declared public sources (RSS/Atom, or any index page via regex), filters with
your own keywords, weights and threshold, deduplicates by stable UID, and delivers by email,
Telegram, Slack, Discord or webhook. Runs in Docker on your own machine.
MIT licensed, standard library only, no external service, no account, no telemetry.
Repo: https://github.com/satruxag/sentinel-digest
Built for Italian bandi/avvisi, but the source layer is declarative, so it works for any
RSS or index page. New project, no users yet — feedback on missing sources welcome.
```

## 6. Cosa serve dal titolare umano (invariato + nuovo)

1. **Compilare il modulo selfh.st** — serve una persona, non un agente (regola anti-LLM).
2. **Taggare la prima release** (`git tag v0.1.0`) — sblocca il conteggio dei 4 mesi per
   awesome-selfhosted.
3. **Registrarsi su formazioneturismo.com** (Google/Facebook OAuth) se si vuole quel canale.
4. **Reddit**: account con karma + modmail a r/commercialisti + riscrittura manuale — come da
   report del 2026-10-26, niente è cambiato (Reddit resta 403 da qui).

---

### Non verificato in questo giro (dichiarato, non dedotto)
- Contenuto del modulo Formbricks di selfh.st oltre le 3 destinazioni (il form è caricato via JS,
  i campi non sono nell'HTML statico).
- Se selfh.st accetta progetti senza release taggata.
- Regolamento di formazioneturismo.com (pagina terms non letta riga per riga).
- Qualsiasi dato Reddit: host bloccato con 403 su `.json` e ricerca.
