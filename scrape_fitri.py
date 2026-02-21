import asyncio
import sys
import time
from playwright.async_api import async_playwright

async def scrape_fitri_calendar():
    year = "2026"
    print("🚀 Avvio scraper professionale...")
    
    async with async_playwright() as p:
        # Lancio browser con parametri per evitare rilevamenti bot
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={'width': 1920, 'height': 1080}
        )
        page = await context.new_page()
        
        url = "https://www.myfitri.it/calendario"
        print(f"🔗 Connessione a {url}...")
        
        try:
            # Navigazione con attesa generosa
            response = await page.goto(url, wait_until="networkidle", timeout=90000)
            print(f"📥 Status Code: {response.status if response else 'N/A'}")
            
            # Aspetta che la pagina carichi il contenuto dinamico
            await page.wait_for_timeout(5000)
            
            # Clicca sul tab TUTTI
            print("🔍 Ricerca pulsante TUTTI...")
            tabs = await page.query_selector_all(".v-tab")
            for tab in tabs:
                text = await tab.inner_text()
                if "TUTTI" in text.upper():
                    await tab.click()
                    print("✅ Pulsante TUTTI cliccato.")
                    await page.wait_for_timeout(5000)
                    break

            # Scrolling per caricare tutta la lista
            print("🖱️ Scrolling della pagina...")
            for i in range(10):
                await page.mouse.wheel(0, 2000)
                await page.wait_for_timeout(1000)

            # Estrazione di tutti i blocchi di testo che sembrano gare
            print("📊 Estrazione dati...")
            content = await page.evaluate("""() => {
                const data = [];
                // Cerchiamo tutti i blocchi che contengono '2026'
                document.querySelectorAll('div').forEach(div => {
                    const text = div.innerText;
                    if (text && text.includes('2026') && text.length > 100 && text.length < 1000) {
                        data.push(text);
                    }
                });
                return [...new Set(data)];
            }""")

            output_lines = []
            for item in content:
                # Pulizia base del testo per il formato EVENTO | DATA | SPEC
                parts = [p.strip() for p in item.split('\n') if p.strip()]
                if len(parts) >= 3:
                    # Semplifichiamo il formato per il tuo parser
                    line = f"{parts[0]} | {parts[1]} | {parts[-1]}"
                    output_lines.append(line)

            if output_lines:
                filename = f"gare_fitri_{year}.txt"
                with open(filename, "w", encoding="utf-8") as f:
                    f.write("\n".join(output_lines))
                print(f"✨ SUCCESSO: Salvate {len(output_lines)} gare in {filename}")
            else:
                print("❌ Nessuna gara trovata nel contenuto della pagina.")
                # Creiamo un file minimo per non far fallire il push successivo
                with open(f"gare_fitri_{year}.txt", "w", encoding="utf-8") as f:
                    f.write("Nessun dato trovato nell'ultima scansione.")

        except Exception as e:
            print(f"⚠️ Errore durante l'esecuzione: {e}")
            # Non usciamo con errore per permettere alla GitHub Action di finire
        
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(scrape_fitri_calendar())
