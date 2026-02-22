import json
import re
import os

def parse_gare_file(file_path):
    new_races = []
    month_map = {'gen': '01', 'feb': '02', 'mar': '03', 'apr': '04', 'mag': '05', 'giu': '06', 'lug': '07', 'ago': '08', 'set': '09', 'ott': '10', 'nov': '11', 'dic': '12'}

    if not os.path.exists(file_path): return []
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    main_info_pattern = re.compile(r'^(?:dal )?(\d{2}-\d{2}-2026)(?: al \d{2}-\d{2}-2026)?\s+(.*)', re.IGNORECASE)
    sub_event_info_pattern = re.compile(r'^(\d{1,2})-(\S{3})\s+(.*?)$', re.IGNORECASE)

    for line in lines:
        parts = line.strip().split(' | ') 
        if len(parts) < 3: continue
            
        try:
            event_title = parts[0].strip()
            main_date_loc_raw = parts[1].strip()
            sub_event_part_raw = parts[2].strip()
            link = parts[3].strip() if len(parts) > 3 else ""

            main_match = main_info_pattern.match(main_date_loc_raw)
            city = main_match.group(2).strip() if main_match else main_date_loc_raw
            region = "Italia" 

            sub_match = sub_event_info_pattern.match(sub_event_part_raw)
            if not sub_match: continue
            
            day, month_abbr, full_sub_title = sub_match.group(1).zfill(2), sub_match.group(2).lower(), sub_match.group(3).strip()
            date = f"{day}-{month_map.get(month_abbr, '00')}-2026"

            # Logica sport (MOLTO RIGOROSA)
            search_text_upper = (full_sub_title + " " + event_title).upper()
            if "DUATHLON" in search_text_upper: race_type = "Duathlon"
            elif "WINTER" in search_text_upper: race_type = "Winter"
            elif "AQUATHLON" in search_text_upper: race_type = "Aquathlon"
            elif "CROSS" in search_text_upper: race_type = "Cross"
            else: race_type = "Triathlon"

            rank = next((r for r in ["Silver", "Gold", "Bronze", "Internazionale"] if r in full_sub_title), "")
            
            category = ""
            if "paratriathlon" in search_text_upper.lower(): category = "Paratriathlon"
            elif "kids" in search_text_upper.lower(): category = "Kids"
            elif "youth" in search_text_upper.lower(): category = "Youth"
            elif "giovanile" in search_text_upper.lower(): category = "Giovanile"

            distance = next((d for d in ["Super Sprint", "Sprint", "Classico", "Olimpico", "Medio", "Lungo", "Staffetta", "Cross"] if d.lower() in full_sub_title.lower()), "")

            new_races.append({
                "date": date, "title": full_sub_title, "event": event_title,
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

    # In questa bonifica, resettiamo il database per applicare le nuove regole a tutto
    unique_races = {}
    
    # Ri-processiamo tutto per assicurarci che i tipi siano corretti ovunque
    # Nota: In una sessione reale non lo faremmo sempre, ma qui serve per la bonifica
    for nr in new_races:
        key = f"{nr['date']}-{nr['title']}-{nr['location']}"
        unique_races[key] = nr

    final_list = sorted(list(unique_races.values()), key=lambda x: x['date'].split('-')[::-1])
    for i, r in enumerate(final_list): r['id'] = str(i + 1)

    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(final_list, f, ensure_ascii=False, indent=2)
    return len(final_list)

if __name__ == "__main__":
    new_data = parse_gare_file('gare_2026.txt')
    total = merge_and_save(new_data, 'app/src/races_full.json')
    print(f"✅ Database BONIFICATO: {total} gare con tipi sport corretti.")
