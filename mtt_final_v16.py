import time
import sys
from playwright.sync_api import sync_playwright

NL = chr(10)

def run():
    print("🚀 STARTING_V16_MESE_13_FORCE")
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
            page = context.new_page()
            
            print("🔗 Connecting to MyFITri...")
            page.goto("https://www.myfitri.it/calendario", wait_until="networkidle", timeout=90000)
            time.sleep(10)

            # SBLOCCO FILTRO MESE (Basato sul tuo suggerimento 'meseCorrente: 13')
            print("⚡ Removing Month Filter (Looking for 'X')...")
            page.evaluate("""() => {
                const months = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"];
                
                // 1. Trova il chip del mese e clicca sulla sua X
                const chips = Array.from(document.querySelectorAll('.v-chip'));
                const activeMonthChip = chips.find(c => months.some(m => c.innerText.includes(m)));
                
                if (activeMonthChip) {
                    const closeIcon = activeMonthChip.querySelector('.v-chip__close') || activeMonthChip.querySelector('.v-icon') || activeMonthChip;
                    closeIcon.click();
                    console.log('Month chip closed');
                }

                // 2. Forza il click sul tab TUTTI
                const allTabs = Array.from(document.querySelectorAll('.v-tab'));
                const tuttiTab = allTabs.find(t => t.innerText && t.innerText.toUpperCase().includes('TUTTI'));
                if (tuttiTab) {
                    tuttiTab.click();
                    console.log('TUTTI tab clicked');
                }
            }""")
            
            print("⏳ Waiting for Season Unlock (15s)...")
            time.sleep(15)

            # SCROLLING
            print("🖱️ Deep scrolling to load all data...")
            for i in range(25):
                page.mouse.wheel(0, 4000)
                time.sleep(1)

            # ESTRAZIONE
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
                print(f"✅ SUCCESS: {len(output)} races found!")
            else:
                print(f"⚠️ Only {len(output)} races found. Still filtered?")
                # Salviamo comunque per debug
                with open("gare_fitri_2026.txt", "w", encoding="utf-8") as f:
                    for line in output: f.write(line + NL)

            browser.close()
        except Exception as e:
            print(f"ERROR: {e}")
            sys.exit(0)

if __name__ == "__main__":
    run()
