import os
import json
from supabase import create_client, Client

def sync_db_to_json():
    """
    Scarica tutte le gare presenti su Supabase e sovrascrive il file JSON locale.
    Questo serve come fix rapido per allineare l'App al Database senza cambiare gli ID.
    """
    url = os.environ.get("SUPABASE_URL", "").strip()
    key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "").strip()

    if not url or not key:
        print("❌ Errore: Variabili d'ambiente SUPABASE_URL o SUPABASE_SERVICE_ROLE_KEY mancanti.")
        return

    try:
        supabase: Client = create_client(url, key)
        print(f"📡 Connessione a Supabase per il download dei dati...")
        
        # Recuperiamo tutte le gare dal DB
        response = supabase.table("races").select("*").execute()
        
        if not response.data:
            print("⚠️ Nessuna gara trovata nel database.")
            return

        # Ordiniamo i dati per ID numerico per mantenere la coerenza nel JSON
        sorted_data = sorted(
            response.data, 
            key=lambda x: int(x['id']) if str(x['id']).isdigit() else x['id']
        )
        
        json_path = 'app/src/races_full.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(sorted_data, f, ensure_ascii=False, indent=2)
            
        print(f"✅ SINCRO COMPLETATA! Scaricate {len(sorted_data)} gare.")
        print(f"📂 File aggiornato: {json_path}")
        print("\nPROSSIMI PASSI:")
        print("1. Fai il Push su GitHub per aggiornare l'App online.")
        print("2. NON lanciare 'upload_data.py' o 'parse_gare_file.py' per ora.")

    except Exception as e:
        print(f"❌ Errore durante la sincronizzazione: {e}")

if __name__ == "__main__":
    sync_db_to_json()
