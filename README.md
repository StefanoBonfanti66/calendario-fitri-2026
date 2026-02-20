# FITRI 2026 Calendar Planner (Evolution)

Questo progetto è pronto per essere pubblicato online su **Vercel** con aggiornamenti automatici tramite **GitHub Actions**.

## 🚀 Come Pubblicare in 3 Semplici Passaggi

### 1. Carica su GitHub
Dal tuo terminale (nella cartella del progetto):
```powershell
git init
git add .
git commit -m "Initial commit: Ready for Vercel"
# Crea un nuovo repository su GitHub e collegalo:
git remote add origin https://github.com/TUO_UTENTE/NOME_REPO.git
git branch -M main
git push -u origin main
```

### 2. Collega a Vercel
1. Vai su [vercel.com](https://vercel.com/) e fai il login con GitHub.
2. Clicca su **"Add New Project"** e seleziona questo repository.
3. **IMPORTANTE**: In "Root Directory", seleziona la cartella `app`.
4. Clicca su **"Deploy"**.

### 3. Attiva l'Automazione Notturna (GitHub)
Il sistema è già configurato per aggiornarsi ogni notte alle 04:00. 
Se vuoi testarlo subito su GitHub:
1. Vai nella scheda **"Actions"** del tuo repository su GitHub.
2. Seleziona **"Update Fitri Calendar 2026"**.
3. Clicca su **"Run workflow"**.

---

## 🛠️ Funzionalità Integrate
- ✅ **Aggiornamento Automatico**: GitHub Actions lancia Playwright ogni notte per scaricare i nuovi dati dal sito FITRI.
- ✅ **Calcolo Distanza**: Selezionando la tua provincia, l'app calcola i KM per ogni gara.
- ✅ **Export Calendario**: Pulsante per generare il file `.ics` universale per Google/Outlook/Apple.
- ✅ **Sicurezza Atleta**: Avviso automatico se scegli gare con meno di 3 giorni di recupero.
- ✅ **Filtri Avanzati**: Filtra per regione, sport o distanza.

**Nota:** Il sistema usa GitHub Actions (gratuito) per gestire lo scraping pesante, così Vercel rimane leggero e veloce sia su cellulare che su PC.
