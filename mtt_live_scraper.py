import time
import sys
from playwright.sync_api import sync_playwright

def run():
    print("🚀 MTT_SCRAPER_V11_MESE_13_UNLOCK")
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
            page = context.new_page()
            
            print("🔗 Connessione a MyFITri...")
            page.goto("https://www.myfitri.it/calendario", wait_until="networkidle", timeout=90000)
            time.sleep(10)

            # SBLOCCO FILTRO MESE (Basato sulla tua scoperta: meseCorrente = 13)
            print("⚡ Sblocco filtri: impostazione 'Tutti i mesi' (ID 13)...")
            page.evaluate("""() => {
                // 1. Cerchiamo di chiudere qualsiasi chip di filtro attivo (la 'X' che hai visto)
                const chips = Array.from(document.querySelectorAll('.v-chip'));
                const monthChip = chips.find(c => /Gennaio|Febbraio|Marzo|Aprile|Maggio|Giugno|Luglio|Agosto|Settembre|Ottobre|Novembre|Dicembre/i.test(c.innerText));
                if (monthChip) {
                    const closeBtn = monthChip.querySelector('.v-chip__close');
                    if (closeBtn) closeBtn.click();
                    console.log('Filtro mese chiuso tramite X');
                }

                // 2. Metodo alternativo: forziamo il selettore 'TUTTI' se presente
                const tabs = Array.from(document.querySelectorAll('.v-tab'));
                const tutti = tabs.find(t => t.innerText && t.innerText.toUpperCase().includes('TUTTI'));
                if (tutti) tutti.click();
            }""")
            
            time.sleep(10) # Tempo generoso per caricare tutto l'anno

            # SCROLLING per caricare la lista lunga
            print("🖱️ Scorrimento per catturare l'intera stagione...")
            for i in range(25): # Più scroll per essere sicuri
                page.mouse.wheel(0, 4000)
                time.sleep(1)

            # ESTRAZIONE DATI
            print("📊 Estrazione gare...")
            results = page.evaluate("""() => {
                const data = [];
                const cards = document.querySelectorAll('.v-card');
                cards.forEach(card => {
                    const text = card.innerText || "";
                    if (text.includes('2026') && text.length > 60) {
                        const lines = text.split('\\n').map(l => l.trim()).filter(l => l.length > 1);
                        if (lines.length >= 3) {
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
                print(f"✅ MISSIONE COMPIUTA: Trovate {len(results)} gare!")
            else:
                print("❌ Errore: Nessuna gara estratta dopo lo sblocco.")

            browser.close()
        except Exception as e:
            print(f"⚠️ Errore critico: {e}")
            sys.exit(0)

if __name__ == "__main__":
    run()
