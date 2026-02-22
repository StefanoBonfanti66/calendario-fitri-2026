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
            # Formato: EVENTO | DATA LOC | SPECIALITÀ | [LINK]
            event_title = parts[0].strip()
            main_date_loc_raw = parts[1].strip()
            sub_event_part_raw = parts[2].strip()
            link = parts[3].strip() if len(parts) > 3 else ""

            main_match = main_info_pattern.match(main_date_loc_raw)
            city = main_match.group(2).strip() if main_match else main_date_loc_raw
            region = "Italia" # Default

            sub_match = sub_event_info_pattern.match(sub_event_part_raw)
            if not sub_match: continue
            
            day, month_abbr, full_sub_title = sub_match.group(1).zfill(2), sub_match.group(2).lower(), sub_match.group(3).strip()
            date = f"{day}-{month_map.get(month_abbr, '00')}-2026"

            rank = next((r for r in ["Silver", "Gold", "Bronze", "Internazionale"] if r in full_sub_title), "")
            category = next((c for c in ["Giovanile", "Paratriathlon", "Kids", "Youth"] if c in full_sub_title), "")
            distance = next((d for d in ["Super Sprint", "Sprint", "Classico", "Olimpico", "Medio", "Lungo", "Staffetta", "Cross"] if d.lower() in full_sub_title.lower()), "")

            race_type = "Triathlon"
            if "DUATHLON" in full_sub_title.upper(): race_type = "Duathlon"
            elif "WINTER" in full_sub_title.upper(): race_type = "Winter"
            elif "AQUATHLON" in full_sub_title.upper(): race_type = "Aquathlon"

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

    def get_key(r): return f"{r['date']}-{r['title']}-{r['location']}"
    unique_races = {get_key(r): r for r in existing_races}
    
    for nr in new_races:
        # Se la nuova gara ha un link e la vecchia no, aggiorniamo il link
        key = get_key(nr)
        if key in unique_races:
            if nr.get('link'): unique_races[key]['link'] = nr['link']
        else:
            unique_races[key] = nr

    final_list = sorted(list(unique_races.values()), key=lambda x: x['date'].split('-')[::-1])
    for i, r in enumerate(final_list): r['id'] = str(i + 1)

    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(final_list, f, ensure_ascii=False, indent=2)
    return len(final_list)

if __name__ == "__main__":
    new_data = parse_gare_file('gare_2026.txt')
    total = merge_and_save(new_data, 'app/src/races_full.json')
    print(f"✅ Database aggiornato: {total} gare.")
