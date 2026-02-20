from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import json
import time
import re

def scrape_full_calendar():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Inizializza il driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    url = "https://www.myfitri.it/calendario"
    
    try:
        print(f"Caricamento URL: {url}")
        driver.get(url)
        
        # Aspetta che gli elementi del calendario siano pronti
        wait = WebDriverWait(driver, 30)
        wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '2026')]")))
        print("Pagina caricata correttamente.")

        # Scorrimento per caricare tutti gli elementi dinamici
        last_height = driver.execute_script("return document.body.scrollHeight")
        for _ in range(10): # Limitiamo i tentativi di scorrimento per sicurezza
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            print("Caricamento nuovi eventi...")

        body_text = driver.find_element(By.TAG_NAME, "body").text
        lines = body_text.split('\n')
        
        races = []
        race_id = 1
        
        # Regex per date italiane
        date_regex = re.compile(r'(\d{2}-\d{2}-2026)')
        
        for i, line in enumerate(lines):
            if date_regex.search(line):
                # Tentativo di estrazione intelligente
                # Se la riga è solo la data, cerchiamo nelle righe successive
                content = line
                if len(line.strip()) < 15 and i+1 < len(lines):
                    content += " " + lines[i+1]
                    if i+2 < len(lines):
                        content += " " + lines[i+2]

                # Match del pattern completo
                match = re.search(r'((?:dal )?\d{2}-\d{2}-2026(?: al \d{2}-\d{2}-2026)?)\s+(.*?)\s+([^|]+?\(.*?\)\s*\|\s*[^\n]*)', content)
                
                if match:
                    date_val = match.group(1).strip()
                    title_val = match.group(2).strip()
                    location_val = match.group(3).strip()
                    
                    # Tipo di gara
                    t_upper = title_val.upper()
                    race_type = "Triathlon"
                    if "DUATHLON" in t_upper: race_type = "Duathlon"
                    elif "WINTER" in t_upper: race_type = "Winter Triathlon"
                    elif "AQUATHLON" in t_upper: race_type = "Aquathlon"
                    elif "CROSS" in t_upper: race_type = "Cross Triathlon"
                    
                    races.append({
                        "id": str(race_id),
                        "date": date_val,
                        "title": title_val,
                        "location": location_val,
                        "type": race_type
                    })
                    race_id += 1

        return races

    except Exception as e:
        print(f"Errore durante lo scraping: {e}")
        return []
    finally:
        driver.quit()

if __name__ == "__main__":
    results = scrape_full_calendar()
    if results:
        # Crea la cartella se non esiste
        import os
        if not os.path.exists('app/src'):
            os.makedirs('app/src')
            
        with open('app/src/races_full.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"Successo! {len(results)} gare salvate.")
    else:
        print("Non è stato possibile estrarre i dati.")
