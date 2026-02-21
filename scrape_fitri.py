import os
from playwright.sync_api import sync_playwright

def scrape_fitri_calendar():
    year = "2026" # Puoi renderlo dinamico se preferisci
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://www.myfitri.it/calendario")

        # Clicca su "TUTTI"
        try:
            page.click("div.v-tab:has-text('TUTTI')")
            page.wait_for_timeout(3000) 
        except:
            print("Pulsante TUTTI non trovato, procedo con caricamento standard")

        # Selettore basato sulla struttura myFITri (Vuetify/Material Design)
        events = page.query_selector_all(".v-card") 
        
        output_lines = []
        for event in events:
            try:
                # Estrazione dati corretta con Nome Evento
                title_el = event.query_selector(".text-h6")
                if not title_el: continue
                title = title_el.inner_text().strip()
                
                date_loc_el = event.query_selector(".text-subtitle-2")
                date_loc = date_loc_el.inner_text().strip() if date_loc_el else "N/A"
                
                sub_events = event.query_selector_all(".v-list-item")
                for sub in sub_events:
                    sub_info = sub.inner_text().replace("
", " ").strip()
                    # Formato richiesto: Nome Evento | Data Località | Sotto-evento
                    line = f"{title} | {date_loc} | {sub_info}"
                    output_lines.append(line)
            except Exception as e:
                continue

        if output_lines:
            with open(f"gare_fitri_{year}.txt", "w", encoding="utf-8") as f:
                f.write("
".join(output_lines))
            print(f"File aggiornato con {len(output_lines)} righe.")
        
        browser.close()

if __name__ == "__main__":
    scrape_fitri_calendar()
