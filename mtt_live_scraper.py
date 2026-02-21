import time
import sys
from playwright.sync_api import sync_playwright

def run():
    print("MTT_SCRAPER_STARTING_V6")
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("https://www.myfitri.it/calendario", wait_until="networkidle")
            time.sleep(10)
            
            # Clicca TUTTI via JS
            page.evaluate("Array.from(document.querySelectorAll('*')).find(e => e.innerText==='TUTTI')?.click()")
            time.sleep(5)
            
            # Estrazione dati
            data = page.evaluate("Array.from(document.querySelectorAll('.v-card')).map(c => c.innerText)")
            
            output = []
            for item in data:
                if "2026" in item:
                    # Usiamo un metodo di split che non richiede \n letterale
                    lines = [l.strip() for l in item.splitlines() if l.strip()]
                    if len(lines) >= 3:
                        output.append(lines[0] + " | " + lines[1] + " | " + lines[-1])
            
            if output:
                filename = "gare_fitri_2026.txt"
                with open(filename, "w", encoding="utf-8") as f:
                    for line in output:
                        f.write(line)
                        f.write("\n")
                print("SUCCESS_FOUND_RACES")
            
            browser.close()
        except Exception as e:
            print("ERROR_OCCURRED")
            print(str(e))

if __name__ == "__main__":
    run()
