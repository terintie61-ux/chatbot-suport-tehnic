"""
Model de clasificare a intențiilor pentru Chatbot Culinar
Autor: Carai Maria
Data: 2024

Folosește:
- TF-IDF pentru vectorizare
- SVM (Support Vector Machine) pentru clasificare
"""

import pandas as pd
import numpy as np
import json
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.pipeline import make_pipeline
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

def incarca_date():
    """Încarcă datele de antrenare de la Vasile"""
    print("📖 Încarc datele de la Vasile...")
    
    # Încarcă CSV-ul
    df = pd.read_csv('data/processed/date_antrenare.csv')
    
    # Curăță datele (elimină rândurile cu valori lipsă)
    df = df.dropna(subset=['intrebare', 'intentie'])
    
    print(f"   ✅ Încărcat {len(df)} exemple valide")
    print(f"   🏷️ Intenții: {df['intentie'].unique()}")
    
    return df

def antreneaza_model(df):
    """Antrenează modelul SVM cu TF-IDF"""
    print("\n🤖 Antrenez modelul...")
    
    # Separă caracteristicile (X) și etichetele (y)
    X = df['intrebare'].values
    y = df['intentie'].values
    
    # Împarte în date de antrenare (80%) și test (20%)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"   📚 Antrenare: {len(X_train)} exemple")
    print(f"   🧪 Test: {len(X_test)} exemple")
    
    # Creează pipeline-ul: TF-IDF + SVM
    model = make_pipeline(
        TfidfVectorizer(
            max_features=5000,      # limitează numărul de cuvinte
            ngram_range=(1, 2),     # folosește și perechi de cuvinte
            stop_words='english'     # elimină cuvinte comune în engleză
        ),
        SVC(kernel='linear', C=1.0, random_state=42)
    )
    
    # Antrenează modelul
    model.fit(X_train, y_train)
    
    # Evaluează pe setul de test
    y_pred = model.predict(X_test)
    acuratete = accuracy_score(y_test, y_pred)
    
    print(f"\n   📊 Acuratețe pe test: {acuratete:.2%}")
    
    # Afișează raportul detaliat
    print("\n   📋 Raport clasificare:")
    print(classification_report(y_test, y_pred))
    
    return model, X_test, y_test, y_pred

def vizualizeaza_rezultate(y_test, y_pred, X_test, model):
    """Creează vizualizări pentru evaluare"""
    print("\n📊 Generez vizualizări...")
    
    # Matrice de confuzie
    plt.figure(figsize=(10, 8))
    cm = confusion_matrix(y_test, y_pred)
    
    # Obține etichetele unice
    labels = sorted(set(y_test))
    
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=labels, yticklabels=labels)
    plt.title('Matrice de Confuzie - Model Intenții Culinare')
    plt.xlabel('Predicție')
    plt.ylabel('Real')
    plt.tight_layout()
    
    # Salvează imaginea
    plt.savefig('models/matrice_confuzie.png', dpi=150)
    print("   ✅ Salvat: models/matrice_confuzie.png")
    
    # Afișează câteva predicții greșite
    print("\n   🔍 Exemple de predicții greșite:")
    errors = 0
    for i in range(len(y_test)):
        if y_test[i] != y_pred[i] and errors < 5:
            print(f"      Real: '{y_test[i]}' → Model: '{y_pred[i]}'")
            if i < len(X_test):
                print(f"         Text: '{X_test[i][:100]}...'")
            errors += 1
    
    # Dacă nu sunt erori
    if errors == 0:
        print("      Niciun exemplu greșit! Modelul este perfect pe setul de test! 🎉")

def salveaza_model(model):
    """Salvează modelul antrenat pentru a fi folosit de API"""
    print("\n💾 Salvez modelul...")
    
    # Creează numele fișierului cu data
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nume_fisier = f'models/saved/model_v1_{timestamp}.pkl'
    
    # Salvează modelul
    joblib.dump(model, nume_fisier)
    print(f"   ✅ Model salvat: {nume_fisier}")
    
    # Salvează și o copie ca "model_latest.pkl" pentru API
    joblib.dump(model, 'models/saved/model_latest.pkl')
    print(f"   ✅ Copie salvată: models/saved/model_latest.pkl (pentru API)")
    
    return nume_fisier

def testeaza_model_cu_exemple(model):
    """Testează modelul cu exemple noi"""
    print("\n🧪 Testez modelul cu exemple noi:")
    
    exemple_noi = [
        "Cum se face pizza acasă?",
        "Cât timp se coace cozonacul?",
        "Ce ingrediente pentru sarmale?",
        "Cu ce înlocuiesc ouăle în prăjituri?",
        "E greu de făcut clătite?",
        "Salut, ce faci?",
        "Mulțumesc pentru ajutor!"
    ]
    
    for exemplu in exemple_noi:
        predictie = model.predict([exemplu])[0]
        # Obține și probabilitatea (pentru SVM linear putem folosi decision_function)
        try:
            scor = model.decision_function([exemplu])
            confidenta = max(scor[0]) if len(scor[0]) > 0 else 0
        except:
            confidenta = "N/A"
        
        print(f"   📝 '{exemplu}'")
        print(f"      → Intenție: {predictie}")
        print(f"      → Confidență: {confidenta if confidenta != 'N/A' else 'calculată'}")

def main():
    print("=" * 60)
    print("🤖 ANTREANARE MODEL - CARAI MARIA")
    print("=" * 60)
    
    # 1. Încarcă datele
    df = incarca_date()
    
    # 2. Antrenează modelul
    model, X_test, y_test, y_pred = antreneaza_model(df)
    
    # 3. Vizualizează rezultatele
    vizualizeaza_rezultate(y_test, y_pred, model)
    
    # 4. Salvează modelul
    nume_model = salveaza_model(model)
    
    # 5. Testează cu exemple noi
    testeaza_model_cu_exemple(model)
    
    print("\n" + "=" * 60)
    print("✅ ANTREANARE COMPLETĂ!")
    print("=" * 60)
    print(f"\n📁 Model salvat în: {nume_model}")
    print("🔗 API-ul lui Dumitru poate folosi: models/saved/model_latest.pkl")
    print("\n🎯 Următorul pas: Integrează modelul în API-ul lui Dumitru!")

if __name__ == "__main__":
    main()