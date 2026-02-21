import time
import sys
from playwright.sync_api import sync_playwright

def scrape_fitri_calendar():
    year = "2026"
    print("🚀 AVVIO NINJA SCRAPER V2 (Force Refresh)...")
    
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
            page = context.new_page()
            
            url = "https://www.myfitri.it/calendario"
            print(f"🔗 Connessione a {url}...")
            page.goto(url, wait_until="domcontentloaded", timeout=90000)
            time.sleep(10)

            # Clicca TUTTI via JS
            page.evaluate("""() => {
                const el = Array.from(document.querySelectorAll('div, span, a')).find(e => e.innerText && e.innerText.trim().toUpperCase() === 'TUTTI');
                if (el) el.click();
            }""")
            time.sleep(5)

            # Scrolling JS
            page.evaluate("""async () => {
                for (let i = 0; i < 15; i++) {
                    window.scrollBy(0, 3000);
                    await new Promise(r => setTimeout(r, 1000));
                }
            }""")
            time.sleep(2)

            # Estrazione
            results = page.evaluate("""() => {
                const data = [];
                const cards = document.querySelectorAll('.v-card, .event-card, [class*="card"]');
                cards.forEach(card => {
                    const text = card.innerText;
                    if (text && text.includes('2026') && text.length > 60) {
                        const lines = text.split('
').map(l => l.trim()).filter(l => l.length > 1);
                        if (lines.length >= 3) {
                            data.push(`${lines[0]} | ${lines[1]} | ${lines[lines.length-1]}`);
                        }
                    }
                });
                return [...new Set(data)];
            }""")

            if results:
                with open(f"gare_fitri_{year}.txt", "w", encoding="utf-8") as f:
                    f.write("
".join(results))
                print(f"✨ SUCCESSO: Trovate {len(results)} gare.")
            else:
                print("❌ Nessun dato trovato.")

            browser.close()
        except Exception as e:
            print(f"⚠️ Errore: {e}")
            sys.exit(0)

if __name__ == "__main__":
    scrape_fitri_calendar()
