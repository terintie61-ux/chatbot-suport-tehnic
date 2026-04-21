"""
Model simplu de clasificare a intențiilor
Autor: Carai Maria
Folosește: TF-IDF + Naive Bayes
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import joblib
import json
from datetime import datetime
import os

# DATA Directory:
PROJECT_ROOT = os.path.abspath(os.path.join(__file__, "..", "..", ".."))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
RAW_DATA_PATH = os.path.join(DATA_DIR, 'raw_data')
PROCESSED_DATA_PATH = os.path.join(DATA_DIR, 'processed_data')

# MODEL Directory:
MODEL_DIR = os.path.abspath(os.path.join(__file__, "..",".."))
SAVE_MODEL_DIR = os.path.join(MODEL_DIR, "saved")



def incarca_date():
    """Încarcă datele de antrenare"""
    print("📖 Încarc datele de antrenare...")
    df = pd.read_csv( os.path.join(RAW_DATA_PATH, "date_antrenare.csv") )
    print(f"   Am încărcat {len(df)} exemple")
    return df

def antreneaza_model():
    """Antrenează modelul de clasificare"""
    print("\n" + "=" * 60)
    print("🤖 ANTRENARE MODEL - CLASIFICARE INTENȚII")
    print("=" * 60)
    
    # 1. Încarcă datele
    df = incarca_date()
    
    # 2. Separă datele în caracteristici (X) și etichete (y)
    X = df['intrebare'].values  # întrebările
    y = df['intentie'].values   # intențiile
    
    # 3. Împarte datele în antrenare (80%) și testare (20%)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"\n📊 Split-ul datelor:")
    print(f"   Antrenare: {len(X_train)} exemple")
    print(f"   Testare: {len(X_test)} exemple")
    
    # 4. Creează pipeline-ul: TF-IDF + Naive Bayes
    model = make_pipeline(
        TfidfVectorizer(
            max_features=5000,      # limitează numărul de cuvinte
            ngram_range=(1, 2),     # folosește unigram și bigram
            lowercase=True,         # transformă în litere mici
            stop_words='english'    # elimină cuvinte comune în engleză
        ),
        MultinomialNB(alpha=0.1)   # Naive Bayes cu smoothing
    )
    
    # 5. Antrenează modelul
    print("\n🏋️ Antrenez modelul...")
    model.fit(X_train, y_train)
    print("   Antrenare completă!")
    
    # 6. Evaluează modelul
    print("\n📊 Evaluare model:")
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"   Acuratețe: {accuracy:.4f} ({accuracy*100:.2f}%)")
    
    print("\n📋 Raport detaliat:")
    print(classification_report(y_test, y_pred))
    
    # 7. Salvează modelul
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_path = os.path.join(SAVE_MODEL_DIR, f"model_v1_{timestamp}.pkl")  
    joblib.dump(model, model_path)
    print(f"\n💾 Model salvat la: {model_path}")
    
    # 8. Salvează și informații despre model
    model_info = {
        "versiune": "1.0",
        "data_antrenare": timestamp,
        "acuratete": float(accuracy),
        "numar_exemple": len(df),
        "numar_intentii": len(df['intentie'].unique()),
        "intentii": list(df['intentie'].unique()),
        "model_path": model_path
    }
    
    with open( os.path.join(SAVE_MODEL_DIR, "model_info.json") , 'w', encoding='utf-8') as f:
        json.dump(model_info, f, ensure_ascii=False, indent=2)
    
    print(f"📄 Informații model salvate în: models/saved/model_info.json")
    
    return model, model_path

def testeaza_model(model):
    """Testează modelul cu întrebări noi"""
    print("\n" + "=" * 60)
    print("🧪 TESTARE MODEL CU ÎNTREBĂRI NOI")
    print("=" * 60)
    
    # Întrebări de test
    intrebari_test = [
        "Cum se face pizza acasă?",
        "Cât timp se coace cozonacul?",
        "Ce ingrediente pentru sarmale?",
        "Cu ce înlocuiesc ouăle în prăjituri?",
        "E greu de făcut mămăligă?",
        "Salut, ce faci?",
        "Mulțumesc pentru ajutor!",
        "Câte ouă se pun în chec?",
        "La ce temperatură se coace puiul?",
        "Cum fac piure de cartofi?"
    ]
    
    print("\n📝 Testează modelul:")
    for intrebare in intrebari_test:
        intentie = model.predict([intrebare])[0]
        probabilitati = model.predict_proba([intrebare])[0]
        confidenta = max(probabilitati)
        
        print(f"\n   ❓ {intrebare}")
        print(f"   🎯 Intenție: {intentie} (confidență: {confidenta:.2f})")

if __name__ == "__main__":
    model, path = antreneaza_model()
    testeaza_model(model)
    
    print("\n" + "=" * 60)
    print("✅ MODELUL ESTE GATA DE FOLOSIT!")
    print("=" * 60)