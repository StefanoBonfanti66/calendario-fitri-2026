import time
import sys
from playwright.sync_api import sync_playwright

def scrape_fitri_calendar():
    year = "2026"
    print("🚀 AVVIO SCRAPER FINALE (Stabilità Massima)...")
    
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
            page = context.new_page()
            
            url = "https://www.myfitri.it/calendario"
            print(f"🔗 Connessione a {url}...")
            page.goto(url, wait_until="domcontentloaded", timeout=90000)
            time.sleep(10)

            # Forza il tab TUTTI via JS
            print("⚡ Click TUTTI...")
            page.evaluate("() => { const tabs = Array.from(document.querySelectorAll('div, span, a')); const target = tabs.find(t => t.innerText && t.innerText.trim().toUpperCase() === 'TUTTI'); if (target) target.click(); }")
            time.sleep(5)

            # Scrolling via JS
            print("🖱️ Scrolling...")
            page.evaluate("async () => { for (let i = 0; i < 15; i++) { window.scrollBy(0, 3000); await new Promise(r => setTimeout(r, 1000)); } }")
            time.sleep(2)

            # Estrazione sicura (senza caratteri speciali problematici)
            print("📊 Estrazione dati...")
            results = page.evaluate("""() => {
                const data = [];
                const cards = document.querySelectorAll('.v-card, .event-card, [class*="card"]');
                cards.forEach(card => {
                    const text = card.innerText || "";
                    if (text.includes('2026') && text.length > 60) {
                        // Usiamo un separatore testuale invece di 
 per evitare errori di escape
                        const parts = text.split(/[
]+/).map(l => l.trim()).filter(l => l.length > 1);
                        if (parts.length >= 3) {
                            data.push(parts[0] + " | " + parts[1] + " | " + parts[parts.length-1]);
                        }
                    }
                });
                return [...new Set(data)];
            }""")

            if results:
                with open(f"gare_fitri_{year}.txt", "w", encoding="utf-8") as f:
                    f.write("
".join(results))
                print(f"✅ SUCCESSO: Trovate {len(results)} gare.")
            else:
                print("❌ Nessuna gara trovata.")

            browser.close()
        except Exception as e:
            print(f"⚠️ Errore critico: {e}")
            sys.exit(0)

if __name__ == "__main__":
    scrape_fitri_calendar()
