import json
import re
import os

def parse_gare_file(file_path):
    new_races = []
    month_map = {'gen': '01', 'feb': '02', 'mar': '03', 'apr': '04', 'mag': '05', 'giu': '06', 'lug': '07', 'ago': '08', 'set': '09', 'ott': '10', 'nov': '11', 'dic': '12'}

    if not os.path.exists(file_path): return []
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Regex flessibile per la parte principale (Data + Città)
    main_info_pattern = re.compile(r'^(dal )?(\d{2}-\d{2}-2026)(.*)', re.IGNORECASE)

    for line in lines:
        parts = line.strip().split(' | ') 
        if len(parts) < 3: continue
            
        try:
            event_title = parts[0].strip()
            main_date_loc_raw = parts[1].strip()
            sub_event_part_raw = parts[2].strip()

            main_match = main_info_pattern.match(main_date_loc_raw)
            if main_match:
                date = main_match.group(2)
                city = main_match.group(3).strip()
            else:
                date = "01-01-2026"
                city = main_date_loc_raw

            region = "Italia"
            link = ""
            
            # Se abbiamo almeno 4 parti (0: Evento, 1: DataLoc, 2: Regione, 3: Specialità)
            if len(parts) >= 4:
                region = parts[2].strip()
                sub_event_part_raw = parts[3].strip()
                if len(parts) >= 5:
                    link = parts[4].strip()
            else:
                # Caso con 3 parti (0: Evento, 1: DataLoc, 2: Specialità)
                sub_event_part_raw = parts[2].strip()
                if len(parts) >= 4:
                    link = parts[3].strip()

            # Logica sport (MOLTO RIGOROSA)
            search_text_upper = (sub_event_part_raw + " " + event_title).upper()
            if "DUATHLON" in search_text_upper: race_type = "Duathlon"
            elif "WINTER" in search_text_upper: race_type = "Winter"
            elif "AQUATHLON" in search_text_upper: race_type = "Aquathlon"
            elif "CROSS" in search_text_upper: race_type = "Cross"
            else: race_type = "Triathlon"

            category = ""
            if "paratriathlon" in search_text_upper.lower(): category = "Paratriathlon"
            elif "kids" in search_text_upper.lower(): category = "Kids"
            elif "youth" in search_text_upper.lower(): category = "Youth"
            elif "giovanile" in search_text_upper.lower(): category = "Giovanile"

            distance = next((d for d in ["Super Sprint", "Sprint", "Classico", "Olimpico", "Medio", "Lungo", "Staffetta", "Cross"] if d.lower() in sub_event_part_raw.lower()), "")

            # Estrazione Rank (Gold, Silver, Bronze)
            rank = ""
            for r in ["Gold", "Silver", "Bronze"]:
                if r.lower() in sub_event_part_raw.lower():
                    rank = r
                    # Puliamo il titolo rimuovendo il rank e spazi extra/tab
                    sub_event_part_raw = re.sub(r.lower(), '', sub_event_part_raw, flags=re.IGNORECASE).strip()
                    break
            
            # Pulizia ulteriore da tabulazioni e spazi doppi nel titolo
            sub_event_part_raw = re.sub(r'\t+', ' ', sub_event_part_raw)
            sub_event_part_raw = re.sub(r' +', ' ', sub_event_part_raw).strip()

            new_races.append({
                "date": date, "title": sub_event_part_raw, "event": event_title,
                "location": city, "region": region, "type": race_type,
                "distance": distance, "rank": rank, "category": category, "link": link
            })
        except: continue
    return new_races

def merge_and_save(new_races, output_json):
    existing_races = []
    if os.path.exists(output_json):
        try:
            with open(output_json, 'r', encoding='utf-8') as f:
                existing_races = json.load(f)
        except: pass

    unique_races = {}
    # Priorità ai nuovi dati ma manteniamo i vecchi se unici
    # La chiave ora include l'evento per evitare di perdere gare diverse nello stesso giorno/luogo
    for r in existing_races:
        key = f"{r['date']}-{r['event']}-{r['title']}-{r['location']}"
        unique_races[key] = r
    
    for nr in new_races:
        key = f"{nr['date']}-{nr['event']}-{nr['title']}-{nr['location']}"
        unique_races[key] = nr

    final_list = sorted(list(unique_races.values()), key=lambda x: x['date'].split('-')[::-1])
    for i, r in enumerate(final_list): r['id'] = str(i + 1)

    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(final_list, f, ensure_ascii=False, indent=2)
    return len(final_list)

if __name__ == "__main__":
    import sys
    input_file = sys.argv[1] if len(sys.argv) > 1 else 'gare_2026.txt'
    new_data = parse_gare_file(input_file)
    total = merge_and_save(new_data, 'app/src/races_full.json')
    print(f"✅ Database AGGIORNATO ({input_file}): {total} gare.")
