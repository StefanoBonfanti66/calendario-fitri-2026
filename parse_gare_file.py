import json
import re

def parse_gare_file(file_path):
    races = []
    race_id_counter = 1
    
    month_map = {
        'gen': '01', 'feb': '02', 'mar': '03', 'apr': '04', 'mag': '05', 'giu': '06',
        'lug': '07', 'ago': '08', 'set': '09', 'ott': '10', 'nov': '11', 'dic': '12'
    }

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Errore: Il file '{file_path}' non trovato.")
        return []
    
    # Il nuovo formato ha 4 parti separate da " | ":
    # EVENTO | DATA_LOC_GENERICA | REGIONE | DATA_SPECIFICA TITOLO
    
    main_info_pattern = re.compile(r'^(?:dal )?(\d{2}-\d{2}-2026)(?: al \d{2}-\d{2}-2026)?\s+(.*)', re.IGNORECASE)
    sub_event_info_pattern = re.compile(r'^(\d{1,2})-(\S{3})\s+(.*?)$', re.IGNORECASE)

    for line in lines:
        stripped_line = line.strip()
        if not stripped_line: continue
            
        parts = stripped_line.split(' | ') 
        if len(parts) < 4: 
            # Invece di stampare solo, saltiamo silenziosamente per non far fallire l'action
            continue
            
        try:
            event_title = parts[0].strip()
            main_date_loc_raw = parts[1].strip()
            region = parts[2].strip()
            sub_event_part_raw = parts[3].strip()

            # Estraiamo la città dalla parte principale (es: "10-01-2026 Predazzo (Trento)")
            main_match = main_info_pattern.match(main_date_loc_raw)
            city = ""
            if main_match:
                city = main_match.group(2).strip()

            # Parsifica la parte del sotto-evento (es: "11-gen WinterTriathlon Sprint")
            sub_match = sub_event_info_pattern.match(sub_event_part_raw)
            if not sub_match: continue
                
            sub_day = sub_match.group(1).zfill(2)
            sub_month_abbr = sub_match.group(2).lower()
            full_sub_title = sub_match.group(3).strip()

            sub_month = month_map.get(sub_month_abbr, '00')
            full_sub_event_date = f"{sub_day}-{sub_month}-2026"

            # Estrazione Rank
            rank = ""
            for r in ["Silver", "Gold", "Bronze", "Internazionale"]:
                if r in full_sub_title:
                    rank = r
                    full_sub_title = full_sub_title.replace(r, "").strip()
                    break

            # Estrazione Categoria
            category = ""
            for c in ["Giovanile", "Paratriathlon", "Kids", "Youth"]:
                if c in full_sub_title:
                    category = c
                    full_sub_title = full_sub_title.replace(c, "").strip()
                    break

            # Estrazione Distanza
            distance = ""
            for d in ["Super Sprint", "Sprint", "Classico", "Olimpico", "Medio", "Lungo", "Staffetta", "Cross", "Mtb", "Minitriathlon", "Youth", "Kids"]:
                if d.lower() in full_sub_title.lower():
                    distance = d
                    break

            # Tipo Gara
            race_type = "Triathlon"
            if "DUATHLON" in full_sub_title.upper(): race_type = "Duathlon"
            elif "WINTER" in full_sub_title.upper(): race_type = "Winter"
            elif "AQUATHLON" in full_sub_title.upper(): race_type = "Aquathlon"
            elif "CROSS" in full_sub_title.upper(): race_type = "Cross"

            races.append({
                "id": str(race_id_counter),
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
            race_id_counter += 1
        except Exception as e:
            print(f"Errore riga: {e}")
            continue
            
    return races

if __name__ == "__main__":
    parsed_races = parse_gare_file('gare_2026.txt')
    if parsed_races:
        # Ordiniamo per data
        parsed_races.sort(key=lambda x: x['date'].split('-')[::-1])
        # Riassegniamo gli ID
        for i, r in enumerate(parsed_races): r['id'] = str(i + 1)
        
        with open('app/src/races_full.json', 'w', encoding='utf-8') as f:
            json.dump(parsed_races, f, ensure_ascii=False, indent=2)
        print(f"Aggiornate {len(parsed_races)} gare con titoli evento completi.")
