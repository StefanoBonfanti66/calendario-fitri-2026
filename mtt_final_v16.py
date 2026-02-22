import time
import sys
import re
from playwright.sync_api import sync_playwright

# Carattere 'a capo' sicuro
NL = chr(10)

def run():
    print("🚀 MTT_SCRAPER_V19_VERIFIED_UNLOCK")
    with sync_playwright() as p:
        try:
            # Headless=True per l'ambiente GitHub Actions
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
            page = context.new_page()
            
            print("🔗 Connecting to MyFITri...")
            page.goto("https://www.myfitri.it/calendario", wait_until="networkidle", timeout=90000)
            time.sleep(10)

            # LOGICA DI SBLOCCO VERIFICATA
            print("🧹 Removing Active Month Filters...")
            try:
                # Regex universale per i mesi italiani
                months_regex = re.compile(r"Gennaio|Febbraio|Marzo|Aprile|Maggio|Giugno|Luglio|Agosto|Settembre|Ottobre|Novembre|Dicembre", re.IGNORECASE)
                
                # Trova i chip dei mesi e clicca sull'icona 'i' (la X di chiusura)
                month_filters = page.locator("span").filter(has_text=months_regex)
                count = month_filters.count()
                
                if count > 0:
                    for i in range(count):
                        try:
                            month_filters.nth(i).locator("i").click(timeout=5000)
                            print(f"✅ Filter {i+1} removed.")
                        except:
                            month_filters.nth(i).click(timeout=2000)
                
                # Forza il tab TUTTI
                tutti_tab = page.locator("div.v-tab").filter(has_text=re.compile(r"TUTTI", re.IGNORECASE))
                if tutti_tab.count() > 0:
                    tutti_tab.first.click()
                    print("✅ Tab TUTTI selected.")

            except Exception as e:
                print(f"⚠️ Unlock warning: {e}")

            print("⏳ Waiting for season refresh...")
            time.sleep(15)

            # SCROLLING
            print("🖱️ Deep scrolling for full data extraction...")
            for i in range(25):
                page.mouse.wheel(0, 4000)
                time.sleep(1)

            # ESTRAZIONE DATI
            print("📊 Extracting races...")
            res = page.evaluate("() => Array.from(document.querySelectorAll('.v-card')).map(c => c.innerText)")
            output = []
            for item in res:
                if "2026" in item:
                    # splitlines() evita problemi di caratteri speciali \n
                    lines = [l.strip() for l in item.splitlines() if l.strip()]
                    if len(lines) >= 3:
                        output.append(lines[0] + " | " + lines[1] + " | " + lines[-1])
            
            output = list(dict.fromkeys(output))

            if len(output) > 10:
                filename = "gare_2026.txt"
                with open(filename, "w", encoding="utf-8") as f:
                    for line in output:
                        f.write(line + NL)
                print("✨ SUCCESS: " + str(len(output)) + " races saved!")
            else:
                print("❌ ERROR: Only " + str(len(output)) + " races found. Still filtered?")
                filename = "gare_2026.txt"
                with open(filename, "w", encoding="utf-8") as f:
                    for line in output:
                        f.write(line + NL)

            browser.close()
        except Exception as e:
            print("FATAL ERROR: " + str(e))
            sys.exit(0)

if __name__ == "__main__":
    run()
