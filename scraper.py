import requests
from bs4 import BeautifulSoup
import json
import re

def scrape_fitri_calendar():
    url = "https://www.myfitri.it/calendario"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch data: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Based on the snippet, let's look for the structure.
    # The snippet showed: "31-01-2026 1° COPPA S. AGATA DUATHLON SUPER SPRINT Catania (Catania) | Sicilia"
    # We need to find the container for these items.
    
    races = []
    
    # Usually, these lists are in <div> or <li> elements. 
    # Let's try to find elements that contain a date pattern.
    date_pattern = re.compile(r'\d{2}-\d{2}-\d{4}')
    
    # We'll search for all text and see where the pattern appears.
    # However, a better way is to find the specific container.
    # Let's look for common calendar class names or IDs.
    
    # Since I don't have the full HTML, I'll use a more generic search first
    # or look for the structure in the provided snippet.
    
    # The snippet suggests the items might be inside a specific div or just siblings.
    # I'll try to find all <div> or <span> that match the date format.
    
    # Re-analyzing the snippet:
    # < 31-01-2026 1° COPPA S. AGATA DUATHLON SUPER SPRINT Catania (Catania) | Sicilia
    
    # I'll search for elements containing the text and try to extract siblings.
    # But let's assume a list structure like .calendario-item or similar.
    # Actually, I'll just look for elements that have the date text directly.
    
    items = soup.find_all(string=date_pattern)
    for item in items:
        parent = item.parent
        # Try to find the full row. Usually it's a div or li.
        # This is a bit heuristic without the exact CSS selectors.
        row_text = parent.get_text(strip=True, separator=' ')
        
        # Example: "31-01-2026 1° COPPA S. AGATA DUATHLON SUPER SPRINT Catania (Catania) | Sicilia"
        # Match groups: Date, Title, Location
        match = re.search(r'(\d{2}-\d{2}-\d{4}(?: al \d{2}-\d{2}-\d{4})?)\s+(.*?)\s+([^|]+?\(.*?\)\s*\|\s*.*)', row_text)
        
        if match:
            date_str = match.group(1)
            title = match.group(2)
            location = match.group(3)
            
            # Determine type
            race_type = "Triathlon"
            if "DUATHLON" in title.upper():
                race_type = "Duathlon"
            elif "AQUATHLON" in title.upper():
                race_type = "Aquathlon"
            elif "WINTER TRIATHLON" in title.upper():
                race_type = "Winter Triathlon"

            races.append({
                "date": date_str,
                "title": title,
                "location": location,
                "type": race_type
            })

    return races

if __name__ == "__main__":
    data = scrape_fitri_calendar()
    with open('races.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Scraped {len(data)} races.")
