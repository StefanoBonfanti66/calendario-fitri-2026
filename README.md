# 🏊‍♂️ MTT Milano Triathlon Team - Season Planner 2026

Una Web App professionale progettata per gli atleti del **MTT**, dedicata alla pianificazione strategica e analitica della stagione agonistica 2026.

## 🚀 Visione del Progetto
L'app trasforma il calendario ufficiale FITRI in un ecosistema interattivo. Permette agli atleti di gestire ogni aspetto della stagione: dalla logistica geografica all'analisi climatica, fino alla condivisione social dei propri obiettivi.

## ✨ Funzionalità Elite

### 🧭 Logistica & Navigazione Avanzata
- **🗺️ Mappa Interattiva**: Pin colorati per sport e icone speciali per gli obiettivi A.
- **📏 Raggio d'Azione**: Slider per filtrare le gare entro una specifica distanza chilometrica.
- **📍 Direct Go!**: Integrazione con Google Maps per avviare il navigatore verso la gara con un clic.
- **🌡️ Smart Prep (Meteo)**: Analisi dei dati storici medi (temperatura e pioggia) per ogni località e data.

### 🎯 Gestione & Diario Atleta
- **📈 Dashboard Analitica**: Riepilogo automatico della stagione (Focus Target, Mix Discipline, KM totali).
- **📝 Diario di Gara**: Note personali persistenti per ogni evento (strategie, alimentazione, setup tecnico).
- **🎒 Smart Checklist**: Lista dell'attrezzatura necessaria generata automaticamente in base allo sport (Triathlon, Duathlon, Cross, Winter).
- **🛡️ Safety Check**: Algoritmo di protezione del recupero (< 3 giorni).

### 📸 Social & Export
- **🖼️ Social Card Generator**: Creazione di infografiche professionali per Instagram (Stagione intera o singola sfida).
- **📅 Sincronizzazione Totale**: Esportazione in `.ics` (Calendario) e `.csv` (Excel) con inclusione di note e priorità.

## 🤖 Automazione & Stack
- **Crawler**: Python + Playwright con sblocco dinamico dei filtri MyFITri.
- **Pipeline**: GitHub Actions per il refresh settimanale automatico dei dati.
- **Frontend**: React 19, TypeScript, Tailwind CSS, Leaflet.js.
- **Hosting**: Vercel con Analytics integrato per il monitoraggio degli accessi.

---
*www.milanotriathlonteam.com • Stagione 2026*
