# 🏊‍♂️ MTT Milano Triathlon Team - Season Planner 2026

Una Web App professionale e ultra-veloce progettata per gli atleti del **MTT**, dedicata alla pianificazione strategica della stagione agonistica 2026.

## 🚀 Visione del Progetto
L'app trasforma il calendario testuale ufficiale FITRI in uno strumento interattivo di gestione sportiva. Permette agli atleti di visualizzare la distribuzione geografica delle gare, valutare l'impatto logistico ed economico e organizzare i propri picchi di forma (Periodizzazione A-B-C).

## ✨ Funzionalità Evolute

### 🧭 Navigazione & Logistica
- **🗺️ Mappa Interattiva**: Visualizzazione dinamica di tutte le gare d'Italia con marker differenziati per sport.
- **📏 Calcolo Distanze**: Integrazione di un database di coordinate per il calcolo istantaneo dei KM dalla base di Milano (o altra provincia).
- **🏎️ Performance UI**: Ottimizzata con React 19 Transitions per un passaggio istantaneo tra vista Lista e Mappa.

### 🎯 Gestione Atleta
- **📈 Sistema di Priorità A-B-C**: Classificazione delle gare tra obiettivi stagionali (A), gare di preparazione (B) e allenamenti (C).
- **🛡️ Safety Check**: Algoritmo di monitoraggio del recupero che avverte l'atleta in caso di gare troppo ravvicinate (< 3 giorni).
- **📅 Sincronizzazione**: Esportazione universale in formato `.ics` compatibile con Google Calendar, Outlook e Apple Calendar.

### 💰 Budgeting
- **💸 Financial Planner**: Gestione dei costi di iscrizione e stima automatica delle spese di viaggio basata sulla distanza chilometrica.

## 🤖 Automazione & Tecnologia
L'applicazione è basata su un'architettura **"Live-Data"**:
- **Backend Crawler**: Script Python + Playwright che monitora il sito FITRI ogni notte.
- **Data Pipeline**: Elaborazione automatica tramite GitHub Actions che aggiorna il database JSON.
- **Frontend**: React 19, TypeScript, Tailwind CSS, Leaflet.js.
- **PWA**: Completamente installabile su dispositivi iOS e Android come app nativa.

---
*Sviluppato per MTT Milano Triathlon Team - Stagione 2026*
