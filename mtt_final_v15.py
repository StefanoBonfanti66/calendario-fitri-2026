import time
import sys
from playwright.sync_api import sync_playwright

NL = chr(10)

def run():
    print("🚀 STARTING_V15_ULTRA_UNLOCK")
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
            page = context.new_page()
            
            page.goto("https://www.myfitri.it/calendario", wait_until="networkidle", timeout=90000)
            print("🔗 Page Loaded. Waiting for rendering...")
            time.sleep(12)

            # ESECUZIONE SBLOCCO TOTALE VIA JS
            print("⚡ Executing Ultra-Unlock JS...")
            page.evaluate("""() => {
                // 1. Cerca e clicca su qualsiasi cosa sembri una 'X' di chiusura filtro
                const closeElements = document.querySelectorAll('.v-chip__close, .v-chip__filter, .v-icon--link, button[aria-label*="close"]');
                closeElements.forEach(el => {
                    el.click();
                    el.dispatchEvent(new MouseEvent('click', {view: window, bubbles: true, cancelable: true}));
                });

                // 2. Cerca specificamente il testo del mese corrente (es. FEBBRAIO) e clicca la sua X
                const allChips = Array.from(document.querySelectorAll('.v-chip'));
                const monthChips = allChips.filter(c => /Gennaio|Febbraio|Marzo|Aprile|Maggio|Giugno|Luglio|Agosto|Settembre|Ottobre|Novembre|Dicembre/i.test(c.innerText));
                monthChips.forEach(c => {
                    const x = c.querySelector('.v-chip__close') || c;
                    x.click();
                });

                // 3. Clicca sul tab TUTTI (con forza)
                const tabs = Array.from(document.querySelectorAll('.v-tab'));
                const tutti = tabs.find(t => t.innerText && t.innerText.toUpperCase().includes('TUTTI'));
                if (tutti) {
                    tutti.click();
                    // Simula anche il cambio di stato interno
                    tutti.dispatchEvent(new Event('change'));
                }
            }""")
            
            print("⏳ Waiting for data refresh (15s)...")
            time.sleep(15)

            # SCROLLING MASSICCIO (Vuetify potrebbe avere un container specifico)
            print("🖱️ Deep scrolling...")
            page.evaluate("""async () => {
                const scrollTarget = document.querySelector('main') || window;
                for (let i = 0; i < 30; i++) {
                    if (scrollTarget.scrollBy) scrollTarget.scrollBy(0, 3000);
                    else window.scrollBy(0, 3000);
                    await new Promise(r => setTimeout(r, 800));
                }
            }""")
            time.sleep(5)

            # ESTRAZIONE
            res = page.evaluate("() => Array.from(document.querySelectorAll('.v-card')).map(c => c.innerText)")
            output = []
            for item in res:
                if "2026" in item:
                    lines = [l.strip() for l in item.splitlines() if l.strip()]
                    if len(lines) >= 3:
                        output.append(lines[0] + " | " + lines[1] + " | " + lines[-1])
            
            output = list(dict.fromkeys(output))

            if output:
                with open("gare_fitri_2026.txt", "w", encoding="utf-8") as f:
                    for line in output:
                        f.write(line + NL)
                print("✅ SUCCESS_COUNT_" + str(len(output)))
            else:
                print("❌ NO_DATA_AFTER_UNLOCK")

            browser.close()
        except Exception as e:
            print("ERROR_" + str(e))
            sys.exit(0)

if __name__ == "__main__":
    run()
