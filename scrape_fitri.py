import json
import re
import requests
from bs4 import BeautifulSoup

def scrape_fitri_calendar():
    year = "2026"
    url = "https://www.myfitri.it/calendario"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    print(f"Richiesta dati a {url}...")
    try:
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code != 200:
            print(f"Errore HTTP: {response.status_code}")
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # MyFITri usa Nuxt e i dati sono dentro uno script con ID __NUXT_DATA__
        script = soup.find('script', id='__NUXT_DATA__')
        if not script:
            print("Dati __NUXT_DATA__ non trovati. Fallback su estrazione testuale...")
            # Fallback estrazione testo grezzo
            all_text = soup.get_text(separator='|')
            races = re.findall(r'([^|]+2026[^|]+)', all_text)
            with open(f"gare_fitri_{year}.txt", "w", encoding="utf-8") as f:
                f.write("\n".join([r.strip() for r in races if len(r) > 20]))
            return

        # I dati sono in una lista piatta di stringhe e numeri
        raw_data = json.loads(script.string)
        print("Dati estratti. Analisi in corso...")

        output_lines = []
        current_event = "N/A"
        current_loc = "N/A"

        # Cerchiamo le stringhe che corrispondono ai pattern delle gare
        for item in raw_data:
            if not isinstance(item, str): continue
            
            # Pattern Titolo Evento (Tutto maiuscolo, lungo)
            if item.isupper() and len(item) > 10 and not any(x in item for x in ["GEN", "FEB", "MAR", "APR", "MAG", "GIU", "LUG", "AGO", "SET", "OTT", "NOV", "DIC"]):
                current_event = item
                continue
            
            # Pattern Data e Località (es: 31-01-2026...)
            if re.search(r'\d{2}-\d{2}-2026', item):
                current_loc = item
                continue
            
            # Pattern Specialità
            if any(x in item.upper() for x in ["TRIATHLON", "DUATHLON", "AQUATHLON", "CROSS"]):
                if current_event != "N/A":
                    line = f"{current_event} | {current_loc} | {item}"
                    output_lines.append(line)

        # Pulizia e salvataggio
        output_lines = list(dict.fromkeys(output_lines))
        if output_lines:
            with open(f"gare_fitri_{year}.txt", "w", encoding="utf-8") as f:
                f.write("\n".join(output_lines))
            print(f"Completato! Trovate {len(output_lines)} gare.")
        else:
            print("Nessuna gara individuata nel JSON.")

    except Exception as e:
        print(f"Errore: {e}")

if __name__ == "__main__":
    scrape_fitri_calendar()
