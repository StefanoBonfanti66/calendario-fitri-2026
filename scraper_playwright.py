import asyncio
import os
import sys
from playwright.async_api import async_playwright

async def scrape_fitri_calendar():
    async with async_playwright() as p:
        # Lancio browser con impostazioni specifiche per ambiente cloud
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={'width': 1280, 'height': 800}
        )
        page = await context.new_page()
        
        print("Connessione a MyFITri...")
        try:
            # Caricamento pagina con timeout aumentato
            await page.goto("https://www.myfitri.it/calendario", wait_until="networkidle", timeout=90000)
            
            # Attesa selettore principale
            await page.wait_for_selector("main", timeout=30000)
            print("Pagina caricata con successo.")
            
            # Clicca su "TUTTI" per caricare gli eventi dell'anno (se presente il tasto)
            try:
                await page.get_by_text("TUTTI", exact=True).last.click()
                await asyncio.sleep(3)
            except:
                pass

            # Estrazione dati in formato compatibile con il tuo parser
            # Cerchiamo blocchi che contengono date 2026
            events = await page.evaluate("""() => {
                const results = [];
                // Estrattore basato sulla struttura attuale Nuxt di MyFITri
                const eventNodes = document.querySelectorAll('div'); 
                eventNodes.forEach(node => {
                    const text = node.innerText;
                    if (text.includes('2026') && text.length > 50 && text.length < 500) {
                        // Cerchiamo di ricostruire la riga evento | data | regione | specialità
                        results.push(text.replace(/\\n/g, ' | '));
                    }
                });
                return [...new Set(results)]; // Rimuove duplicati
            }""")

            if events:
                # Se abbiamo nuovi dati, aggiorniamo il file
                with open("gare_2026.txt", "w", encoding="utf-8") as f:
                    for ev in events:
                        f.write(f"{ev.strip()}\n")
                print(f"Scraping completato: trovate {len(events)} righe di dati.")
            else:
                print("Nessun evento estratto. Verificare selettori.")

        except Exception as e:
            print(f"Errore durante lo scraping: {e}")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(scrape_fitri_calendar())
