import time
import sys
from playwright.sync_api import sync_playwright

def run():
    print("MTT_SCRAPER_STARTING")
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("https://www.myfitri.it/calendario", wait_until="networkidle")
            time.sleep(10)
            
            # Clicca TUTTI
            page.evaluate("Array.from(document.querySelectorAll('*')).find(e => e.innerText==='TUTTI')?.click()")
            time.sleep(5)
            
            # Estrazione dati (solo testo semplice)
            data = page.evaluate("Array.from(document.querySelectorAll('.v-card')).map(c => c.innerText)")
            
            output = []
            for item in data:
                if "2026" in item:
                    lines = [l.strip() for l in item.split("\n") if l.strip()]
                    if len(lines) >= 3:
                        output.append(f"{lines[0]} | {lines[1]} | {lines[-1]}")
            
            if output:
                with open("gare_fitri_2026.txt", "w", encoding="utf-8") as f:
                    f.write("
".join(output))
                print(f"DONE_FOUND_{len(output)}")
            
            browser.close()
        except Exception as e:
            print(f"ERROR_{str(e)}")

if __name__ == "__main__":
    run()
