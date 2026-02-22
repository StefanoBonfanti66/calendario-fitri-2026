import time
import sys
import re
from playwright.sync_api import sync_playwright

NL = chr(10)

def run():
    print("🚀 MTT_SCRAPER_V18_GENERIC_MONTH_UNLOCK")
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
            page = context.new_page()
            
            print("🔗 Connecting to MyFITri...")
            page.goto("https://www.myfitri.it/calendario", wait_until="networkidle", timeout=90000)
            time.sleep(10)

            # SBLOCCO FILTRO MESE GENERICO (Regex per tutti i mesi)
            print("🧹 Looking for any active month filter chip...")
            try:
                # Regex che include tutti i mesi in italiano
                months_regex = re.compile(r"Gennaio|Febbraio|Marzo|Aprile|Maggio|Giugno|Luglio|Agosto|Settembre|Ottobre|Novembre|Dicembre", re.IGNORECASE)
                
                # Applichiamo la tua logica registrata: cerca lo span col mese e clicca l'icona 'i'
                # Lo facciamo per tutti i match trovati
                month_filters = page.locator("span").filter(has_text=months_regex)
                count = month_filters.count()
                
                if count > 0:
                    print(f"🎯 Found {count} month filter(s). Clicking 'X' icons...")
                    for i in range(count):
                        try:
                            # Clicca sull'iconcina 'i' (la X di chiusura) dentro lo span o il suo parent
                            month_filters.nth(i).locator("i").click(timeout=5000)
                            print(f"✅ Filter {i+1} closed.")
                        except:
                            # Se non trova 'i', prova a cliccare lo span stesso (spesso sblocca comunque)
                            month_filters.nth(i).click(timeout=2000)
                else:
                    print("⚠️ No month filter chip visible.")

                # Forza comunque il tab TUTTI per sicurezza
                tutti_tab = page.locator("div.v-tab").filter(has_text=re.compile(r"TUTTI", re.IGNORECASE))
                if tutti_tab.count() > 0:
                    tutti_tab.first.click()
                    print("✅ Forced 'TUTTI' tab click.")

            except Exception as e:
                print(f"❌ Error during unlocking: {e}")

            print("⏳ Waiting for season to load (15s)...")
            time.sleep(15)

            # SCROLLING
            print("🖱️ Deep scrolling...")
            for i in range(25):
                page.mouse.wheel(0, 4000)
                time.sleep(1)

            # ESTRAZIONE
            print("📊 Extracting data...")
            res = page.evaluate("() => Array.from(document.querySelectorAll('.v-card')).map(c => c.innerText)")
            output = []
            for item in res:
                if "2026" in item:
                    lines = [l.strip() for l in item.splitlines() if l.strip()]
                    if len(lines) >= 3:
                        output.append(lines[0] + " | " + lines[1] + " | " + lines[-1])
            
            output = list(dict.fromkeys(output))

            if len(output) > 10:
                filename = "gare_fitri_2026.txt"
                with open(filename, "w", encoding="utf-8") as f:
                    for line in output:
                        f.write(line + NL)
                print(f"✨ SUCCESS: {len(output)} races saved!")
            else:
                print(f"☹️ Extraction failed or only {len(output)} races found.")

            browser.close()
        except Exception as e:
            print(f"FATAL ERROR: {e}")
            sys.exit(0)

if __name__ == "__main__":
    run()
