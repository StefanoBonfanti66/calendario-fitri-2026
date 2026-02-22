import time
import sys
from playwright.sync_api import sync_playwright

NL = chr(10)

def run():
    print("🚀 MTT_SCRAPER_V17_FINAL_SMASH")
    with sync_playwright() as p:
        try:
            # Headless=True per GitHub Actions
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
            page = context.new_page()
            
            print("🔗 Connecting to MyFITri...")
            page.goto("https://www.myfitri.it/calendario", wait_until="networkidle", timeout=90000)
            time.sleep(10)

            # SBLOCCO FILTRO MESE (La tecnica che hai confermato funzionare!)
            print("⚡ UNLOCKING: Removing all active filters...")
            page.evaluate("""() => {
                // 1. Identifica tutti i chip dei filtri (Gennaio, Febbraio, ecc.)
                const months = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"];
                
                // 2. Trova e clicca su OGNI icona di chiusura (X) nella pagina
                const closeIcons = document.querySelectorAll('.v-chip__close, .v-icon--link, [class*="close"]');
                closeIcons.forEach(icon => {
                    icon.click();
                    // Simula anche un evento di mouse per sicurezza
                    icon.dispatchEvent(new MouseEvent('click', {bubbles: true}));
                });

                // 3. Fallback: clicca su qualsiasi chip che contiene il nome di un mese
                const allChips = Array.from(document.querySelectorAll('.v-chip'));
                allChips.forEach(chip => {
                    if (months.some(m => chip.innerText.includes(m))) {
                        const x = chip.querySelector('.v-chip__close') || chip.querySelector('i') || chip;
                        x.click();
                    }
                });

                // 4. Forza il tab TUTTI
                const tabs = Array.from(document.querySelectorAll('.v-tab'));
                const tutti = tabs.find(t => t.innerText && t.innerText.toUpperCase().includes('TUTTI'));
                if (tutti) tutti.click();
            }""")
            
            print("⏳ Waiting for data to refresh (15s)...")
            time.sleep(15)

            # SCROLLING
            print("🖱️ Scrolling through the entire season...")
            for i in range(25):
                page.mouse.wheel(0, 4000)
                time.sleep(1)

            # ESTRAZIONE
            print("📊 Extracting data...")
            res = page.evaluate("() => Array.from(document.querySelectorAll('.v-card')).map(c => c.innerText)")
            output = []
            for item in res:
                if "2026" in item:
                    lines = [l.strip() for l in item.splitlines() if l.strip()]
                    if len(lines) >= 3:
                        output.append(lines[0] + " | " + lines[1] + " | " + lines[-1])
            
            output = list(dict.fromkeys(output))

            if len(output) > 10:
                filename = "gare_fitri_2026.txt"
                with open(filename, "w", encoding="utf-8") as f:
                    for line in output:
                        f.write(line + NL)
                print(f"✅ MISSIONE COMPIUTA: Trovate {len(output)} gare!")
            else:
                print(f"⚠️ Solo {len(output)} gare trovate. Lo sblocco automatico potrebbe aver fallito.")
                with open("gare_fitri_2026.txt", "w", encoding="utf-8") as f:
                    for line in output: f.write(line + NL)

            browser.close()
        except Exception as e:
            print(f"ERROR: {e}")
            sys.exit(0)

if __name__ == "__main__":
    run()
