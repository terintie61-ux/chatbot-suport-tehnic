import os

print("=" * 50)
print("Verificare date antrenare")
print("=" * 50)

# Lista de fișiere de verificat
fisiere = [
    "data/raw/intrebari_culinare.json",
    "data/raw/retete_complete.json", 
    "data/processed/date_antrenare.csv",
    "data/processed/intentii_antrenare.json"
]

for fisier in fisiere:
    if os.path.exists(fisier):
        print(f"✅ {fisier} - EXISTĂ")
    else:
        print(f"❌ {fisier} - NU EXISTĂ")

print("=" * 50)