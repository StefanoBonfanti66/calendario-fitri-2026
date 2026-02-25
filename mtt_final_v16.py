import time
import json
import re
import calendar
from playwright.sync_api import sync_playwright

OUTPUT_FILE = "gare_2026.txt"

def run():
    print("🚀 SCRAPER V33: API MAPPING PERFECTED")
    all_final_races = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("🔗 Inizializzazione sessione MyFITri...")
        page.goto("https://www.myfitri.it/calendario", wait_until="networkidle")
        time.sleep(2)

        for month in range(1, 13):
            _, last_day = calendar.monthrange(2026, month)
            start_date = f"2026-{month:02d}-01"
            end_date = f"2026-{month:02d}-{last_day:02d}"
            
            # URL con populate=Gare e limit=300 per prendere tutto il mese
            api_url = f"https://cms.myfitri.it/api/eventi?populate=Gare&filters[$and][0][dataInizio][$gte]={start_date}&filters[$and][1][dataInizio][$lte]={end_date}&sort[0]=dataInizio&pagination[limit]=300"
            
            print(f"📅 Recupero Mese {month:02d}...")
            
            try:
                response_text = page.evaluate(f"async () => {{ const r = await fetch('{api_url}'); return r.ok ? await r.text() : null; }}")
                if not response_text: continue

                data = json.loads(response_text)
                events = data.get('data', [])
                
                for event in events:
                    # MAPPATURA ESATTA DAI TUOI DATI
                    event_title = event.get('denominazione', 'Ignoto').strip()
                    event_id = event.get('id', '')
                    region = event.get('regione', 'Italia').strip()
                    comune = event.get('comune', '').strip()
                    prov = event.get('provincia', '').strip()
                    
                    # Costruzione Location: "Comune (Provincia)"
                    location = f"{comune} ({prov})" if prov else comune
                    if not location: location = "Località n.d."

                    link = f"https://www.myfitri.it/calendario/evento/{event_id}"

                    # Estrazione Sottogare dall'array 'Gare'
                    gare_list = event.get('Gare', [])
                    if gare_list:
                        for g in gare_list:
                            # Data specifica della gara (es. Sabato o Domenica)
                            raw_data_gara = g.get('data_gara', event.get('dataInizio', '2026-01-01'))
                            std_date = "-".join(raw_data_gara.split('-')[::-1]) if '-' in raw_data_gara else "01-01-2026"
                            
                            # Titolo della specialità (es. "Duathlon Sprint Age Group")
                            spec = g.get('denominazione', '').strip()
                            if not spec:
                                # Fallback su tipo + specializzazione
                                t = g.get('tipoevento', '')
                                s = g.get('specializzazione', '')
                                spec = f"{t} {s}".strip() or "Gara"

                            all_final_races.append(f"{event_title} | {std_date} | {location} | {region} | {spec} | {link}")
                    else:
                        # Fallback se non ci sono sottogare nell'array
                        raw_start = event.get('dataInizio', '2026-01-01')
                        std_date = "-".join(raw_start.split('-')[::-1]) if '-' in raw_start else "01-01-2026"
                        all_final_races.append(f"{event_title} | {std_date} | {location} | {region} | Gara | {link}")

            except Exception as e:
                print(f"   ⚠️ Errore: {e}")

        # SALVATAGGIO FINALE
        unique_output = sorted(list(set(all_final_races)))
        if len(unique_output) > 20:
            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                for r in unique_output:
                    f.write(r + "\n")
            print(f"\n✨ SUCCESS: {len(unique_output)} gare/specialità salvate correttamente!")
        else:
            print(f"\n❌ Errore critico: Dati non estratti correttamente.")

        browser.close()

if __name__ == "__main__":
    run()
