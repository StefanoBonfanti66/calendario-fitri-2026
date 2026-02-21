import os
import time
from playwright.sync_api import sync_playwright

def scrape_fitri_calendar():
    year = "2026"
    print("Avvio browser Playwright...")
    with sync_playwright() as p:
        # Lancio browser con User Agent realistico
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        print("Connessione a MyFITri...")
        try:
            page.goto("https://www.myfitri.it/calendario", wait_until="networkidle", timeout=60000)
            
            # Aspettiamo che la pagina sia effettivamente pronta
            page.wait_for_selector("body", timeout=10000)
            time.sleep(5) # Pausa per rendering JS

            # Tentativo di cliccare su "TUTTI" con selettore più elastico
            print("Cerco il pulsante TUTTI...")
            tabs = page.query_selector_all(".v-tab")
            for tab in tabs:
                if "TUTTI" in tab.inner_text().upper():
                    tab.click()
                    print("Pulsante TUTTI cliccato.")
                    time.sleep(5)
                    break

            # Estrazione dati: MyFITri usa spesso strutture annidate. 
            # Cerchiamo di prendere tutto ciò che sembra una card di evento.
            print("Estrazione eventi...")
            events = page.query_selector_all(".v-card, .event-card, [class*='card']") 
            
            output_lines = []
            for event in events:
                try:
                    text = event.inner_text()
                    if "2026" in text and len(text) > 50:
                        # Pulizia testo: trasformiamo i ritorni a capo in separatori
                        lines = [l.strip() for l in text.split("\n") if l.strip()]
                        if len(lines) >= 2:
                            # Tentiamo di mappare Titolo | Info | Dettaglio
                            title = lines[0]
                            info = lines[1]
                            detail = " ".join(lines[2:]) if len(lines) > 2 else "N/A"
                            output_lines.append(f"{title} | {info} | {detail}")
                except:
                    continue

            # Rimuoviamo duplicati mantenendo l'ordine
            output_lines = list(dict.fromkeys(output_lines))

            if output_lines:
                filename = f"gare_fitri_{year}.txt"
                with open(filename, "w", encoding="utf-8") as f:
                    f.write("\n".join(output_lines))
                print(f"Successo! Generato {filename} con {len(output_lines)} righe.")
            else:
                print("Attenzione: Nessun evento trovato con i selettori attuali.")
                # Creiamo un file vuoto per evitare l'exit code 1 se vogliamo che l'action passi comunque
                with open(f"gare_fitri_{year}.txt", "w", encoding="utf-8") as f:
                    f.write("Nessun dato trovato - Verificare sito MyFITri")

        except Exception as e:
            print(f"Errore critico durante lo scraping: {e}")
            # Non facciamo crashare l'action, scriviamo l'errore nel log
        
        browser.close()

if __name__ == "__main__":
    scrape_fitri_calendar()
