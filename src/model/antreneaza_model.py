"""
Model avansat - TF-IDF + SVM (Support Vector Machine)
Autor: Carai Maria
Performanță mai bună decât Naive Bayes
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import joblib
import json
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os
import warnings
warnings.filterwarnings('ignore')

# ==================== CONFIGURARE CĂI ====================

# Detectează automat rădăcina proiectului
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")

# Căi corecte pentru fișiere
RAW_DATA_PATH = os.path.join(DATA_DIR, 'raw')           # Date brute (JSON-uri)
PROCESSED_DATA_PATH = os.path.join(DATA_DIR, 'processed')  # Date procesate (CSV)

# Director pentru model
MODEL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "models"))
SAVE_MODEL_DIR = os.path.join(MODEL_DIR, "saved")

# Creează directorul dacă nu există
os.makedirs(SAVE_MODEL_DIR, exist_ok=True)

# ==================== FUNCȚII ====================

def incarca_date():
    """Încarcă datele de antrenare din fișierul CSV"""
    csv_path = os.path.join(PROCESSED_DATA_PATH, "date_antrenare.csv")
    
    if not os.path.exists(csv_path):
        print(f"❌ Fișierul nu a fost găsit: {csv_path}")
        print("   Verifică structura folderelor:")
        print(f"   - Există folderul 'data/processed'?")
        print(f"   - Există fișierul 'date_antrenare.csv'?")
        return None
    
    df = pd.read_csv(csv_path)
    print(f"📖 Am încărcat {len(df)} exemple din {csv_path}")
    print(f"   Intenții disponibile: {df['intentie'].unique()}")
    return df

def antreneaza_model_svm():
    """Antrenează modelul SVM cu TF-IDF"""
    print("\n" + "=" * 60)
    print("🤖 ANTRENARE MODEL AVANSAT - TF-IDF + SVM")
    print("=" * 60)
    
    # Încarcă datele
    df = incarca_date()
    if df is None:
        return None, None
    
    # Separă datele
    X = df['intrebare'].values
    y = df['intentie'].values
    
    print(f"\n📊 Distribuție intenții:")
    for intent, count in df['intentie'].value_counts().items():
        print(f"   {intent}: {count} exemple")
    
    # Split (80% antrenare, 20% testare)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"\n📚 Antrenare: {len(X_train)} exemple")
    print(f"🧪 Testare: {len(X_test)} exemple")
    
    # Creează pipeline-ul
    model = make_pipeline(
        TfidfVectorizer(
            max_features=5000,      # limitează numărul de cuvinte
            ngram_range=(1, 2),     # folosește cuvinte individuale și perechi
            lowercase=True,          # transformă în litere mici
            stop_words='english'     # elimină cuvinte comune în engleză
        ),
        SVC(
            kernel='linear',         # kernel liniar (bun pentru text)
            C=1.0,                   # parametru de regularizare
            probability=True,        # pentru a obține probabilități
            random_state=42
        )
    )
    
    # Antrenează
    print("\n🏋️ Antrenez modelul SVM...")
    model.fit(X_train, y_train)
    
    # Evaluare pe setul de test
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\n📊 Acuratețe pe setul de test: {accuracy:.4f} ({accuracy*100:.2f}%)")
    print("\n📋 Raport detaliat de clasificare:")
    print(classification_report(y_test, y_pred))
    
    # Cross-validation (opțional, durează mai mult)
    print("\n🔄 Cross-validation (5 folds)...")
    cv_scores = cross_val_score(model, X, y, cv=5)
    print(f"   Scoruri individuale: {cv_scores}")
    print(f"   Medie: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
    
    # Matrice de confuzie
    plot_confusion_matrix(y_test, y_pred, model.classes_)
    
    # Salvează modelul
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_path = os.path.join(SAVE_MODEL_DIR, f'model_svm.pkl')
    joblib.dump(model, model_path)
    print(f"\n💾 Model salvat: {model_path}")
    
    # Salvează și o copie ca "model_latest.pkl" pentru API
    latest_path = os.path.join(SAVE_MODEL_DIR, 'model_latest.pkl')
    joblib.dump(model, latest_path)
    print(f"💾 Copie salvată: {latest_path} (pentru API)")
    
    # Salvează informațiile modelului
    model_info = {
        "versiune": "2.0",
        "tip": "TF-IDF + SVM (Linear)",
        "data_antrenare": timestamp,
        "acuratete": float(accuracy),
        "cv_score_mean": float(cv_scores.mean()),
        "cv_score_std": float(cv_scores.std()),
        "numar_exemple": len(df),
        "numar_intentii": len(model.classes_),
        "intentii": list(model.classes_),
        "model_path": model_path
    }
    
    info_path = os.path.join(SAVE_MODEL_DIR, 'model_info_svm.json')
    with open(info_path, 'w', encoding='utf-8') as f:
        json.dump(model_info, f, ensure_ascii=False, indent=2)
    print(f"💾 Informații salvate: {info_path}")
    
    return model, model_path

def plot_confusion_matrix(y_test, y_pred, classes):
    """Plotează și salvează matricea de confuzie"""
    cm = confusion_matrix(y_test, y_pred)
    
    plt.figure(figsize=(12, 10))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=classes, yticklabels=classes)
    plt.title('Matrice de Confuzie - Model SVM', fontsize=14)
    plt.xlabel('Predicție', fontsize=12)
    plt.ylabel('Real', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    
    # Salvează imaginea
    img_path = os.path.join(SAVE_MODEL_DIR, 'confusion_matrix_svm.png')
    plt.savefig(img_path, dpi=150)
    print(f"\n📊 Matricea de confuzie salvată: {img_path}")
    plt.close()  # Închide figura ca să nu blocheze execuția

def compara_modele():
    """Compară modelul simplu cu cel avansat"""
    print("\n" + "=" * 60)
    print("📊 COMPARAȚIE MODELE")
    print("=" * 60)
    
    # Citește informațiile modelului simplu (Naive Bayes)
    info_simplu_path = os.path.join(SAVE_MODEL_DIR, 'model_info.json')
    if os.path.exists(info_simplu_path):
        with open(info_simplu_path, 'r') as f:
            info_simplu = json.load(f)
        print(f"\n✅ Model simplu (Naive Bayes):")
        print(f"   Acuratețe: {info_simplu.get('acuratete', 0)*100:.2f}%")
    else:
        print("\n⚠️ Modelul simplu nu a fost găsit. Rulează mai întâi model_simplu.py")
    
    # Citește informațiile modelului avansat (SVM)
    info_svm_path = os.path.join(SAVE_MODEL_DIR, 'model_info_svm.json')
    if os.path.exists(info_svm_path):
        with open(info_svm_path, 'r') as f:
            info_svm = json.load(f)
        print(f"\n✅ Model avansat (SVM):")
        print(f"   Acuratețe: {info_svm['acuratete']*100:.2f}%")
        print(f"   Cross-validation: {info_svm['cv_score_mean']*100:.2f}% (+/- {info_svm['cv_score_std']*2*100:.2f}%)")
    else:
        print("\n⚠️ Modelul avansat tocmai a fost creat, dar informațiile nu sunt încă disponibile.")

def testeaza_model_cu_exemple_noi(model_path=None):
    """Testează modelul cu exemple noi"""
    if model_path is None:
        model_path = os.path.join(SAVE_MODEL_DIR, 'model_latest.pkl')
    
    if not os.path.exists(model_path):
        print(f"❌ Modelul nu există la: {model_path}")
        return
    
    model = joblib.load(model_path)
    print("\n" + "=" * 60)
    print("🧪 TESTARE MODEL CU EXEMPLE NOI")
    print("=" * 60)
    
    exemple_noi = [
        "Cum se face pizza acasă?",
        "Cât timp se coace cozonacul?",
        "Ce ingrediente pentru sarmale?",
        "Cu ce înlocuiesc ouăle în prăjituri?",
        "E greu de făcut clătite?",
        "Salut, ce faci?",
        "Mulțumesc pentru ajutor!",
        "Vreau o rețetă de ciorbă",
        "Cum prepar paste carbonara?",
        "Cât durează să fac un tort?"
    ]
    
    for exemplu in exemple_noi:
        intentie = model.predict([exemplu])[0]
        # Obține probabilitatea (doar dacă modelul are probability=True)
        try:
            proba = model.predict_proba([exemplu])[0]
            confidenta = max(proba)
            print(f"   📝 '{exemplu}' → {intentie} (confidență: {confidenta:.2%})")
        except:
            print(f"   📝 '{exemplu}' → {intentie}")

# ==================== MAIN ====================

if __name__ == "__main__":
    # Verifică structura folderelor
    print("\n🔍 Verific structura proiectului:")
    print(f"   Rădăcină proiect: {PROJECT_ROOT}")
    print(f"   Director date: {DATA_DIR}")
    print(f"   Director raw: {RAW_DATA_PATH}")
    print(f"   Director processed: {PROCESSED_DATA_PATH}")
    print(f"   Director model: {SAVE_MODEL_DIR}")
    
    # Verifică dacă există fișierul CSV
    csv_path = os.path.join(PROCESSED_DATA_PATH, "date_antrenare.csv")
    if os.path.exists(csv_path):
        print(f"   ✅ Fișierul CSV există: {csv_path}")
    else:
        print(f"   ❌ Fișierul CSV NU există: {csv_path}")
        print("\n   Soluție: Asigură-te că Vasile a încărcat datele în branch-ul lui")
        print("   și că ai făcut 'git pull origin feature/data-preprocessing'")
    
    # Antrenează modelul
    model, path = antreneaza_model_svm()
    
    if model:
        # Compară modelele
        compara_modele()
        
        # Testează modelul
        testeaza_model_cu_exemple_noi()
        
        print("\n" + "=" * 60)
        print("✅ MODELUL AVANSAT ESTE GATA!")
        print("=" * 60)
        print("\n📁 Fișiere create:")
        print(f"   - {SAVE_MODEL_DIR}/model_svm_[timestamp].pkl")
        print(f"   - {SAVE_MODEL_DIR}/model_latest.pkl")
        print(f"   - {SAVE_MODEL_DIR}/model_info_svm.json")
        print(f"   - {SAVE_MODEL_DIR}/confusion_matrix_svm.png")
        print("\n🔗 API-ul lui Dumitru poate folosi: models/saved/model_latest.pkl")
    else:
        print("\n❌ Antrenarea a eșuat. Verifică fișierele și rulează din nou.")