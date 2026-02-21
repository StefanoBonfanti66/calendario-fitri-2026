import time
import sys
from playwright.sync_api import sync_playwright

def run():
    print("🚀 MTT_LIVE_SCRAPER_V9_X_FILTER_FIX")
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
            page = context.new_page()
            
            url = "https://www.myfitri.it/calendario"
            print(f"🔗 Connessione a {url}...")
            page.goto(url, wait_until="networkidle", timeout=90000)
            time.sleep(10)

            # SBLOCCO FILTRO (Strategia migliorata)
            print("🧹 Sblocco calendario (rimozione filtri mese)...")
            page.evaluate("""() => {
                // 1. Cerca il tasto 'X' (v-chip__close) e clicca TUTTI quelli che trova
                const xButtons = document.querySelectorAll('.v-chip__close, button[aria-label*="close"], .v-icon--link');
                xButtons.forEach(b => b.click());
                
                // 2. Se non bastasse, cerca il tab che contiene 'TUTTI' e forza il click
                const allElements = Array.from(document.querySelectorAll('.v-tab, .v-btn, span, div'));
                const tutti = allElements.find(el => el.innerText && el.innerText.trim().toUpperCase() === 'TUTTI');
                if (tutti) {
                    tutti.click();
                    // Alcuni siti richiedono due click per confermare il cambio stato
                    setTimeout(() => tutti.click(), 500);
                }
            }""")
            time.sleep(8) # Diamo più tempo per ricaricare la lista sbloccata

            # SCROLLING per caricare la lista lunga ( lazy loading )
            print("🖱️ Scrolling profondo...")
            for i in range(15):
                page.mouse.wheel(0, 3000)
                time.sleep(1.5)

            # ESTRAZIONE DATI
            print("📊 Estrazione gare...")
            results = page.evaluate("""() => {
                const data = [];
                // Cerchiamo i container Vuetify standard per le gare
                const cards = document.querySelectorAll('.v-card, .v-list-item, [class*="card"]');
                cards.forEach(card => {
                    const text = card.innerText || "";
                    if (text.includes('2026') && text.length > 60) {
                        const lines = text.split('\\n').map(l => l.trim()).filter(l => l.length > 1);
                        if (lines.length >= 3) {
                            // Formato: EVENTO | DATA LOC | SPECIALITA
                            data.push(`${lines[0]} | ${lines[1]} | ${lines[lines.length-1]}`);
                        }
                    }
                });
                return [...new Set(data)];
            }""")

            if results:
                filename = "gare_fitri_2026.txt"
                with open(filename, "w", encoding="utf-8") as f:
                    for line in results:
                        f.write(line + "\\n")
                print(f"✅ SUCCESSO: Trovate {len(results)} gare!")
            else:
                print("❌ Nessuna gara trovata dopo lo sblocco.")

            browser.close()
        except Exception as e:
            print(f"⚠️ Errore: {e}")
            sys.exit(0)

if __name__ == "__main__":
    run()
