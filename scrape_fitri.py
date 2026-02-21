import time
import sys
from playwright.sync_api import sync_playwright

def scrape_fitri_calendar():
    year = "2026"
    print("🚀 Avvio scraper NINJA (JS Injection Mode)...")
    
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
            )
            page = context.new_page()
            
            url = "https://www.myfitri.it/calendario"
            print(f"🔗 Connessione a {url}...")
            
            # Navigazione
            page.goto(url, wait_until="domcontentloaded", timeout=90000)
            print("⏳ Attesa caricamento iniziale (10s)...")
            time.sleep(10)

            # ESECUZIONE JS: Questa parte forza il sito a mostrare tutto
            print("⚡ Iniezione JavaScript per forzare il tab TUTTI...")
            page.evaluate("""() => {
                // Trova tutti i div che sembrano tab
                const elements = Array.from(document.querySelectorAll('div, span, a'));
                const tutti = elements.find(el => el.innerText && el.innerText.trim().toUpperCase() === 'TUTTI');
                if (tutti) {
                    tutti.click();
                    console.log('TUTTI cliccato via JS');
                }
            }""")
            time.sleep(5)

            # SCROLLING JS: Forza il caricamento di tutta la lista lunga
            print("🖱️ Scrolling automatico via JS...")
            page.evaluate("""async () => {
                for (let i = 0; i < 15; i++) {
                    window.scrollBy(0, 3000);
                    await new Promise(r => setTimeout(r, 1000));
                }
            }""")
            time.sleep(2)

            # ESTRAZIONE DATI: Legge direttamente i nodi card
            print("📊 Cattura dati in corso...")
            results = page.evaluate("""() => {
                const data = [];
                // Cerchiamo le card Vue/Vuetify
                const cards = document.querySelectorAll('.v-card, .event-card, [class*="card"]');
                cards.forEach(card => {
                    const text = card.innerText;
                    if (text && text.includes('2026') && text.length > 60) {
                        const lines = text.split('\\n').map(l => l.trim()).filter(l => l.length > 1);
                        if (lines.length >= 3) {
                            // Formato: EVENTO | DATA LOC | ULTIMA RIGA (SPECIALITÀ)
                            data.push(`${lines[0]} | ${lines[1]} | ${lines[lines.length-1]}`);
                        }
                    }
                });
                return [...new Set(data)];
            }""")

            if results:
                filename = f"gare_fitri_{year}.txt"
                with open(filename, "w", encoding="utf-8") as f:
                    f.write("\n".join(results))
                print(f"✨ COMPLETATO: Trovate {len(results)} gare uniche.")
            else:
                print("❌ Nessuna gara trovata con JS. Verifico testo grezzo...")
                # Metodo di emergenza: prendi tutto il testo che contiene 2026
                text_fallback = page.evaluate("document.body.innerText")
                with open(f"gare_fitri_{year}.txt", "w", encoding="utf-8") as f:
                    f.write("FALLBACK: " + text_fallback[:5000])

            browser.close()

        except Exception as e:
            print(f"⚠️ Errore critico: {e}")
            sys.exit(0)

if __name__ == "__main__":
    scrape_fitri_calendar()
