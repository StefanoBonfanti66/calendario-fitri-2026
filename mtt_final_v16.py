import time
import sys
import re
from playwright.sync_api import sync_playwright

OUTPUT_FILE = "gare_2026.txt"

def run():
    print("🚀 SCRAPER V26: FIXED PADOLA & INTERNATIONAL EVENTS")
    all_final_races = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 1000})
        page = context.new_page()

        print("🔗 Caricamento MyFITri...")
        page.goto("https://www.myfitri.it/calendario", wait_until="networkidle")
        time.sleep(5)

        print("🧹 Sblocco filtro mese...")
        try:
            months_regex = re.compile(r"Gennaio|Febbraio|Marzo|Aprile|Maggio|Giugno|Luglio|Agosto|Settembre|Ottobre|Novembre|Dicembre", re.IGNORECASE)
            page.locator("span").filter(has_text=months_regex).locator("i").click()
            print("✅ Filtro rimosso.")
        except: pass

        time.sleep(3)

        print("🖱️ Scrolling completo...")
        for _ in range(45):
            page.mouse.wheel(0, 3000)
            time.sleep(1.0)

        print("📋 Analisi e cattura...")
        raw_cards = page.evaluate("""() => {
            return Array.from(document.querySelectorAll('.v-card'))
                .filter(c => c.innerText.includes('2026'))
                .map(c => ({
                    text: c.innerText,
                    link: c.querySelector('a[href*="/evento/"]')?.href || ""
                }));
        }""")

        short_date_pattern = re.compile(r'^(\d{1,2}-(?:gen|feb|mar|apr|mag|giu|lug|ago|set|ott|nov|dic))', re.IGNORECASE)

        for card in raw_cards:
            lines = [l.strip() for l in card['text'].split('\n') if l.strip()]
            if len(lines) < 2: continue
            
            event_name = lines[0]
            
            # CORREZIONE: Cerchiamo la riga della data SALTANDO il titolo (lines[0])
            # perché il titolo potrebbe contenere "2026" (es. Padola)
            main_info_line = ""
            for l in lines[1:]:
                if "2026" in l:
                    main_info_line = l
                    break
            
            # Fallback se non trovata nelle righe successive
            if not main_info_line: main_info_line = lines[0]

            # Cerchiamo la data standard (es. 27-02-2026)
            date_match = re.search(r'(\d{2}-\d{2}-2026)', main_info_line)
            standard_date = date_match.group(1) if date_match else "01-01-2026"
            
            # Estrazione Città
            location = "Località n.d."
            region = "Italia"
            if "|" in main_info_line:
                parts = main_info_line.split("|")
                region = parts[-1].strip()
                # Pulizia città: rimuove data, 'dal', 'al' e spazi
                city_raw = re.sub(r'.*?\d{2}-\d{2}-2026', '', parts[0])
                city_raw = city_raw.replace('dal', '').replace('al', '').strip()
                if city_raw: location = city_raw
            else:
                # Se non c'è la pipe, proviamo a estrarre la regione dalle righe
                for l in lines:
                    if any(r in l for r in ["Veneto", "Lombardia", "Piemonte", "Toscana", "Lazio", "Sicilia"]):
                        region = l
                        break

            # Sottogare
            sub_event_found = False
            for i, l in enumerate(lines):
                if short_date_pattern.match(l):
                    spec = lines[i+1] if (i+1 < len(lines) and not short_date_pattern.match(lines[i+1])) else short_date_pattern.sub("", l).strip()
                    if spec and not any(s in spec.upper() for s in ["VAI ALLA", "RANK", "DETTAGLI"]):
                        all_final_races.append(f"{event_name} | {standard_date} | {location} | {region} | {spec} | {card['link']}")
                        sub_event_found = True

            if not sub_event_found:
                for l in reversed(lines):
                    if not any(s in l.upper() for s in ["VAI ALLA", "RANK", "DETTAGLI", "2026", "2025"]):
                        all_final_races.append(f"{event_name} | {standard_date} | {location} | {region} | {l} | {card['link']}")
                        break

        unique_output = sorted(list(set(all_final_races)))
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            for r in unique_output:
                f.write(r + "\n")
        
        print(f"✨ SUCCESS: {len(unique_output)} gare salvate.")
        browser.close()

if __name__ == "__main__":
    run()
