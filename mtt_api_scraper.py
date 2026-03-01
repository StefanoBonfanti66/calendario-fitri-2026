import requests
import json
import calendar
import time

OUTPUT_FILE = "gare_2026.txt"

def run_api_scraper():
    print("🚀 SCRAPER API V4.3: CORRECT ID MAPPING (id_evento)")
    all_final_races = []
    
    url = "https://cms.myfitri.it/api/eventi"
    
    # Range trimestrali per coprire tutto il 2026
    ranges = [
        ("2026-01-01", "2026-03-31"),
        ("2026-04-01", "2026-06-30"),
        ("2026-07-01", "2026-09-30"),
        ("2026-10-01", "2026-12-31")
    ]
    
    for start_date, end_date in ranges:
        print(f"📅 Recupero periodo {start_date} -> {end_date}...")
        
        params = {
            "populate": "*",
            "filters[$and][0][dataInizio][$gte]": start_date,
            "filters[$and][1][dataInizio][$lte]": end_date,
            "sort[0]": "dataInizio",
            "pagination[limit]": "500"
        }

        try:
            response = requests.get(url, params=params, timeout=30)
            if response.status_code != 200:
                print(f"   ⚠️ Errore API: {response.status_code}")
                continue

            res_json = response.json()
            events = res_json.get('data', [])

            for event in events:
                # Strapi v4 può avere i dati in 'attributes' o direttamente nell'oggetto
                item = event.get('attributes') if 'attributes' in event else event
                
                # LA CORREZIONE CRUCIALE: Usiamo 'id_evento' (4 cifre) invece di 'id' (6 cifre)
                # 'id_evento' è l'ID pubblico usato per i link ufficiali
                event_id = item.get('id_evento') or event.get('id', '')
                
                event_title = item.get('denominazione', 'Ignoto').strip()
                region = item.get('regione', 'Italia').strip()
                comune = item.get('localita', '').strip()
                prov = item.get('provincia', '').strip()
                location = f"{comune} ({prov})" if prov else comune
                if not location: location = "Località n.d."

                # Costruzione link ufficiale funzionante
                link = f"https://www.myfitri.it/evento/{event_id}"       

                gare_list = item.get('Gare', [])
                
                if not gare_list:
                    raw_start = item.get('dataInizio', '2026-01-01')
                    std_date = "-".join(raw_start.split('-')[::-1]) if '-' in raw_start else "01-01-2026"
                    all_final_races.append(f"{event_title} | {std_date} | {location} | {region} | Gara | {link}")
                else:
                    for g in gare_list:
                        raw_data_gara = g.get('data_gara') or item.get('dataInizio', '2026-01-01')
                        std_date = "-".join(raw_data_gara.split('-')[::-1]) if '-' in raw_data_gara else "01-01-2026"
                        
                        spec = g.get('denominazione', '').strip()
                        if not spec:
                            t = g.get('tipoevento', '')
                            s = g.get('specializzazione', '')
                            spec = f"{t} {s}".strip() or "Gara"

                        all_final_races.append(f"{event_title} | {std_date} | {location} | {region} | {spec} | {link}")

        except Exception as e:
            print(f"   ⚠️ Errore durante il recupero: {e}")
        
        time.sleep(0.3)

    # SALVATAGGIO
    unique_output = sorted(list(set(all_final_races)))
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for r in unique_output:
            f.write(r + "\n")
    
    print(f"\n✨ FINISHED: {len(unique_output)} gare salvate con link ufficiali id_evento.")

if __name__ == "__main__":
    run_api_scraper()
