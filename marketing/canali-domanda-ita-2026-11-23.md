# Canali e domanda — settimana 2026-11-23

Novità di questa settimana: (1) il **Voucher Cloud e Cybersecurity 2026 MIMIT** è
aperto ORA e crea urgenza di spesa software fino al 20 gennaio 2027 — ma **non è
un canale di vendita per noi** (elenco fornitori già chiuso). (2) Scala di prezzi
reale dei concorrenti, letta dalle loro pagine: fissa dove possiamo stare.
(3) Il gruppo Facebook "Finanziamenti & Contributi a Fondo Perduto" è un canale
nuovo, reale e verificato (HTTP 200), con regole NON ancora lette.

## 1) Voucher Cloud e Cybersecurity 2026 (MIMIT) — leva di domanda, NON canale

Fonti primarie/secondarie verificate:
- Pagina ufficiale MIMIT: https://www.mimit.gov.it/it/incentivi/sostegno-alla-domanda-di-servizi-di-cloud-computing-e-cyber-security (HTTP 200)
- Elenco fornitori (Invitalia): https://vcc-elencofornitori.npi.invitalia.it/ (HTTP 403 da qui: non leggibile via curl)
- Dettaglio con date e vincoli: https://www.ticonsiglio.com/voucher-cloud-cybersecurity-2026-contributi-fondo-perduto-imprese/

Fatti verificati:
- Contributo **a fondo perduto del 50%** delle spese, **max 20.000 EUR** (piano da 40.000 EUR per saturare).
- **Spesa minima ammissibile 4.000 EUR** (contributo minimo 2.000 EUR).
- Finestra domande imprese: **dalle 12:00 del 10 novembre 2026 alle 12:00 del 20 gennaio 2027**.
  Procedura **valutativa a sportello** in ordine cronologico: chiude prima se finiscono i 150 mln EUR.
- Spese finanziabili (tra le altre): servizi cloud SaaS, servizi di configurazione, monitoraggio
  e **supporto continuativo**, "compresi i servizi professionali".
- VINCOLO CRITICO: la configurazione/supporto/servizi professionali sono ammessi
  **solo fino al 30% del piano** e **solo se collegati** ad almeno un altro servizio dell'elenco.
- VINCOLO DECISIVO PER NOI: i servizi vanno acquistati **esclusivamente da fornitori iscritti
  nell'elenco MIMIT** (decreto direttoriale 29 luglio 2026). La finestra di iscrizione
  fornitori è **chiusa il 27 maggio 2026** → **oggi non possiamo essere fornitore agevolabile**.
- Esclusi: i servizi cloud a consumo (pay-per-use) e il semplice aggiornamento di versione.

Interpretazione onesta:
- NON possiamo vendere "via voucher" in questo ciclo: l'elenco fornitori è già chiuso.
- MA il voucher È il motivo per cui una PMI/professionista sta decidendo ADESSO se
  spendere in software entro gennaio. Chi si muove entro il 20/01/2027 e compra da un
  fornitore accreditato recupera metà della spesa.
- Uso corretto: **leva di urgenza nel testo verso consulenti/PMI**, non promessa di sconto.
  Chi compra da noi NON recupera il voucher (non siamo in elenco): va detto chiaramente.
  Chi vuole il voucher deve comprare da un fornitore dell'elenco (es. Serverplan, cloud provider accreditati).

## 2) Scala prezzi concorrenti (per posizionare l'offerta)

Prezzi letti dalle pagine dei concorrenti (non stimati):
- Simatica: ~9,90 EUR/mese (entry-level)
- Finanza Lab: ~19,90 EUR/mese
- Bando Easy: da ~49 EUR/mese (Silver) fino a centinaia; 2400+ bandi + consulenza
- Bandi d'Italia: ~149 EUR/anno
- iCRIBIS RADAR: ~850 EUR/anno
- R4 (Bandimpresa): ~390 EUR/anno

Conseguenza: NON conviene competere sul prezzo mensile (siamo un tool, non un servizio
di consulenza). Il nostro spazio è **one-off / self-hosted**: nessun abbonamento,
nessun dato che esce dalla macchina. Offerta a prezzo una tantum, non ricorrente.

## 3) Canale nuovo: gruppo Facebook "Finanziamenti & Contributi a Fondo Perduto"

- URL: https://www.facebook.com/groups/844335092261376/ (HTTP 200 verificato)
- 200+ gruppi FB / community di finanza agevolata pubblicano bandi aperti e scadenze.
- Regole del gruppo NON lette (Facebook blocca lo scraping senza login): da verificare
  a mano prima di pubblicare. Richiede **account Facebook del titolare umano**.
- Altri gruppi/pagine visti: "Contributi Regionali a Fondo Perduto – Infomedia",
  "Finanza Agevolata Strategica", "Associazione Imprenditori Italia", CNA Bologna.

## 4) Canali directory (stato aggiornato)

- selfh.st/apps: submit page verificata 2026-11-23 (https://selfh.st/submit/, HTTP 200,
  form Formbricks) — l'unica directory self-hosted **senza soglia di stelle/release**.
- awesome-selfhosted: regola letta alla fonte (CONTRIBUTING.md): *"first released more
  than 4 months ago"*, contatore dal **primo tag**. Repo oggi senza tag → respinto.
- opensourcealternative.to / openalternative.co: richiedono stelle (50+) o sono a pagamento.

## Azione bloccante unica (vale per tutte le directory)

`git tag v0.1.0 && git push --tags` — non eseguito: richiede decisione del titolare umano
(versione pubblica). Sblocca awesome-selfhosted (dal 2027-02) e dà credibilità "release".

## Cosa serve dal titolare umano
1. `git tag v0.1.0 && git push --tags` (una riga, sblocca le directory).
2. Compilare il form selfh.st/submit (nessun account richiesto) e selfhosttools.com.
3. Account Facebook per il gruppo 844335092261376 (prima leggere le regole).
4. Decidere se usare il Voucher MIMIT come leva di urgenza nel testo (non come sconto).
