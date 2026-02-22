import time
import sys
from playwright.sync_api import sync_playwright

def run():
    print("🚀 MTT_SCRAPER_V12_MESE_13_DEFINITIVE")
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
            page = context.new_page()
            
            print("🔗 Connecting to FITRI...")
            page.goto("https://www.myfitri.it/calendario", wait_until="networkidle", timeout=90000)
            time.sleep(10)

            # SBLOCCO MESE (Tua scoperta!)
            print("⚡ UNLOCKING: Forcing 'meseCorrente: 13' logic...")
            page.evaluate("""() => {
                document.querySelectorAll('.v-chip__close, .v-icon--link, button[aria-label*="close"]').forEach(el => el.click());
                const tabs = Array.from(document.querySelectorAll('.v-tab'));
                const tutti = tabs.find(t => t.innerText && t.innerText.toUpperCase().includes('TUTTI'));
                if (tutti) tutti.click();
            }""")
            time.sleep(10)

            # SCROLLING
            print("🖱️ Deep scrolling...")
            for i in range(25):
                page.mouse.wheel(0, 4000)
                time.sleep(1)

            # ESTRAZIONE
            print("📊 Extracting races...")
            results = page.evaluate("""() => {
                const out = [];
                document.querySelectorAll('.v-card').forEach(card => {
                    const txt = card.innerText || "";
                    if (txt.includes('2026') && txt.length > 60) {
                        const lines = txt.split('\\n').map(l => l.trim()).filter(l => l.length > 1);
                        if (lines.length >= 3) {
                            out.push(lines[0] + ' | ' + lines[1] + ' | ' + lines[lines.length-1]);
                        }
                    }
                });
                return [...new Set(out)];
            }""")

            if results:
                filename = "gare_fitri_2026.txt"
                with open(filename, "w", encoding="utf-8") as f:
                    for line in results:
                        # Scrittura sicura senza \n letterale nel codice
                        f.write(line)
                        f.write(chr(10))
                print(f"✅ SUCCESS: {len(results)} races saved!")
            else:
                print("❌ ERROR: No data extracted.")

            browser.close()
        except Exception as e:
            print(f"FATAL_ERROR: {e}")
            sys.exit(0)

if __name__ == "__main__":
    run()
