import time
import sys
from playwright.sync_api import sync_playwright

def run():
    print("🚀 MTT_SCRAPER_V10_ULTIMATE")
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
            page = context.new_page()
            
            print("🔗 Connecting...")
            page.goto("https://www.myfitri.it/calendario", wait_until="networkidle", timeout=90000)
            time.sleep(10)

            # Sblocco filtri massiccio
            print("🧹 Unlocking all races...")
            page.evaluate("""() => {
                // Clicca su ogni 'X' o tasto di chiusura filtri
                document.querySelectorAll('button, div, span, i').forEach(el => {
                    if (el.innerText === 'clear' || el.classList.contains('v-chip__close') || (el.getAttribute('aria-label') && el.getAttribute('aria-label').includes('close'))) {
                        el.click();
                    }
                });
                // Forza il tab TUTTI
                const tabs = Array.from(document.querySelectorAll('.v-tab'));
                const tutti = tabs.find(t => t.innerText.toUpperCase().includes('TUTTI'));
                if (tutti) tutti.click();
            }""")
            time.sleep(5)

            # Scrolling aggressivo
            for i in range(15):
                page.mouse.wheel(0, 4000)
                time.sleep(1)

            # Estrazione universale: prendi ogni blocco che parla di una gara 2026
            print("📊 Extracting...")
            results = page.evaluate("""() => {
                const out = [];
                // Cerchiamo i blocchi principali di Vuetify
                document.querySelectorAll('.v-card').forEach(card => {
                    const txt = card.innerText;
                    if (txt.includes('2026') && txt.length > 50) {
                        const lines = txt.split('\\n').map(l => l.trim()).filter(l => l.length > 1);
                        if (lines.length >= 3) {
                            out.push(lines[0] + ' | ' + lines[1] + ' | ' + lines[lines.length-1]);
                        }
                    }
                });
                return [...new Set(out)];
            }""")

            if results:
                with open("gare_fitri_2026.txt", "w", encoding="utf-8") as f:
                    for line in results:
                        f.write(line + "\n")
                print(f"DONE_FOUND_{len(results)}_RACES")
            else:
                print("RETRYING_WITH_BODY_TEXT")
                # Fallback: se le card falliscono, leggiamo il testo puro
                body_text = page.evaluate("document.body.innerText")
                with open("gare_fitri_2026.txt", "w", encoding="utf-8") as f:
                    f.write("Dati non strutturati trovati. Verificare sito.")

            browser.close()
        except Exception as e:
            print(f"FATAL_ERROR_{str(e)}")
            sys.exit(0)

if __name__ == "__main__":
    run()
