import time
import sys
import traceback
from playwright.sync_api import sync_playwright

def scrape_fitri_calendar():
    year = "2026"
    print("--- INIZIO DIAGNOSTICA SCRAPER ---")
    
    try:
        with sync_playwright() as p:
            print("1. Avvio Chromium...")
            browser = p.chromium.launch(headless=True)
            
            print("2. Creazione contesto e pagina...")
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
            )
            page = context.new_page()
            
            url = "https://www.myfitri.it/calendario"
            print(f"3. Navigazione verso {url}...")
            
            # Usiamo un'attesa più permissiva
            page.goto(url, wait_until="load", timeout=90000)
            print("4. Pagina caricata. Attendo rendering Vuetify...")
            time.sleep(10) # Diamo tempo al sito di "montarsi"
            
            # Catturiamo uno screenshot del log testuale (virtuale)
            print(f"5. Titolo pagina trovato: {page.title()}")

            print("6. Cerco il pulsante TUTTI...")
            # Proviamo a trovare il pulsante con un selettore di testo universale
            try:
                tutti_btn = page.get_by_role("tab").get_by_text("TUTTI", exact=False)
                if tutti_btn.count() > 0:
                    tutti_btn.first.click()
                    print("✅ Pulsante TUTTI cliccato con successo.")
                    time.sleep(5)
                else:
                    print("⚠️ Pulsante TUTTI non trovato via Role, provo via selettore generico...")
                    page.locator("div.v-tab").filter(has_text="TUTTI").click()
                    print("✅ Pulsante TUTTI cliccato via locator generico.")
                    time.sleep(5)
            except Exception as e:
                print(f"❌ Impossibile cliccare TUTTI: {e}")

            print("7. Scrolling per caricare tutta la stagione...")
            for i in range(5):
                page.mouse.wheel(0, 4000)
                time.sleep(2)

            print("8. Estrazione dati dai nodi card...")
            # MyFITri usa spesso .v-card o strutture simili
            cards = page.locator(".v-card, .event-card, div[class*='card']").all()
            print(f"Found {len(cards)} potential card elements.")
            
            output_lines = []
            for card in cards:
                try:
                    text = card.inner_text()
                    if "2026" in text:
                        lines = [l.strip() for l in text.split("\n") if l.strip()]
                        if len(lines) >= 3:
                            output_lines.append(f"{lines[0]} | {lines[1]} | {lines[-1]}")
                except:
                    continue

            output_lines = list(dict.fromkeys(output_lines))
            
            if output_lines:
                filename = f"gare_fitri_{year}.txt"
                with open(filename, "w", encoding="utf-8") as f:
                    f.write("\n".join(output_lines))
                print(f"--- FINISH: Generato {filename} con {len(output_lines)} gare ---")
            else:
                print("--- FINISH: Nessuna gara estratta, ma lo script è terminato correttamente ---")
                with open(f"gare_fitri_{year}.txt", "w", encoding="utf-8") as f:
                    f.write("Diagnostica: Dati non trovati nel DOM.")

            browser.close()

    except Exception as e:
        print("!!! ERRORE CRITICO RILEVATO !!!")
        print(f"Tipo errore: {type(e).__name__}")
        print(f"Messaggio: {str(e)}")
        print("--- TRACEBACK COMPLETO ---")
        traceback.print_exc()
        # Esco con 0 per vedere il log su GitHub senza bloccare il workflow
        sys.exit(0)

if __name__ == "__main__":
    scrape_fitri_calendar()
