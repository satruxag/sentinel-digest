# Testo pronto — post per r/commercialisti

> Prima di pubblicare: inviare modmail ai mod chiedendo il permesso e usare il tag
> `[Autorizzato Mod]`. Vedi `canali-b2b-commercialisti-2026-10-05.md` §5.
> Tono da tool gratuito in cerca di feedback, non da vendita. Non promettere clienti.

---

[Autorizzato Mod] Ho scritto un tool open source per farsi il "bollettino bandi" da soli

Giro sempre gli stessi tre problemi: i bandi sono sparsi tra MIMIT, Invitalia, regioni e
Gazzetta Ufficiale; i servizi commerciali (Bando Easy, Trovabando) partono da 12 €/mese e in
genere mandano tutto indistinto; chi lavora su più clienti vuole invece filtrare con i propri
criteri. Così ho scritto Sentinel Digest: gira sulla vostra macchina (Docker o Python, solo
libreria standard), filtra per parole chiave e frasi intere con pesi e soglia, deduplica, e
consegna via email, Telegram, Slack o webhook. Non è un servizio, non c'è account, non
raccoglie dati: config e storico restano locali. È MIT, quindi lo potete leggere e modificare.

È nuovo e onesto sullo stato: non ha una lista di fonti già pronta da caricare, la config
delle fonti la fate voi (RSS/Atom o pagina indice HTML). Sto cercando feedback da chi lo usa
su casi reali: quali fonti vi servono, cosa manca nel filtro, cosa si rompe.

Repo: https://github.com/satruxag/sentinel-digest
