import requests
import json

def run():
    print("MTT_API_SCRAPER_STARTING_V7")
    year = "2026"
    
    # URL dell'API interna di MyFITri che restituisce tutti i dati Nuxt
    # MyFITri usa spesso un sistema di payload JSON. Proviamo l'endpoint diretto.
    url = "https://www.myfitri.it/calendario"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8"
    }

    try:
        print("Scaricamento dati sorgente...")
        r = requests.get(url, headers=headers, timeout=30)
        
        # Cerchiamo i dati Nuxt nel codice HTML (sono più completi dei 6 visibili)
        # Il pattern è: "data":[...] o simile
        content = r.text
        
        # Estraiamo tutte le date del 2026 per trovare i blocchi
        dates = re.findall(r'\d{2}-\d{2}-2026', content)
        print(f"Date 2026 trovate nel codice: {len(dates)}")

        # Strategia: usiamo la tecnica di estrazione stringhe dal payload Nuxt
        # Cerchiamo la lista piatta di stringhe nel tag __NUXT_DATA__
        import re
        script_match = re.search(r'<script id="__NUXT_DATA__".*?>(.*?)</script>', content, re.DOTALL)
        
        output = []
        if script_match:
            data = json.loads(script_match.group(1))
            print(f"Payload Nuxt trovato: {len(data)} elementi.")
            
            current_event = ""
            current_loc = ""
            
            for item in data:
                if not isinstance(item, str): continue
                
                # Riconoscimento Titolo (Tutto maiuscolo, lungo)
                if item.isupper() and len(item) > 12 and not any(x in item for x in ["GEN", "FEB", "MAR", "APR", "MAG", "GIU", "LUG", "AGO", "SET", "OTT", "NOV", "DIC"]):
                    current_event = item
                    continue
                
                # Riconoscimento Data/Località
                if "2026" in item and len(item) > 15 and "|" in item:
                    current_loc = item
                    continue
                
                # Riconoscimento Specialità
                if any(x in item.upper() for x in ["TRIATHLON", "DUATHLON", "AQUATHLON", "CROSS"]):
                    if current_event and current_loc:
                        output.append(f"{current_event} | {current_loc} | {item}")

        output = list(dict.fromkeys(output))
        
        if output:
            with open("gare_fitri_2026.txt", "w", encoding="utf-8") as f:
                for line in output:
                    f.write(line + "\n")
            print(f"DONE_API_FOUND_{len(output)}")
        else:
            print("FALLBACK_ESTRAZIONE_TESTUALE")
            # Ultima spiaggia: regex sul testo totale
            lines = re.findall(r'([A-Z\s]{10,}.*?\d{2}-\d{2}-2026.*?\|.*?\|.*?[A-Za-z\s]{5,})', content)
            with open("gare_fitri_2026.txt", "w", encoding="utf-8") as f:
                f.write("\n".join(lines))

    except Exception as e:
        print(f"ERROR: {str(e)}")

if __name__ == "__main__":
    run()
