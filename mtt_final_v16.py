import time
import sys
import re
from playwright.sync_api import sync_playwright

OUTPUT_FILE = "gare_2026.txt"

def run():
    print("🚀 SCRAPER V23: LOGICA ESTRAZIONE PRECISA (PREDAZZO/MAGIONE STYLE)")
    all_final_races = []

    with sync_playwright() as p:
        # Per test locale: headless=False. Per GitHub Action: headless=True.
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 1000})
        page = context.new_page()

        print("🔗 Caricamento MyFITri...")
        page.goto("https://www.myfitri.it/calendario", wait_until="networkidle")
        time.sleep(5)

        print("🧹 Sblocco filtro mese (Logica User)...")
        try:
            months_regex = re.compile(r"Gennaio|Febbraio|Marzo|Aprile|Maggio|Giugno|Luglio|Agosto|Settembre|Ottobre|Novembre|Dicembre", re.IGNORECASE)
            page.locator("span").filter(has_text=months_regex).locator("i").click()
            print("✅ Filtro rimosso.")
        except: pass

        time.sleep(3)

        print("🖱️ Caricamento completo del calendario...")
        for _ in range(45):
            page.mouse.wheel(0, 3000)
            time.sleep(1.0)

        print("📋 Estrazione card e parsing strutturato...")
        raw_cards = page.evaluate("""() => {
            return Array.from(document.querySelectorAll('.v-card'))
                .filter(c => c.innerText.includes('2026'))
                .map(c => ({
                    text: c.innerText,
                    link: c.querySelector('a[href*="/evento/"]')?.href || ""
                }));
        }""")

        print(f"🧐 Analisi di {len(raw_cards)} eventi trovati...")
        
        # Regex per le date abbreviate (es: 10-gen, 18-apr)
        short_date_pattern = re.compile(r'^(\d{1,2}-(?:gen|feb|mar|apr|mag|giu|lug|ago|set|ott|nov|dic))', re.IGNORECASE)

        for card in raw_cards:
            # Dividiamo il testo della card in righe, pulendo spazi e tab
            lines = [l.strip() for l in card['text'].split('\n') if l.strip()]
            if len(lines) < 2: continue
            
            # 1. Titolo Evento (sempre la prima riga)
            event_name = lines[0]
            
            # 2. Data e Regione (cerchiamo la riga che contiene l'anno 2026)
            main_info_line = ""
            for l in lines:
                if "2026" in l:
                    main_info_line = l
                    break
            
            if not main_info_line: continue

            # Estrazione Data Standard (es. 10-01-2026)
            date_match = re.search(r'(\d{2}-\d{2}-2026)', main_info_line)
            standard_date = date_match.group(1) if date_match else "01-01-2026"
            
            # Estrazione Regione (tutto ciò che segue il carattere '|')
            region = "Italia"
            if "|" in main_info_line:
                region = main_info_line.split("|")[-1].strip()

            # 3. Estrazione Specialità (Sottogare)
            # Scorriamo le righe cercando quelle che seguono una data abbreviata
            sub_event_found = False
            for i, l in enumerate(lines):
                if short_date_pattern.match(l):
                    # Abbiamo trovato una data abbreviata (es. 11-gen)
                    # La specialità è solitamente nella riga immediatamente successiva
                    # o nella stessa riga se non ci sono a capo
                    spec_candidate = ""
                    if i + 1 < len(lines) and not short_date_pattern.match(lines[i+1]):
                        spec_candidate = lines[i+1]
                    else:
                        spec_candidate = short_date_pattern.sub("", l).strip()
                    
                    if spec_candidate and not any(s in spec_candidate.upper() for s in ["VAI ALLA", "RANK", "DETTAGLI"]):
                        # Pulizia tabulazioni multiple nel nome specialità
                        spec_candidate = re.sub(r'\t+', ' ', spec_candidate).strip()
                        all_final_races.append(f"{event_name} | {standard_date} | {region} | {spec_candidate} | {card['link']}")
                        sub_event_found = True

            # 4. Fallback per gare singole (se non abbiamo trovato date abbreviate)
            if not sub_event_found:
                # Prendiamo l'ultima riga sensata che non sia un comando
                for l in reversed(lines):
                    if not any(s in l.upper() for s in ["VAI ALLA", "RANK", "DETTAGLI", "2026", "2025"]):
                        all_final_races.append(f"{event_name} | {standard_date} | {region} | {l} | {card['link']}")
                        break

        # Deduplicazione finale
        unique_output = sorted(list(set(all_final_races)))

        if len(unique_output) > 50:
            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                for r in unique_output:
                    f.write(r + "\n")
            print(f"✨ SUCCESS: {len(unique_output)} gare/specialità estratte correttamente!")
        else:
            print(f"❌ Errore: Trovate solo {len(unique_output)} gare.")

        browser.close()

if __name__ == "__main__":
    run()
