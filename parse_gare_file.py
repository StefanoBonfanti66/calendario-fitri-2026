import json
import re
import os

def parse_gare_file(file_path):
    new_races = []
    
    month_map = {
        'gen': '01', 'feb': '02', 'mar': '03', 'apr': '04', 'mag': '05', 'giu': '06',
        'lug': '07', 'ago': '08', 'set': '09', 'ott': '10', 'nov': '11', 'dic': '12'
    }

    if not os.path.exists(file_path):
        print(f"Avviso: Il file '{file_path}' non esiste.")
        return []

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    main_info_pattern = re.compile(r'^(?:dal )?(\d{2}-\d{2}-2026)(?: al \d{2}-\d{2}-2026)?\s+(.*)', re.IGNORECASE)
    sub_event_info_pattern = re.compile(r'^(\d{1,2})-(\S{3})\s+(.*?)$', re.IGNORECASE)

    for line in lines:
        stripped_line = line.strip()
        if not stripped_line: continue
            
        parts = stripped_line.split(' | ') 
        if len(parts) < 3: continue
            
        try:
            # Gestione dinamica dei formati (3 o 4 parti)
            if len(parts) >= 4:
                event_title = parts[0].strip()
                main_date_loc_raw = parts[1].strip()
                region = parts[2].strip()
                sub_event_part_raw = parts[3].strip()
            else:
                # Fallback per il vecchio formato a 3 parti
                event_title = parts[0].strip()
                main_date_loc_raw = parts[1].strip()
                region = "Italia"
                sub_event_part_raw = parts[2].strip()

            main_match = main_info_pattern.match(main_date_loc_raw)
            city = main_match.group(2).strip() if main_match else main_date_loc_raw

            sub_match = sub_event_info_pattern.match(sub_event_part_raw)
            if not sub_match: continue
                
            sub_day = sub_match.group(1).zfill(2)
            sub_month_abbr = sub_match.group(2).lower()
            full_sub_title = sub_match.group(3).strip()

            sub_month = month_map.get(sub_month_abbr, '00')
            full_sub_event_date = f"{sub_day}-{sub_month}-2026"

            rank = ""
            for r in ["Silver", "Gold", "Bronze", "Internazionale"]:
                if r in full_sub_title:
                    rank = r
                    full_sub_title = full_sub_title.replace(r, "").strip()
                    break

            category = ""
            for c in ["Giovanile", "Paratriathlon", "Kids", "Youth"]:
                if c in full_sub_title:
                    category = c
                    full_sub_title = full_sub_title.replace(c, "").strip()
                    break

            distance = ""
            for d in ["Super Sprint", "Sprint", "Classico", "Olimpico", "Medio", "Lungo", "Staffetta", "Cross", "Mtb", "Minitriathlon", "Youth", "Kids"]:
                if d.lower() in full_sub_title.lower():
                    distance = d
                    break

            race_type = "Triathlon"
            if "DUATHLON" in full_sub_title.upper(): race_type = "Duathlon"
            elif "WINTER" in full_sub_title.upper(): race_type = "Winter"
            elif "AQUATHLON" in full_sub_title.upper(): race_type = "Aquathlon"
            elif "CROSS" in full_sub_title.upper(): race_type = "Cross"

            new_races.append({
                "date": full_sub_event_date,
                "title": full_sub_title,
                "event": event_title,
                "location": city,
                "region": region,
                "type": race_type,
                "distance": distance,
                "rank": rank,
                "category": category
            })
        except:
            continue
            
    return new_races

def merge_and_save(new_races, output_json):
    # 1. Carica le gare esistenti
    existing_races = []
    if os.path.exists(output_json):
        try:
            with open(output_json, 'r', encoding='utf-8') as f:
                existing_races = json.load(f)
        except:
            existing_races = []

    # 2. Crea un set di chiavi uniche per evitare duplicati (Giorno + Titolo + Località)
    def get_key(r): return f"{r['date']}-{r['title']}-{r['location']}"
    
    unique_races = {get_key(r): r for r in existing_races}
    
    # 3. Aggiungi le nuove gare (se la chiave esiste già, la nuova sovrascrive la vecchia - utile per aggiornamenti)
    for nr in new_races:
        unique_races[get_key(nr)] = nr

    # 4. Converti di nuovo in lista e ordina per data
    final_list = list(unique_races.values())
    final_list.sort(key=lambda x: x['date'].split('-')[::-1])

    # 5. Riassegna gli ID
    for i, r in enumerate(final_list):
        r['id'] = str(i + 1)

    # 6. Salva
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(final_list, f, ensure_ascii=False, indent=2)
    
    return len(final_list)

if __name__ == "__main__":
    new_data = parse_gare_file('gare_2026.txt')
    total = merge_and_save(new_data, 'app/src/races_full.json')
    print(f"✅ Sincronizzazione completata! Database aggiornato: {total} gare totali.")
