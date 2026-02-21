import time
import sys
from playwright.sync_api import sync_playwright

def run():
    print("🚀 MTT_LIVE_SCRAPER_V8_UNLOCKING_FULL_YEAR")
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
            page = context.new_page()
            
            print("🔗 Connessione a MyFITri...")
            page.goto("https://www.myfitri.it/calendario", wait_until="networkidle", timeout=90000)
            time.sleep(10)

            # RIMOZIONE FILTRO MESE (La tua intuizione!)
            print("🧹 Rimozione filtri attivi (chiusura 'X' del mese)...")
            page.evaluate("""() => {
                // Cerca tutti i chip dei filtri attivi (spesso hanno una classe 'v-chip' o simili)
                // e clicca sulla 'X' (v-chip__close o icona di chiusura)
                const closeButtons = document.querySelectorAll('.v-chip__close, .v-icon--link, button[aria-label*="close"]');
                closeButtons.forEach(btn => btn.click());
                
                // Se non bastasse, cerchiamo il tab TUTTI
                const tabs = Array.from(document.querySelectorAll('div, span, a'));
                const tutti = tabs.find(el => el.innerText && el.innerText.trim().toUpperCase() === 'TUTTI');
                if (tutti) tutti.click();
            }""")
            time.sleep(5)

            # SCROLLING per caricare la lista ora sbloccata
            print("🖱️ Scorrimento per caricare tutta la stagione...")
            page.evaluate("""async () => {
                for (let i = 0; i < 20; i++) {
                    window.scrollBy(0, 3000);
                    await new Promise(r => setTimeout(r, 1000));
                }
            }""")
            time.sleep(2)

            # ESTRAZIONE DATI
            print("📊 Estrazione gare in corso...")
            results = page.evaluate("""() => {
                const data = [];
                const cards = document.querySelectorAll('.v-card, .event-card');
                cards.forEach(card => {
                    const text = card.innerText || "";
                    if (text.includes('2026') && text.length > 60) {
                        const parts = text.split('\\n').map(l => l.trim()).filter(l => l.length > 1);
                        if (parts.length >= 3) {
                            data.push(`${parts[0]} | ${parts[1]} | ${parts[parts.length-1]}`);
                        }
                    }
                });
                return [...new Set(data)];
            }""")

            if results:
                with open("gare_fitri_2026.txt", "w", encoding="utf-8") as f:
                    for line in results:
                        f.write(line + "\\n")
                print(f"✅ SUCCESSO: Trovate {len(results)} gare per l'intera stagione!")
            else:
                print("❌ Nessuna gara trovata. Verificare selettori.")

            browser.close()
        except Exception as e:
            print(f"⚠️ Errore critico: {e}")
            sys.exit(0)

if __name__ == "__main__":
    run()
