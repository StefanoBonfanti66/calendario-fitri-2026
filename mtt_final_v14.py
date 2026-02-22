import time
import sys
from playwright.sync_api import sync_playwright

# Definisco il carattere 'a capo' tramite codice ASCII per evitare errori di sintassi
NL = chr(10)

def run():
    print("STARTING_V14_NO_ESCAPE_CHARS")
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("https://www.myfitri.it/calendario", wait_until="networkidle", timeout=90000)
            time.sleep(10)
            
            # Sblocco filtri
            page.evaluate("() => { document.querySelectorAll('.v-chip__close').forEach(el => el.click()); const t = Array.from(document.querySelectorAll('.v-tab')).find(x => x.innerText.includes('TUTTI')); if (t) t.click(); }")
            time.sleep(10)
            
            # Scrolling
            for i in range(20):
                page.mouse.wheel(0, 3000)
                time.sleep(1)
            
            # Estrazione
            res = page.evaluate("() => Array.from(document.querySelectorAll('.v-card')).map(c => c.innerText)")
            
            output = []
            for item in res:
                if "2026" in item:
                    # Uso splitlines() che non richiede caratteri speciali
                    lines = [l.strip() for l in item.splitlines() if l.strip()]
                    if len(lines) >= 3:
                        output.append(lines[0] + " | " + lines[1] + " | " + lines[-1])
            
            if output:
                with open("gare_fitri_2026.txt", "w", encoding="utf-8") as f:
                    for line in output:
                        # Scrittura sicura usando la variabile definita all'inizio
                        f.write(line + NL)
                print("SUCCESS_COUNT_" + str(len(output)))
            
            browser.close()
        except Exception as e:
            print("ERROR_" + str(e))
            sys.exit(0)

if __name__ == "__main__":
    run()
