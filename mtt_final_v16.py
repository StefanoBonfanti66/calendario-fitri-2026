import time
import sys
import re
from playwright.sync_api import sync_playwright

NL = chr(10)

def run():
    print("🚀 MTT_SCRAPER_V20_DEEP_LINKING")
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
            page = context.new_page()
            
            print("🔗 Connecting to MyFITri...")
            page.goto("https://www.myfitri.it/calendario", wait_until="networkidle", timeout=90000)
            time.sleep(10)

            print("🧹 Removing Filters...")
            page.evaluate("""() => {
                const months = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"];
                document.querySelectorAll('.v-chip__close, .v-icon--link, button[aria-label*="close"]').forEach(el => el.click());
                const tabs = Array.from(document.querySelectorAll('.v-tab'));
                const tutti = tabs.find(t => t.innerText && t.innerText.toUpperCase().includes('TUTTI'));
                if (tutti) tutti.click();
            }""")
            time.sleep(15)

            print("🖱️ Deep scrolling...")
            for i in range(25):
                page.mouse.wheel(0, 4000)
                time.sleep(1)

            # ESTRAZIONE AVANZATA (Testo + Link)
            print("📊 Extracting races with deep links...")
            results = page.evaluate("""() => {
                const out = [];
                document.querySelectorAll('.v-card').forEach(card => {
                    const txt = card.innerText || "";
                    if (txt.includes('2026') && txt.length > 60) {
                        const lines = txt.split('\\n').map(l => l.trim()).filter(l => l.length > 1);
                        
                        // Cerchiamo il link alla scheda gara (solitamente è un pulsante o l'ID è nel DOM)
                        // MyFITri usa link tipo /calendario/evento/ID
                        const linkEl = card.querySelector('a[href*="/evento/"]');
                        const link = linkEl ? linkEl.href : "";
                        
                        if (lines.length >= 3) {
                            // Nuovo formato: EVENTO | DATA LOC | SPECIALITÀ | LINK
                            out.push(`${lines[0]} | ${lines[1]} | ${lines[lines.length-1]} | ${link}`);
                        }
                    }
                });
                return [...new Set(out)];
            }""")

            if len(results) > 10:
                filename = "gare_2026.txt"
                with open(filename, "w", encoding="utf-8") as f:
                    for line in results:
                        f.write(line + NL)
                print(f"✨ SUCCESS: {len(results)} races with links saved!")
            else:
                print("❌ ERROR: Only " + str(len(results)) + " found.")

            browser.close()
        except Exception as e:
            print(f"FATAL ERROR: {e}")
            sys.exit(0)

if __name__ == "__main__":
    run()
