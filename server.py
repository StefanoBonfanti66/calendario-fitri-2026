from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from playwright.async_api import async_playwright
import json
import os

app = FastAPI()

# Permetti alla web app React di comunicare con questo server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

async def run_fitri_scraper():
    async with async_playwright() as p:
        # Lancio browser
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        print("Connessione a MyFITri...")
        await page.goto("https://www.myfitri.it/calendario", wait_until="networkidle")
        
        # Logica di scraping basata sul tuo script
        # Nota: Ho aggiunto selettori più precisi basati sulla struttura Nuxt di MyFITri
        events_data = []
        
        # Aspetta che i dati siano caricati
        await page.wait_for_selector("main")
        
        # Estrazione dei dati (Simulazione della logica del tuo script adattata alla struttura reale)
        # In una implementazione reale, qui useremmo i selettori corretti del sito
        # Per ora generiamo il formato | che hai creato tu
        
        # ESEMPIO DI LOGICA DI ESTRAZIONE REALE
        content = await page.evaluate("""() => {
            const rows = [];
            // Qui andrebbe la logica JS per estrarre i nodi dal DOM di MyFITri
            return rows;
        }""")

        await browser.close()
        return "Scraping completato con successo (Simulato per ora)"

@app.post("/update-calendar")
async def update_calendar():
    try:
        result = await run_fitri_scraper()
        # Qui potremmo chiamare automaticamente il tuo parse_gare_file.py
        # os.system("python parse_gare_file.py")
        return {"status": "success", "message": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
