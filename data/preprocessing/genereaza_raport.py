"""
Generează un raport frumos pentru Prezentarea 1
Autor: Juncu Vasile
"""

import json
import csv
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


RAW_DATA_PATH = os.path.join(BASE_DIR, 'raw_data')
PROCESSED_DATA_PATH = os.path.join(BASE_DIR, 'processed_data')


def main():
    print("=" * 70)
    print("🍳 RAPORT DATE - CHATBOT CULINAR 'BUCĂTARUL VIRTUAL'")
    print("=" * 70)
    print("\n📊 CE AM COLECTAT:")
    print("-" * 70)
    
    # ========== 1. Citește întrebările ==========
    with open( os.path.join(RAW_DATA_PATH, 'intrebari_culinare.json') , 'r', encoding='utf-8') as f:
        intrebari = json.load(f)
    
    # Numără pe categorii
    categorii = {}
    for item in intrebari:
        cat = item.get('categorie', 'necunoscut')
        categorii[cat] = categorii.get(cat, 0) + 1
    
    print(f"\n✅ {len(intrebari)} întrebări culinare")
    print("\n   Distribuție pe categorii:")
    for cat, count in sorted(categorii.items(), key=lambda x: x[1], reverse=True):
        procent = count / len(intrebari) * 100
        print(f"   • {cat.upper()}: {count} întrebări ({procent:.0f}%)")
    
    # ========== 2. Citește rețetele ==========
    try:
        with open(os.path.join(RAW_DATA_PATH, 'retete_complete.json'), 'r', encoding='utf-8') as f:
            retete_data = json.load(f)
        
        # Verifică structura - poate e dicționar cu cheia "retete"
        if isinstance(retete_data, dict):
            if 'retete' in retete_data:
                retete = retete_data['retete']
            else:
                # Dacă e dicționar cu alte chei, ia valorile
                retete = list(retete_data.values())
                if retete and isinstance(retete[0], dict) and 'nume' not in retete[0]:
                    retete = [retete_data]  # e o singură rețetă
        else:
            retete = retete_data
        
        print(f"\n✅ {len(retete)} rețete complete")
        
        if len(retete) > 0:
            print("\n   Rețete disponibile:")
            for i, ret in enumerate(retete[:10]):
                nume = ret.get('nume', ret.get('nume_reteta', 'Necunoscut'))
                dificultate = ret.get('dificultate', 'N/A')
                print(f"   • {nume} ({dificultate})")
            
            if len(retete) > 10:
                print(f"   ... și încă {len(retete) - 10} rețete")
        else:
            print("   ⚠️ Nu există rețete în fișier!")
            
    except FileNotFoundError:
        print("\n⚠️ Fișierul retete_complete.json nu a fost găsit!")
        retete = []
    except Exception as e:
        print(f"\n⚠️ Eroare la citirea rețetelor: {e}")
        retete = []
    
    # ========== 3. Citește datele de antrenare ==========
    try:
        with open(os.path.join(PROCESSED_DATA_PATH, 'date_antrenare.csv'), 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        intentii = {}
        for row in rows:
            intent = row.get('intentie', 'necunoscut')
            intentii[intent] = intentii.get(intent, 0) + 1
        
        print(f"\n✅ {len(rows)} exemple pentru antrenarea modelului")
        print("\n   Exemple pe intenții:")
        for intent, count in sorted(intentii.items(), key=lambda x: x[1], reverse=True):
            print(f"   • {intent}: {count} exemple")
            
    except FileNotFoundError:
        print("\n⚠️ Fișierul date_antrenare.csv nu a fost găsit!")
        rows = []
        intentii = {}
    
    # ========== 4. Citește statisticile generate ==========
    try:
        with open(os.path.join(PROCESSED_DATA_PATH, 'statistici.json'), 'r', encoding='utf-8') as f:
            stats = json.load(f)
        
        print("\n📈 STATISTICI DIN PROCESARE:")
        print(f"   • Total întrebări: {stats.get('total_intrebari', 0)}")
        if 'intentii' in stats:
            print(f"   • Intenții acoperite: {len(stats['intentii'])}")
            print(f"   • Total exemple: {sum(stats['intentii'].values())}")
    except:
        pass
    
    # ========== 5. Rezumat final ==========
    print("\n" + "=" * 70)
    print("📈 TOTAL GENERAL:")
    print(f"   • {len(intrebari)} întrebări culinare")
    print(f"   • {len(retete)} rețete complete")
    print(f"   • {len(rows)} exemple antrenare")
    print(f"   • {len(intentii)} intenții acoperite")
    print("=" * 70)
    
    # ========== 6. Următorii pași ==========
    print("\n🎯 URMĂTORII PAȘI:")
    print("   1. Maria va antrena modelul cu aceste date")
    print("   2. Dumitru va integra răspunsurile în API")
    print("   3. Debora va conecta frontend-ul")
    print("   4. Toți vom testa integrarea")
    print("=" * 70)
    
    # ========== 7. Verificare calitate ==========
    print("\n✅ VERIFICARE CALITATE DATE:")
    
    if len(intrebari) >= 100:
        print("   ✅ SUFICIENTE întrebări (100+)")
    else:
        print(f"   ⚠️ DOAR {len(intrebari)} întrebări - mai adaugă!")
    
    if len(rows) >= 300:
        print("   ✅ SUFICIENTE exemple antrenare (300+)")
    else:
        print(f"   ⚠️ DOAR {len(rows)} exemple - mai adaugă!")
    
    if len(intentii) >= 7:
        print("   ✅ SUFICIENTE intenții acoperite (7+)")
    else:
        print(f"   ⚠️ DOAR {len(intentii)} intenții - extinde!")
    
    print("\n🎉 RAPORT GENERAT CU SUCCES!")

if __name__ == "__main__":
    main()