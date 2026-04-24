"""
Script de verificare a datelor primite de la Vasile
Autor: Carai Maria
Scop: Verifică ce date avem pentru antrenarea modelului
"""

import pandas as pd
import json
import os

# DATA Directory:
PROJECT_ROOT = os.path.abspath(os.path.join(__file__, "..", "..", ".."))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
RAW_DATA_PATH = os.path.join(DATA_DIR, 'raw_data')
PROCESSED_DATA_PATH = os.path.join(DATA_DIR, 'processed_data')


# MODEL Directory:
MODEL_DIR = os.path.abspath(os.path.join(__file__, "..",".."))
SAVE_MODEL_DIR = os.path.join(MODEL_DIR, "saved")


def verifica_datele():
    print("=" * 60)
    print("📊 VERIFICARE DATE PRIMITE DE LA VASILE")
    print("=" * 60)
    
    # 1. Verifică datele de antrenare (CSV)
    print("\n📁 Date antrenare (CSV):")
    try:
        df = pd.read_csv( os.path.join(RAW_DATA_PATH, "date_antrenare.csv") )
        print(f"   ✅ Încărcat: {len(df)} exemple")
        print(f"   📋 Coloane: {list(df.columns)}")
        print(f"   🏷️ Intenții unice: {df['intentie'].unique()}")
        print(f"\n   Distribuție pe intenții:")
        for intent, count in df['intentie'].value_counts().items():
            print(f"      • {intent}: {count} exemple")
    except Exception as e:
        print(f"   ❌ Eroare: {e}")
    
    # 2. Verifică întrebările (JSON)
    print("\n📁 Întrebări culinare (JSON):")
    try:
        with open( os.path.join(RAW_DATA_PATH, "intrebari_culinare.json") , 'r', encoding='utf-8') as f:
            intrebari = json.load(f)
        print(f"   ✅ Încărcat: {len(intrebari)} întrebări")
        
        # Categorii
        categorii = {}
        for item in intrebari:
            cat = item.get('categorie', 'necunoscut')
            categorii[cat] = categorii.get(cat, 0) + 1
        print(f"   📂 Categorii: {categorii}")
    except Exception as e:
        print(f"   ❌ Eroare: {e}")
    
    # 3. Verifică intențiile (JSON)
    print("\n📁 Intenții antrenare (JSON):")
    try:
        with open( os.path.join(RAW_DATA_PATH, "intentii_antrenare.json") , 'r', encoding='utf-8') as f:
            intentii = json.load(f)
        print(f"   ✅ Încărcat: {len(intentii['intentii'])} intenții")
        for intent in intentii['intentii'][:5]:
            print(f"      • {intent['nume']}: {len(intent['exemple'])} exemple")
    except Exception as e:
        print(f"   ❌ Eroare: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Verificare completă! Datele sunt gata pentru antrenare.")
    print("=" * 60)

if __name__ == "__main__":
    verifica_datele()