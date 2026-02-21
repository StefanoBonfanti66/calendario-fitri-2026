import os
import time
from playwright.sync_api import sync_playwright

def scrape_fitri_calendar():
    year = "2026"
    print("Avvio browser Playwright...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={'width': 1280, 'height': 1000}
        )
        page = context.new_page()
        
        print("Connessione a MyFITri...")
        try:
            page.goto("https://www.myfitri.it/calendario", wait_until="networkidle", timeout=90000)
            time.sleep(5)

            # 1. Tentativo forzato di cliccare su "TUTTI"
            print("Cerco il pulsante TUTTI per sbloccare l'intera stagione...")
            # Proviamo diversi selettori comuni in Vuetify per il tab TUTTI
            selectors = [
                "div.v-tab:has-text('TUTTI')",
                "//div[contains(@class, 'v-tab') and contains(text(), 'TUTTI')]",
                "text=TUTTI"
            ]
            
            clicked = False
            for selector in selectors:
                try:
                    if page.is_visible(selector):
                        page.click(selector)
                        print(f"Pulsante cliccato con selettore: {selector}")
                        clicked = True
                        time.sleep(5)
                        break
                except:
                    continue
            
            if not clicked:
                print("Avviso: Pulsante TUTTI non trovato, proverò a scorrere comunque.")

            # 2. INFINITE SCROLLING: Scorriamo verso il basso per forzare il caricamento lazy-load
            print("Inizio scrolling della pagina per caricare tutti gli eventi...")
            last_height = page.evaluate("document.body.scrollHeight")
            for i in range(15): # Proviamo a scorrere 15 volte
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(2)
                new_height = page.evaluate("document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
                print(f"Scorrimento {i+1} completato...")

            # 3. Estrazione dati
            print("Estrazione eventi finali...")
            # Cerchiamo tutti i blocchi che contengono info di gara
            # Spesso MyFITri usa classi come .v-card o .card-evento
            events = page.query_selector_all(".v-card, .event-card, div[class*='card']") 
            
            output_lines = []
            for event in events:
                try:
                    text = event.inner_text()
                    # Filtriamo solo i blocchi che contengono effettivamente date 2026 e hanno una lunghezza minima
                    if "2026" in text and len(text) > 100:
                        # Pulizia e formattazione riga
                        parts = [p.strip() for p in text.split("\n") if p.strip()]
                        if len(parts) >= 3:
                            # Cerchiamo di identificare Titolo | Località | Dettagli
                            title = parts[0]
                            # Spesso la seconda riga è la data/località
                            info = parts[1]
                            # Le righe successive sono le specialità
                            for sub in parts[2:]:
                                if any(x in sub.upper() for x in ["TRIATHLON", "DUATHLON", "AQUATHLON", "CROSS"]):
                                    output_lines.append(f"{title} | {info} | {sub}")
                except:
                    continue

            # Rimuoviamo duplicati
            output_lines = list(dict.fromkeys(output_lines))

            if output_lines:
                filename = f"gare_fitri_{year}.txt"
                with open(filename, "w", encoding="utf-8") as f:
                    f.write("\n".join(output_lines))
                print(f"GRANDE SUCCESSO! Generato {filename} con {len(output_lines)} gare trovate.")
            else:
                print("Nessun evento trovato. Proverò a catturare l'intera pagina come debug.")
                with open(f"gare_fitri_{year}.txt", "w", encoding="utf-8") as f:
                    f.write(page.inner_text())

        except Exception as e:
            print(f"Errore critico: {e}")
        
        browser.close()

if __name__ == "__main__":
    scrape_fitri_calendar()
