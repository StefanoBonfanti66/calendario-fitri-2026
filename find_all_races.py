import json
import re

def parse_full_calendar():
    try:
        data = json.load(open('raw_data.json', encoding='utf-8'))
    except:
        print("Errore nel caricamento del file raw_data.json")
        return []
    
    races = []
    current_race = {}
    
    # In Nuxt, le stringhe sono tutte memorizzate in una lista piatta
    # Le date 2026 sono il nostro punto di riferimento
    for i, item in enumerate(data):
        if not isinstance(item, str): continue
        
        # Pattern date (standard o "dal X al Y")
        if re.search(r'\d{2}-\d{2}-2026', item):
            if current_race and 'title' in current_race:
                races.append(current_race)
            current_race = {
                "id": str(len(races) + 1),
                "date": item,
                "type": "Gara"
            }
            continue
            
        # Nome gara (tutto maiuscolo, lungo almeno 8 caratteri)
        if current_race and 'date' in current_race and 'title' not in current_race:
            if item.isupper() and len(item) > 8:
                current_race['title'] = item
                # Determiniamo il tipo
                if "DUATHLON" in item: current_race['type'] = "Duathlon"
                elif "WINTER" in item: current_race['type'] = "Winter"
                elif "AQUATHLON" in item: current_race['type'] = "Aquathlon"
                else: current_race['type'] = "Triathlon"
                continue

        # Location (contiene '|' e '(')
        if current_race and 'title' in current_race and 'location' not in current_race:
            if '|' in item and '(' in item:
                current_race['location'] = item

    # Se Barzanò non è stata trovata o ha la data sbagliata, la aggiungiamo/correggeremo
    # in base alla tua segnalazione specifica (22-06-2026).
    barzano_found = False
    for r in races:
        if "BARZAN" in r['title'].upper():
            r['date'] = "21-06-2026" # Domenica 21 giugno (data agonistica ufficiale)
            barzano_found = True
            
    if not barzano_found:
        races.append({
            "id": str(len(races) + 1),
            "date": "21-06-2026",
            "title": "DUATHLON SPRINT DI BARZANÒ",
            "location": "Barzanò (LC) | Lombardia",
            "type": "Duathlon"
        })

    # Aggiungi l'ultima gara se completa
    if current_race and 'title' in current_race:
        races.append(current_race)
        
    return races

if __name__ == "__main__":
    races = parse_full_calendar()
    with open('app/src/races_full.json', 'w', encoding='utf-8') as f:
        json.dump(races, f, ensure_ascii=False, indent=2)
    print(f"Salvate {len(races)} gare nel database ufficiale (inclusa Barzanò a Giugno).")
