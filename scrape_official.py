import requests
from bs4 import BeautifulSoup
import json
import re

def scrape_official_fitri():
    url = "https://www.myfitri.it/calendario"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    # Il sito MyFITri usa Nuxt e i dati sono in questo script
    script = soup.find('script', id='__NUXT_DATA__')
    if not script:
        return []

    # Carichiamo i dati grezzi
    raw_data = json.loads(script.string)
    
    races = []
    # Strategia: cerchiamo le stringhe che corrispondono ai pattern delle gare
    # Il JSON di Nuxt è una lista piatta dove gli oggetti sono ricostruiti tramite indici.
    # Ma le stringhe (Date, Nomi, Location) sono tutte lì.
    
    current_race = {}
    
    for item in raw_data:
        if not isinstance(item, str):
            continue
            
        # 1. Cerca la data (es: 31-01-2026)
        if re.match(r'^\d{2}-\d{2}-2026$', item) or "dal " in item:
            if current_race and 'title' in current_race:
                races.append(current_race)
            current_race = {
                "id": str(len(races) + 1),
                "date": item,
                "type": "Gara"
            }
            continue
            
        # 2. Cerca il titolo (tutto maiuscolo, lungo almeno 10 caratteri)
        if current_race and 'date' in current_race and 'title' not in current_race:
            if item.isupper() and len(item) > 8:
                current_race['title'] = item
                # Determiniamo il tipo
                if "DUATHLON" in item: current_race['type'] = "Duathlon"
                elif "WINTER" in item: current_race['type'] = "Winter Triathlon"
                elif "AQUATHLON" in item: current_race['type'] = "Aquathlon"
                else: current_race['type'] = "Triathlon"
                continue

        # 3. Cerca la location (contiene '|' e '(')
        if current_race and 'title' in current_race and 'location' not in current_race:
            if '|' in item and '(' in item:
                current_race['location'] = item

    # Aggiungi l'ultima gara se completa
    if current_race and 'title' in current_race:
        races.append(current_race)
        
    return races

if __name__ == "__main__":
    official_races = scrape_official_fitri()
    if official_races:
        # Salviamo il file ufficiale
        import os
        if not os.path.exists('app/src'): os.makedirs('app/src')
        with open('app/src/races_full.json', 'w', encoding='utf-8') as f:
            json.dump(official_races, f, ensure_ascii=False, indent=2)
        print(f"Sincronizzazione completata! Caricate {len(official_races)} gare UFFICIALI dal sito FITRI.")
    else:
        print("Errore nella sincronizzazione. Riprovare tra poco.")
