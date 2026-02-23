import time
import sys
import re
from playwright.sync_api import sync_playwright

# Configurazione
YEAR = "2026"
OUTPUT_FILE = "gare_2026.txt"
MONTHS = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", 
          "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]

# Keywords per esplodere le gare raggruppate
# Ordine importante: dal più specifico al più generico
SUB_EVENTS = [
    "ASSOLUTI", "AGE GROUP", "PARATRIATHLON", "PARADUATHLON", "STAFFETTA", 
    "COPPA CRONO", "JUNIOR", "YOUTH", "KIDS", "GIOVANI", "SUPER SPRINT", 
    "MINITRIATHLON", "MINIDUATHLON", "ATIPICO", "CLASSICO", "MEDIO", "LUNGO", 
    "70.3", "IRONMAN", "CROSS", "WINTER", "AQUATHLON", "SPRINT", "OLIMPICO"
]

def clean_text(text):
    return re.sub(r'\s+', ' ', text).strip()

def run():
    print("🚀 MTT SCRAPER V16: MONTH-BY-MONTH PRECISION MODE")
    all_races = []

    with sync_playwright() as p:
        try:
            # Avvio browser
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                viewport={'width': 1920, 'height': 1080}
            )
            page = context.new_page()
            
            print("🔗 Connecting to MyFITri...")
            page.goto("https://www.myfitri.it/calendario", wait_until="networkidle", timeout=60000)
            time.sleep(5)

            # 1. RESET INIZIALE
            print("🧹 Initial Reset...")
            page.evaluate("""() => {
                document.querySelectorAll('.v-chip__close, button[aria-label*="close"]').forEach(el => el.click());
                const tabs = Array.from(document.querySelectorAll('.v-tab'));
                const tutti = tabs.find(t => t.innerText && t.innerText.toUpperCase().includes('TUTTI'));
                if (tutti) tutti.click();
            }""")
            time.sleep(3)

            # 2. ITERAZIONE MESI
            for month in MONTHS:
                print(f"📅 Processing: {month}...")
                
                # Tenta di attivare il filtro mese (match completo o prime 3 lettere)
                clicked = page.evaluate(f"""(m) => {{
                    const elements = Array.from(document.querySelectorAll('.v-tab, .v-chip, span, button'));
                    const target = elements.find(el => {{
                        const txt = el.innerText ? el.innerText.trim().toUpperCase() : "";
                        return txt === m.toUpperCase() || txt === m.toUpperCase().substring(0,3);
                    }});
                    
                    if (target) {{
                        target.click();
                        return true;
                    }}
                    return false;
                }}""", month)
                
                if not clicked:
                    print(f"⚠️  Filter for {month} not found. Trying generic scroll fallback.")
                
                time.sleep(3) 
                
                # Scroll tattico
                page.mouse.wheel(0, 1000)
                time.sleep(1)
                page.mouse.wheel(0, 2000)
                time.sleep(1)

                # ESTRAZIONE DATI
                raw_data = page.evaluate("""() => {
                    const cards = document.querySelectorAll('.v-card');
                    const data = [];
                    cards.forEach(card => {
                        const text = card.innerText || "";
                        if (text.includes('2026')) {
                            const linkEl = card.querySelector('a[href*="/evento/"]');
                            const link = linkEl ? linkEl.href : "";
                            const titleEl = card.querySelector('.v-card__title, .text-h5, .text-h6');
                            let title = titleEl ? titleEl.innerText : "";
                            
                            data.push({ full_text: text, link: link, explicit_title: title });
                        }
                    });
                    return data;
                }""")

                # PROCESSING PYTHON
                count_month = 0
                for item in raw_data:
                    lines = [l.strip() for l in item['full_text'].split('\n') if l.strip()]
                    if len(lines) < 2: continue

                    # Dati base
                    event_title = clean_text(item['explicit_title']) if item['explicit_title'] else clean_text(lines[0])
                    date_match = re.search(r'(\d{2}-\d{2}-2026)', item['full_text'])
                    event_date = date_match.group(1) if date_match else "01-01-2026"
                    
                    # Regione
                    region = "Italia"
                    for l in lines:
                        if any(r in l for r in ["Lombardia", "Veneto", "Piemonte", "Sicilia", "Lazio", "Emilia", "Toscana", "Sardegna", "Campania", "Puglia"]):
                            region = clean_text(l)
                            break
                    
                    location = clean_text(lines[1]).replace(event_date, "").strip() # Rimuove la data dalla riga location
                    if not location: location = "Location Unknown"

                    # Esplosione Gare
                    full_text_upper = item['full_text'].upper()
                    found_sub_events = []
                    
                    # Cerca keywords specifiche
                    for sub in SUB_EVENTS:
                        if sub in full_text_upper:
                            found_sub_events.append(sub)
                    
                    # Logica di deduplica intelligente
                    main_types = ["SPRINT", "OLIMPICO", "MEDIO", "LUNGO", "STAFFETTA", "KIDS", "GIOVANI", "ATIPICO", "SUPER SPRINT", "CLASSICO"]
                    found_main_types = sorted(list(set([t for t in main_types if t in full_text_upper])))
                    
                    if len(found_main_types) > 0:
                        for ft in found_main_types:
                            # Costruisci descrizione completa
                            cats = [c for c in ["ASSOLUTI", "AGE GROUP", "PARATRIATHLON", "U23"] if c in full_text_upper]
                            cat_str = " ".join(cats)
                            
                            # Prefisso sport
                            sport = "Triathlon"
                            if "DUATHLON" in full_text_upper: sport = "Duathlon"
                            elif "AQUATHLON" in full_text_upper: sport = "Aquathlon"
                            elif "WINTER" in full_text_upper: sport = "Winter Triathlon"
                            
                            full_spec = f"{sport} {ft.title()} {cat_str}".strip()
                            entry = f"{event_title} | {event_date} {location} | {region} | {full_spec} | {item['link']}"
                            all_races.append(entry)
                            count_month += 1
                    else:
                        # Fallback generico
                        spec = lines[-1]
                        entry = f"{event_title} | {event_date} {location} | {region} | {spec} | {item['link']}"
                        all_races.append(entry)
                        count_month += 1

                print(f"   > Extracted {count_month} races for {month}.")

                # Reset filtro
                page.evaluate("""() => {
                    document.querySelectorAll('.v-chip__close, button[aria-label*="close"]').forEach(el => el.click());
                }""")
                time.sleep(2)

            # SALVATAGGIO FINALE
            unique_races = sorted(list(set(all_races)))
            
            if len(unique_races) > 10:
                with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                    for line in unique_races:
                        f.write(line + "\n")
                print(f"✨ SUCCESS: {len(unique_races)} unique races extracted and saved.")
            else:
                print(f"⚠️ WARNING: Only {len(unique_races)} races found.")

            browser.close()

        except Exception as e:
            print(f"❌ FATAL ERROR: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    run()
