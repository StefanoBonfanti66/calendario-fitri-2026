# 🏊‍♂️ MTT Milano Triathlon Team - Season Planner 2026

Una Web App professionale progettata per gli atleti del **MTT**, dedicata alla pianificazione strategica e analitica della stagione agonistica 2026.

## 🚀 Visione del Progetto
L'app trasforma il calendario ufficiale FITRI in un ecosistema interattivo. Grazie a un motore di acquisizione dati di ultima generazione, permette di gestire ogni aspetto della stagione con precisione chirurgica.

## ✨ Funzionalità Elite

### 🧭 Logistica & Navigazione Avanzata
- **🗺️ Mappa Interattiva**: Pin colorati per sport e icone speciali per gli obiettivi A.
- **📏 Raggio d'Azione**: Slider per filtrare le gare entro una specifica distanza chilometrica dalla propria provincia.
- **📍 Direct Go!**: Integrazione con Google Maps per avvio rapido del navigatore verso la località di gara.
- **🌡️ Smart Prep (Meteo)**: Analisi dei dati storici medi (temperatura e pioggia) per ogni località e data.

### 🎯 Gestione & Diario Atleta
- **📈 Dashboard Analitica**: Riepilogo automatico (Focus Target, Mix Discipline, KM totali).
- **📝 Diario di Gara**: Note personali persistenti per ogni evento (strategie, alimentazione).
- **🎒 Smart Checklist**: Lista attrezzatura dinamica basata sullo sport (Triathlon, Duathlon, Cross, Winter).
- **🛡️ Safety Check**: Algoritmo di protezione del recupero tra gare ravvicinate.

### 📸 Social & Export
- **🖼️ Social Card Generator**: Creazione di infografiche professionali per Instagram (Stagione o Singola Sfida).
- **📅 Sincronizzazione**: Esportazione in `.ics` (Calendario) e `.csv` (Excel) con inclusione di note e priorità.

## 🤖 Automazione & Stack (V33 High-Tech)
- **Crawler**: Python + Playwright con **accesso diretto alle API MyFITri**. Gestione automatica di eventi multi-gara (es. Campionati Italiani, Circuiti Giovanili) con esplosione delle sottogare.
- **Data Engine**: Parsing intelligente con estrazione automatica del Rank (Gold/Silver/Bronze) e separazione Comune/Provincia.
- **Frontend**: React 19, TypeScript, Tailwind CSS, Leaflet.js.
- **Hosting**: Vercel con pipeline di deploy continuo collegata a GitHub.

---
*www.milanotriathlonteam.com • Stagione 2026*
