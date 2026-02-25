import time
import json
import re
import calendar
from playwright.sync_api import sync_playwright

OUTPUT_FILE = "gare_2026.txt"

def run():
    print("🚀 SCRAPER V32: API COMPLETE SYNC")
    all_final_races = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("🔗 Inizializzazione MyFITri...")
        page.goto("https://www.myfitri.it/calendario", wait_until="networkidle")
        time.sleep(2)

        for month in range(1, 13):
            _, last_day = calendar.monthrange(2026, month)
            start_date = f"2026-{month:02d}-01"
            end_date = f"2026-{month:02d}-{last_day:02d}"
            
            api_url = f"https://cms.myfitri.it/api/eventi?populate=Gare&filters[$and][0][dataInizio][$gte]={start_date}&filters[$and][1][dataInizio][$lte]={end_date}&sort[0]=dataInizio&pagination[limit]=300"
            
            print(f"📅 Mese {month:02d}...")
            
            try:
                response_text = page.evaluate(f"async () => {{ const r = await fetch('{api_url}'); return r.ok ? await r.text() : null; }}")
                if not response_text: continue

                data = json.loads(response_text)
                events = data.get('data', [])
                
                for event in events:
                    attr = event.get('attributes', {})
                    event_title = attr.get('Nome', 'Ignoto').strip()
                    raw_date = attr.get('dataInizio', '2026-01-01')
                    std_date = "-".join(raw_date.split('-')[::-1]) if '-' in raw_date else "01-01-2026"
                    location = attr.get('Localita', 'Località n.d.').strip()
                    
                    # Regione
                    region = "Italia"
                    try:
                        r_data = attr.get('regione', {}).get('data', {})
                        if r_data: region = r_data.get('attributes', {}).get('Nome', 'Italia')
                    except: pass

                    gare_list = attr.get('Gare', [])
                    event_id = event.get('id', '')
                    link = f"https://www.myfitri.it/calendario/evento/{event_id}"

                    if gare_list:
                        for g in gare_list:
                            spec = g.get('Nome', '') or g.get('Descrizione', '') or "Gara"
                            rank = g.get('Rank', '') or ""
                            full_spec = f"{spec} {rank}".strip()
                            all_final_races.append(f"{event_title} | {std_date} | {location} | {region} | {full_spec} | {link}")
                    else:
                        all_final_races.append(f"{event_title} | {std_date} | {location} | {region} | Gara | {link}")

            except Exception as e:
                print(f"   ⚠️ Errore: {e}")

        # SALVATAGGIO
        unique_output = sorted(list(set(all_final_races)))
        if len(unique_output) > 10:
            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                for r in unique_output:
                    f.write(r + "\n")
            print(f"\n✨ SUCCESS: {len(unique_output)} gare salvate in {OUTPUT_FILE}!")
        else:
            print(f"\n❌ Errore: Trovate solo {len(unique_output)} gare.")

        browser.close()

if __name__ == "__main__":
    run()
