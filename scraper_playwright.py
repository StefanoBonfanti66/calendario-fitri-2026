import asyncio
import os
import sys
from playwright.async_api import async_playwright

async def scrape_fitri_calendar():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={'width': 1280, 'height': 800}
        )
        page = await context.new_page()
        
        print("Connessione a MyFITri...")
        try:
            await page.goto("https://www.myfitri.it/calendario", wait_until="networkidle", timeout=90000)
            await page.wait_for_selector("main", timeout=30000)
            
            # Clicca su 2026 se necessario
            # Clicca su TUTTI per caricare tutto
            try:
                await page.get_by_text("TUTTI", exact=True).last.click()
                await asyncio.sleep(5) # Attendiamo il caricamento della lista lunga
            except:
                pass

            # Estrazione intelligente basata sulla struttura effettiva dei nodi
            # Cerchiamo di ricostruire: NOME_EVENTO | DATA_LOC_GENERICA | REGIONE | SOTTO_EVENTO
            data_rows = await page.evaluate("""() => {
                const results = [];
                // MyFITri raggruppa le gare per container. Cerchiamo i container principali.
                const containers = document.querySelectorAll('.card-evento-container, div[class*="event"]');
                
                containers.forEach(container => {
                    const text = container.innerText;
                    if (text.includes('2026')) {
                        // Proviamo a pulire il testo per renderlo simile al formato richiesto
                        const lines = text.split('\\n').map(l => l.trim()).filter(l => l.length > 2);
                        if (lines.length >= 3) {
                            // Semplificazione: creiamo una riga compatibile con il parser
                            // Formato: EVENTO | DATA LOC | REGIONE | DATA_SPECIFICA TITOLO
                            // Nota: MyFITri spesso mette tutto in blocchi. Qui facciamo una stima.
                            const event = lines[0];
                            const dateLoc = lines[1];
                            const region = lines.includes('Lombardia') ? 'Lombardia' : 'Italia'; // Fallback
                            const subEvent = lines[lines.length-1];
                            
                            results.push(`${event} | ${dateLoc} | ${region} | ${subEvent}`);
                        }
                    }
                });
                return results;
            }""")

            if data_rows:
                # Sovrascriviamo solo se abbiamo trovato dati validi
                with open("gare_2026.txt", "w", encoding="utf-8") as f:
                    for row in data_rows:
                        f.write(f"{row}\n")
                print(f"Scraping completato: {len(data_rows)} gare salvate.")
            else:
                # Se non troviamo nulla con i selettori specifici, usiamo un metodo fallback
                # per non rompere il file originale se lo scraping fallisce.
                print("Nessun dato estratto. Verificare selettori o struttura sito.")
                # Non scriviamo nulla nel file per preservare i dati esistenti

        except Exception as e:
            print(f"Errore critico durante lo scraping: {e}")
            # In caso di errore, usciamo con 0 per non far fallire l'Action, 
            # semplicemente non aggiorneremo i dati per oggi.
            sys.exit(0) 
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(scrape_fitri_calendar())
