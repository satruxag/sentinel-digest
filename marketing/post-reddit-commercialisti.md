# Post per r/commercialisti (da inviare PRIMA ai mod come modmail)

Nota operativa: r/commercialisti accetta post di tool solo con permesso dei mod (esiste un precedente in prima pagina con tag "[Autorizzato Mod]"). Quindi: inviare il testo come modmail, NON pubblicare direttamente. Non pubblicare link a pagamento nel primo post.

---

## Testo modmail (breve, per i moderatori)

Buongiorno, sono Rosario. Ho letto il thread "Bandi e finanza agevolata: ve ne occupate?" e molti commenti lamentano il punto debole del monitoraggio: le fonti sono decine e frammentate.

Ho scritto un tool open source MIT, self-hosted, che raccoglie avvisi pubblici e bandi, li filtra con keyword definite dall'utente e manda un digest via email o Telegram. Non è un servizio: nessun account, nessun dato che esce dalla macchina di chi lo usa.

Non vendo niente in questo post e non chiedo iscrizioni. Chiedo se posso pubblicare una presentazione con il link al repository, senza offerta commerciale, raccogliendo feedback su quali fonti mancano. Se preferite, lo tengo come commento dentro il thread esistente invece di aprire un post nuovo. Grazie.

---

## Bozza di post (se i mod autorizzano)

Titolo: Ho scritto un tool open source (MIT, self-hosted) per il monitoraggio di bandi e avvisi pubblici — cerco feedback sulle fonti

Ciao a tutti. Nel thread sui bandi ho visto che il problema comune non è trovare un bando, è non perderne uno: le fonti sono decine tra MIMIT, Invitalia, portali regionali e pagine indice dei comuni.

Ho scritto Sentinel Digest: raccoglie RSS e pagine HTML, filtra con le keyword e i pesi che decidi tu (includi/escludi, frasi intere, soglia minima), deduplica con un UID stabile e invia un digest via email/Telegram/Slack/webhook, oppure solo su file. Gira in Docker con un cron giornaliero. Licenza MIT, nessun account, nessun tracciamento, i dati restano sulla tua macchina.

Cosa non è: non è una piattaforma, non ha database di bandi pronto all'uso, e per le PA che non espongono RSS va configurata una regex sulla pagina indice. È nuovo e non ha clienti.

Repository: https://github.com/satruxag/sentinel-digest

Se lo provate: quali fonti vi mancano? Mi interessa sapere dove il filtro sbaglia, non raccogliere iscrizioni.
