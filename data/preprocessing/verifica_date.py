"""
Script de verificare a datelor
Autor: Juncu Vasile
Scop: Verifică ce date avem și dacă sunt valide
"""

import json
import csv
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


RAW_DATA_PATH = os.path.join(BASE_DIR, 'raw_data')
PROCESSED_DATA_PATH = os.path.join(BASE_DIR, 'processed_data')
LOGS_DIR = os.path.join(BASE_DIR, 'logs')


def verifica_json(fisier, nume):
    """Verifică un fișier JSON"""
    try:
        with open(fisier, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✅ {nume}: {len(data)} înregistrări")
        
        # Afișează primele 3 exemple
        print(f"   Primele 3: {[item.get('intrebare', item.get('nume', '?'))[:50] for item in data[:3]]}")
        return len(data)
    except Exception as e:
        print(f"❌ {nume}: Eroare - {e}")
        return 0

def verifica_csv(fisier, nume):
    """Verifică un fișier CSV"""
    try:
        with open(fisier, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        print(f"✅ {nume}: {len(rows)} înregistrări")
        print(f"   Coloane: {list(rows[0].keys()) if rows else 'N/A'}")
        return len(rows)
    except Exception as e:
        print(f"❌ {nume}: Eroare - {e}")
        return 0

def verifica_log(fisier, nume):
    """Verifică un fișier log"""
    try:
        with open(fisier, 'r', encoding='utf-8') as f:
            content = f.read()
            data = json.loads(content)
        print(f"✅ {nume}: {len(data)} conversații")
        return len(data)
    except Exception as e:
        print(f"❌ {nume}: Eroare - {e}")
        return 0

def main():
    print("=" * 60)
    print("📊 RAPORT DE VERIFICARE DATE - JUNCU VASILE")
    print("=" * 60)
    
    # Contor total
    total = 0
    
    # Verifică fișierele RAW
    print("\n📁 FIȘIERE RAW (date brute):")
    print("-" * 40)
    
    total += verifica_json(os.path.join(RAW_DATA_PATH, 'intrebari_culinare.json'), 'Întrebări culinare')
    total += verifica_json(os.path.join(RAW_DATA_PATH, 'retete_complete.json'), 'Rețete complete')
    total += verifica_log(os.path.join(LOGS_DIR, 'conversatii.log'), 'Conversații')
    
    # Verifică fișierele PROCESATE
    print("\n📁 FIȘIERE PROCESATE (pentru model):")
    print("-" * 40)
    
    total += verifica_csv(os.path.join(PROCESSED_DATA_PATH, 'date_antrenare.csv'), 'Date antrenare')
    total += verifica_json(os.path.join(PROCESSED_DATA_PATH, 'intentii_antrenare.json'), 'Intenții antrenare')
    total += verifica_json(os.path.join(PROCESSED_DATA_PATH, 'scheme_raspuns.json'), 'Scheme răspunsuri')
    
    # Rezumat
    print("\n" + "=" * 60)
    print(f"📊 TOTAL GENERAL: {total} înregistrări")
    print("=" * 60)
    
    # Verifică dacă sunt suficiente date
    if total >= 500:
        print("🎉 EXCELENT! Ai suficiente date pentru antrenare!")
    elif total >= 300:
        print("👍 BINE! Mai poți adăuga câteva date pentru a fi excelent.")
    else:
        print("⚠️ ATENȚIE! Ai nevoie de mai multe date. Adaugă 100-200 întrebări.")
    
    print("\n✅ Verificare completă!")

if __name__ == "__main__":
    main()