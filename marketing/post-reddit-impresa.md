# Post per r/impresa e r/StartupFinanceItalia

Nota operativa: r/impresa e r/StartupFinanceItalia sono più piccoli e tolleranti verso i post "ho creato", ma il tono deve restare da progetto in costruzione, senza linguaggio commerciale. Un link solo, in fondo. In r/ItaliaStartups serve il permesso dei mod prima.

---

Titolo: Ho scritto un tool open source per non perdere i bandi della propria regione — è nuovo, cerco feedback

Ciao. Da tempo mi capitava di scoprire bandi già chiusi, perché in Italia le informazioni stanno su decine di portali diversi: nazionale, regionale, camerale, più le pagine indice dei singoli enti.

Sentinel Digest è un tool self-hosted, licenza MIT, che fa tre cose: scarica da fonti dichiarate (RSS o HTML), filtra con le tue keyword e i tuoi pesi, e manda un digest via email o Telegram. Deduplica gli avvisi con un UID stabile, così non arriva due volte la stessa cosa. Zero account, zero dati che escono dalla tua macchina, gira in Docker con un run al giorno.

Onestà: è nuovo, non ha clienti, e non ha un database di bandi già pronto — sei tu a dichiarare le fonti che ti interessano (con una config di esempio con AGID, ANSA Economia e Il Sole 24 Ore). È utile se sai già quali portali contano per il tuo settore e vuoi smettere di controllarli a mano.

Se lo provi e mi dici quali fonti mancano nella tua regione, aggiorno gli esempi. Non vendo nulla e non raccolgo iscrizioni.

https://github.com/satruxag/sentinel-digest
