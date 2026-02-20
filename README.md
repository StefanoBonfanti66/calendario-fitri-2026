# 🏊‍♂️ FITRI 2026 Season Planner (Evolution)

Una Web App professionale e ultra-veloce per la pianificazione della stagione agonistica di Triathlon, Duathlon e Multisport 2026.

## 🚀 Funzionalità Principali

- **🗺️ Mappa Interattiva**: Visualizza tutte le gare d'Italia su mappa. Marker colorati per sport e icone speciali per i tuoi obiettivi.
- **🎯 Sistema di Priorità A-B-C**:
  - **A (Gold)**: Obiettivi stagionali principali.
  - **B (Blue)**: Gare di preparazione.
  - **C (Grey)**: Allenamenti e test.
- **💰 Budget Planner**: Inserisci i costi di iscrizione e ottieni una stima automatica dei costi di trasferta (carburante/pedaggi) basata sulla distanza da casa.
- **📏 Calcolo Logistica**: Seleziona la tua provincia e scopri istantaneamente quanti KM dista ogni gara.
- **🛡️ Sicurezza Atleta**: Avviso automatico se provi ad aggiungere gare con meno di 3 giorni di recupero tra loro.
- **📅 Export Universale**: Esporta il tuo piano in formato `.ics` per sincronizzarlo con Google Calendar, Outlook o Apple Calendar.
- **📱 PWA (Installabile)**: Aggiungi l'app alla home del tuo smartphone per usarla come un'app nativa, fluida e a tutto schermo.

## ⚙️ Automazione Dati

L'app è "viva". Ogni notte alle **04:00 AM**, una **GitHub Action** esegue automaticamente:
1. Lo script `scraper_playwright.py` per cercare nuove gare sul sito ufficiale FITRI.
2. Il parser per aggiornare il database `races_full.json`.
3. Il deploy automatico su Vercel.

## 🛠️ Note Tecniche

- **Frontend**: React 19 + Vite + Tailwind CSS.
- **Mappe**: Leaflet.js con ottimizzazione INP (Interaction to Next Paint) per fluidità massima.
- **Backend/Scraping**: Python 3.10 + Playwright (Headless Chromium).
- **Hosting**: Vercel.

---
*Sviluppato per Stefano Bonfanti - Stagione Agonistica 2026*
