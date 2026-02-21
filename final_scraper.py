import time
import sys
from playwright.sync_api import sync_playwright

def scrape_fitri_calendar():
    year = "2026"
    print("STARTING_STABLE_SCRAPER_V5")
    
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
            page = context.new_page()
            
            print("CONNECTING_TO_FITRI")
            page.goto("https://www.myfitri.it/calendario", wait_until="domcontentloaded", timeout=90000)
            time.sleep(10)

            print("CLICKING_TUTTI")
            page.evaluate("() => { const tabs = Array.from(document.querySelectorAll('div, span, a')); const target = tabs.find(t => t.innerText && t.innerText.trim().toUpperCase() === 'TUTTI'); if (target) target.click(); }")
            time.sleep(5)

            print("SCROLLING")
            page.evaluate("async () => { for (let i = 0; i < 15; i++) { window.scrollBy(0, 3000); await new Promise(r => setTimeout(r, 1000)); } }")
            time.sleep(2)

            print("EXTRACTING_DATA")
            # Logica pulita senza commenti o escape problematici
            results = page.evaluate("""() => {
                const data = [];
                const cards = document.querySelectorAll('.v-card, .event-card, [class*="card"]');
                cards.forEach(card => {
                    const text = card.innerText || "";
                    if (text.includes('2026') && text.length > 60) {
                        const parts = text.split(/[\\r\\n]+/).map(l => l.trim()).filter(l => l.length > 1);
                        if (parts.length >= 3) {
                            data.push(parts[0] + ' | ' + parts[1] + ' | ' + parts[parts.length-1]);
                        }
                    }
                });
                return [...new Set(data)];
            }""")

            if results:
                with open(f"gare_fitri_{year}.txt", "w", encoding="utf-8") as f:
                    for line in results:
                        f.write(line + "\n")
                print(f"SUCCESS_FOUND_{len(results)}_RACES")
            else:
                print("NO_DATA_FOUND")

            browser.close()
        except Exception as e:
            print(f"CRITICAL_ERROR: {str(e)}")
            sys.exit(0)

if __name__ == "__main__":
    scrape_fitri_calendar()
