"""
Script de preprocesare text pentru întrebări culinare
Autor: Juncu Vasile
Scop: Curăță textul pentru a fi folosit la antrenarea modelului
"""

import re
import json
import csv
from datetime import datetime

def curata_text(text):
    """
    Curăță textul:
    - litere mici
    - elimină semne de punctuație
    - elimină diacritice simple
    - elimină spații multiple
    """
    # Transformă în litere mici
    text = text.lower()
    
    # Înlocuiește diacritice simple
    diacritice = {
        'ă': 'a', 'â': 'a', 'î': 'i', 'ș': 's', 'ț': 't',
        'Ă': 'a', 'Â': 'a', 'Î': 'i', 'Ș': 's', 'Ț': 't'
    }
    for diac, reg in diacritice.items():
        text = text.replace(diac, reg)
    
    # Elimină semnele de punctuație (păstrează litere, cifre, spații)
    text = re.sub(r'[^\w\s]', '', text)
    
    # Elimină cifrele (dacă nu sunt relevante)
    text = re.sub(r'\d+', '', text)
    
    # Elimină spațiile multiple
    text = re.sub(r'\s+', ' ', text)
    
    # Elimină spațiile de la început și sfârșit
    return text.strip()

def preproceseaza_intrebari_json(input_file, output_file):
    """
    Preprocesează întrebările din JSON
    """
    print(f"📖 Procesez: {input_file}")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for item in data:
        if 'intrebare' in item:
            item['intrebare_curatata'] = curata_text(item['intrebare'])
        if 'raspuns' in item:
            # Scurtăm răspunsul pentru statistici
            item['raspuns_scurt'] = item['raspuns'][:100] + "..." if len(item['raspuns']) > 100 else item['raspuns']
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Salvate în: {output_file}")
    return len(data)

def preproceseaza_date_antrenare(input_file, output_file):
    """
    Preprocesează fișierul CSV de antrenare
    """
    print(f"📖 Procesez: {input_file}")
    
    rows_processed = []
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if 'intrebare' in row:
                row['intrebare_curatata'] = curata_text(row['intrebare'])
            rows_processed.append(row)
    
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        if rows_processed:
            writer = csv.DictWriter(f, fieldnames=rows_processed[0].keys())
            writer.writeheader()
            writer.writerows(rows_processed)
    
    print(f"✅ Salvate în: {output_file}")
    return len(rows_processed)

def genereaza_statistici():
    """
    Generează statistici despre date
    """
    stats = {
        "data_generare": datetime.now().isoformat(),
        "total_intrebari": 0,
        "categorii": {},
        "preparate": {},
        "intentii": {}
    }
    
    # Statistici din intrebari_culinare.json
    try:
        with open('data/raw/intrebari_culinare.json', 'r', encoding='utf-8') as f:
            intrebari = json.load(f)
            stats["total_intrebari"] = len(intrebari)
            
            for item in intrebari:
                cat = item.get('categorie', 'necunoscut')
                stats["categorii"][cat] = stats["categorii"].get(cat, 0) + 1
                
                prep = item.get('preparat', 'general')
                stats["preparate"][prep] = stats["preparate"].get(prep, 0) + 1
    except Exception as e:
        print(f"Eroare la citirea statisticilor: {e}")
    
    # Statistici din date_antrenare.csv
    try:
        with open('data/processed/date_antrenare.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                intent = row.get('intentie', 'necunoscut')
                stats["intentii"][intent] = stats["intentii"].get(intent, 0) + 1
    except Exception as e:
        print(f"Eroare la citirea statisticilor CSV: {e}")
    
    # Salvează statisticile
    with open('data/processed/statistici.json', 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    
    print(f"\n📊 STATISTICI:")
    print(f"   Total întrebări: {stats['total_intrebari']}")
    print(f"   Categorii: {dict(list(stats['categorii'].items())[:5])}")
    print(f"   Intenții: {stats['intentii']}")
    
    return stats

def main():
    print("=" * 60)
    print("🧹 PREPROCESARE DATE - JUNCU VASILE")
    print("=" * 60)
    
    # 1. Preprocesează întrebările
    print("\n1. Preprocesare întrebări...")
    preproceseaza_intrebari_json(
        'data/raw/intrebari_culinare.json',
        'data/processed/intrebari_curatate.json'
    )
    
    # 2. Preprocesează datele de antrenare
    print("\n2. Preprocesare date antrenare...")
    preproceseaza_date_antrenare(
        'data/processed/date_antrenare.csv',
        'data/processed/date_antrenare_curatate.csv'
    )
    
    # 3. Generează statistici
    print("\n3. Generare statistici...")
    genereaza_statistici()
    
    print("\n" + "=" * 60)
    print("✅ PREPROCESARE COMPLETĂ!")
    print("=" * 60)
    print("\n📁 Fișiere create:")
    print("   - data/processed/intrebari_curatate.json")
    print("   - data/processed/date_antrenare_curatate.csv")
    print("   - data/processed/statistici.json")

if __name__ == "__main__":
    main()