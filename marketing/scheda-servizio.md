# Scheda servizio — Sentinel Digest (setup e digest su misura)

Documento interno, da adattare in trattativa. Nessuna promessa di risultati: il servizio è tecnico (configurazione e consegna), non consulenza sul merito dei bandi.

---

## Cosa vendo

Sentinel Digest è un tool open source MIT: raccoglie bandi e avvisi pubblici da fonti dichiarate (RSS o pagine indice), li filtra con keyword e pesi definiti dal cliente, deduplica e consegna un digest via email o Telegram. Gira sulla macchina del cliente, in Docker, con un run giornaliero.

Non vendo il software (è libero e scaricabile da chiunque). Vendo il lavoro che quasi nessuno vuole fare: capire quali fonti contano per quel settore e quella regione, testarle una per una, e scrivere un filtro che non spari dentro rumore.

## Offerta A — Setup e personalizzazione (una tantum)

Consegno:
1. Installazione funzionante (Docker Compose o cron) sulla macchina del cliente.
2. 5-10 fonti selezionate su regione e settore del cliente, ognuna verificata con il comando `sentinel-digest test`.
3. Filtro scritto insieme al cliente: includi/escludi, frasi intere, pesi, soglia minima, età massima degli avvisi.
4. Canale di notifica configurato (email SMTP o Telegram), credenziali fuori dal file di config.
5. Una run di prova consegnata e commentata, più una pagina di istruzioni per cambiare le keyword da soli.

Prezzo: 249-390 EUR, in base al numero di fonti e alla difficoltà dei portali (le PA senza RSS richiedono una regex per pagina).
Tempistica: 3-5 giorni lavorativi dal ricevimento degli accessi.

## Offerta B — Digest su misura ricorrente

Il cliente non installa nulla (o lo fa, e io mantengo la config):
1. Intervista di 1-2 ore su settori, regioni, tipologia di agevolazione e parole da escludere.
2. Configurazione mantenuta e aggiornata: se un portale cambia struttura e una fonte si rompe, la sistemo.
3. Consegna settimanale del digest via email o Telegram, con conteggi (scaricati / filtrati / nuovi).

Prezzo: 49-99 EUR al mese per azienda. 150-250 EUR al mese per studi di consulenza con più profili cliente.
Nota: richiede che il cliente mi dia accesso a una macchina o che io ospiti la run sulla mia infrastruttura (in quel caso i dati del cliente passano da un mio server — da mettere per iscritto).

## Perimetro e limiti (da dire sempre, per iscritto)

- Sentinel Digest non dice se il cliente ha i requisiti per un bando e non compila domande: non è consulenza di finanza agevolata e non sostituisce il consulente.
- Il valore dipende dalla qualità delle fonti dichiarate: se il bando rilevante esce solo come PDF su una pagina senza elenco, il tool può non vederlo.
- Il software è MIT: il cliente può smettere di pagarmi e continuare a usarlo. Il canone copre la manutenzione delle fonti e la configurazione, non una licenza.
- Nessun dato del cliente viene raccolto o rivenduto.

## Primo passo concreto

Offrire una prova gratuita di una run reale sulle fonti del potenziale cliente, senza chiedere carta di credito e senza installare niente da parte sua. È l'unico modo onesto di dimostrare che il filtro funziona prima che esista una referenza.
