import os
import json
from supabase import create_client, Client

def check_sync():
    """
    Confronta il file JSON locale con i dati presenti su Supabase.
    Identifica disallineamenti negli ID e titoli delle gare.
    """
    json_path = 'app/src/races_full.json'
    
    # 1. Carica il JSON locale
    if not os.path.exists(json_path):
        print(f"❌ Errore: File {json_path} non trovato.")
        return
        
    with open(json_path, 'r', encoding='utf-8') as f:
        local_data = json.load(f)
        local_races = {r['id']: r['title'] for r in local_data}

    # 2. Inizializza Supabase (usa variabili d'ambiente)
    url = os.environ.get("SUPABASE_URL", "").strip()
    key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "").strip()

    if not url or not key:
        print("❌ Errore: Variabili d'ambiente SUPABASE_URL o SUPABASE_SERVICE_ROLE_KEY mancanti.")
        print("Assicurati di averle impostate nel tuo terminale.")
        return

    try:
        supabase: Client = create_client(url, key)
        print(f"📡 Connessione a Supabase ({url[:20]}...)")
        
        # 3. Scarica le gare dal DB
        response = supabase.table("races").select("id, title").execute()
        db_races = {r['id']: r['title'] for r in response.data}
        
        # 4. Analisi Differenze
        print("--- ANALISI DISALLINEAMENTI ---")
        
        mismatches = []
        common_ids = set(local_races.keys()) & set(db_races.keys())
        
        # Ordiniamo gli ID numericamente se possibile
        sorted_ids = sorted(common_ids, key=lambda x: int(x) if x.isdigit() else x)
        
        for rid in sorted_ids:
            if local_races[rid] != db_races[rid]:
                mismatches.append((rid, local_races[rid], db_races[rid]))

        if not mismatches:
            print("✅ Tutti gli ID presenti in entrambi i sistemi hanno lo stesso titolo.")
        else:
            print(f"⚠️ Trovati {len(mismatches)} disallineamenti:")
            # Mostriamo i primi 10 per non intasare il terminale
            for rid, loc, db in mismatches[:20]:
                print(f"   ID {rid:4} | LOCALE: {loc[:35]:35} | DB: {db[:35]}")
            if len(mismatches) > 20:
                print(f"   ... e altri {len(mismatches) - 20} errori.")

        # 5. Analisi "Slittamento" (Shift)
        print("--- ANALISI SLITTAMENTO (SHIFT) ---")
        # Proviamo a vedere se l'ID N locale corrisponde all'ID N+1 del DB
        shifts = 0
        for rid in sorted_ids:
            next_id = str(int(rid) + 1) if rid.isdigit() else ""
            if next_id in db_races and local_races[rid] == db_races[next_id]:
                if shifts < 5:
                    print(f"   💡 L'ID locale {rid} ({local_races[rid][:20]}) corrisponde all'ID DB {next_id}")
                shifts += 1
        
        if shifts > 0:
            print(f"   ⚠️ SOSPETTO CONFERMATO: C'è uno slittamento di ID per almeno {shifts} gare.")

        # 6. Statistiche finali
        print("--- STATISTICHE ---")
        print(f"📊 Gare nel JSON locale: {len(local_races)}")
        print(f"📊 Gare nel Database:    {len(db_races)}")
        
        only_local = set(local_races.keys()) - set(db_races.keys())
        only_db = set(db_races.keys()) - set(local_races.keys())
        
        if only_local: print(f"➕ {len(only_local)} ID presenti solo nel JSON locale.")
        if only_db:    print(f"➖ {len(only_db)} ID presenti solo nel Database.")

    except Exception as e:
        print(f"❌ Errore durante l'esecuzione: {e}")

if __name__ == "__main__":
    check_sync()
