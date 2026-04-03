"""
Verifică datele de antrenare
Autor: Carai Maria
"""

import pandas as pd
import json

print("=" * 60)
print("📊 VERIFICARE DATE ANTRENARE")
print("=" * 60)

# 1. Încarcă datele din CSV
df = pd.read_csv('data/processed/date_antrenare.csv')
print(f"\n✅ Am încărcat {len(df)} exemple de antrenare")
print(f"\n📋 Coloane disponibile: {list(df.columns)}")

# 2. Vezi distribuția pe intenții
print("\n📊 Distribuție pe intenții:")
intentii_counts = df['intentie'].value_counts()
for intent, count in intentii_counts.items():
    print(f"   • {intent}: {count} exemple")

# 3. Vezi câte preparate diferite sunt
print(f"\n🍳 Preparate distincte: {df['preparat'].nunique()}")
print(f"   Primele 5: {df['preparat'].value_counts().head().to_dict()}")

# 4. Afișează 3 exemple
print("\n📝 Exemple de antrenare:")
for i in range(min(3, len(df))):
    print(f"\n   Exemplu {i+1}:")
    print(f"   Întrebare: {df.iloc[i]['intrebare'][:80]}...")
    print(f"   Intenție: {df.iloc[i]['intentie']}")
    print(f"   Preparat: {df.iloc[i]['preparat']}")

print("\n" + "=" * 60)
print("✅ Datele sunt gata pentru antrenare!")
print("=" * 60)