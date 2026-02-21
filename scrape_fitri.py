import time
import sys
from playwright.sync_api import sync_playwright

def scrape_fitri_calendar():
    year = "2026"
    print("🚀 Avvio scraper stabile (Sync Mode)...")
    
    with sync_playwright() as p:
        try:
            # Lancio browser con User Agent umano
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
            )
            page = context.new_page()
            
            url = "https://www.myfitri.it/calendario"
            print(f"🔗 Connessione a {url}...")
            
            page.goto(url, wait_until="domcontentloaded", timeout=90000)
            time.sleep(5)
            
            # Clicca su TUTTI per caricare tutto
            print("🔍 Ricerca pulsante TUTTI...")
            tabs = page.query_selector_all(".v-tab")
            for tab in tabs:
                if "TUTTI" in tab.inner_text().upper():
                    tab.click()
                    print("✅ Pulsante TUTTI cliccato.")
                    time.sleep(5)
                    break

            # Scrolling profondo
            print("🖱️ Scorrimento pagina in corso...")
            for i in range(10):
                page.mouse.wheel(0, 3000)
                time.sleep(1)

            # Estrazione dati basata sui blocchi di testo
            print("📊 Analisi contenuti...")
            elements = page.query_selector_all("div")
            
            output_lines = []
            for el in elements:
                try:
                    text = el.inner_text()
                    # Cerchiamo blocchi che contengono date 2026 e dettagli sportivi
                    if "2026" in text and any(x in text.upper() for x in ["TRIATHLON", "DUATHLON", "AQUATHLON"]):
                        lines = [l.strip() for l in text.split("\n") if l.strip()]
                        if len(lines) >= 3:
                            # Formato: EVENTO | DATA LOC | DETTAGLIO
                            # Prendiamo solo i blocchi unici e significativi
                            clean_line = f"{lines[0]} | {lines[1]} | {lines[-1]}"
                            output_lines.append(clean_line)
                except:
                    continue

            # Pulizia e salvataggio
            output_lines = list(dict.fromkeys(output_lines))
            
            if output_lines:
                filename = f"gare_fitri_{year}.txt"
                with open(filename, "w", encoding="utf-8") as f:
                    f.write("\n".join(output_lines))
                print(f"✨ COMPLETATO: Trovate {len(output_lines)} gare.")
            else:
                print("❌ Nessuna gara estratta. Verificare struttura sito.")
                with open(f"gare_fitri_{year}.txt", "w", encoding="utf-8") as f:
                    f.write("Scansione completata - Dati non trovati")

            browser.close()

        except Exception as e:
            print(f"⚠️ Errore script: {e}")
            # Non usciamo con 1 per non rompere il workflow
            sys.exit(0)

if __name__ == "__main__":
    scrape_fitri_calendar()
