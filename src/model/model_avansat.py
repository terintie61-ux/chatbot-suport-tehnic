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

def incarca_date():
    """Încarcă datele de antrenare"""
    df = pd.read_csv('data/processed/date_antrenare.csv')
    print(f"📖 Am încărcat {len(df)} exemple")
    return df

def antreneaza_model_svm():
    """Antrenează model SVM"""
    print("\n" + "=" * 60)
    print("🤖 ANTRENARE MODEL AVANSAT - TF-IDF + SVM")
    print("=" * 60)
    
    # Încarcă datele
    df = incarca_date()
    
    # Separă datele
    X = df['intrebare'].values
    y = df['intentie'].values
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Creează pipeline-ul
    model = make_pipeline(
        TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 2),
            lowercase=True,
            stop_words='english'
        ),
        SVC(
            kernel='linear',      # kernel liniar
            C=1.0,                # parametru de regularizare
            probability=True,     # pentru a obține probabilități
            random_state=42
        )
    )
    
    # Antrenează
    print("\n🏋️ Antrenez modelul SVM...")
    model.fit(X_train, y_train)
    
    # Evaluare
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\n📊 Acuratețe: {accuracy:.4f} ({accuracy*100:.2f}%)")
    print("\n📋 Raport detaliat:")
    print(classification_report(y_test, y_pred))
    
    # Cross-validation
    print("\n🔄 Cross-validation (5 folds):")
    cv_scores = cross_val_score(model, X, y, cv=5)
    print(f"   Scoruri: {cv_scores}")
    print(f"   Medie: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
    
    # Matrice de confuzie
    plot_confusion_matrix(y_test, y_pred, model.classes_)
    
    # Salvează modelul
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_path = f'models/saved/model_svm_{timestamp}.pkl'
    joblib.dump(model, model_path)
    
    # Salvează informații
    model_info = {
        "versiune": "2.0",
        "tip": "TF-IDF + SVM",
        "data_antrenare": timestamp,
        "acuratete": float(accuracy),
        "cv_score_mean": float(cv_scores.mean()),
        "cv_score_std": float(cv_scores.std()),
        "numar_exemple": len(df),
        "intentii": list(model.classes_),
        "model_path": model_path
    }
    
    with open('models/saved/model_info_svm.json', 'w', encoding='utf-8') as f:
        json.dump(model_info, f, ensure_ascii=False, indent=2)
    
    return model, model_path

def plot_confusion_matrix(y_test, y_pred, classes):
    """Plotează matricea de confuzie"""
    cm = confusion_matrix(y_test, y_pred)
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=classes, yticklabels=classes)
    plt.title('Matrice de Confuzie - Model SVM')
    plt.xlabel('Predicție')
    plt.ylabel('Real')
    plt.tight_layout()
    plt.savefig('models/saved/confusion_matrix.png')
    plt.show()
    print("\n📊 Matricea de confuzie a fost salvată în models/saved/confusion_matrix.png")

def compara_modele():
    """Compară modelul simplu cu cel avansat"""
    print("\n" + "=" * 60)
    print("📊 COMPARAȚIE MODELE")
    print("=" * 60)
    
    # Citește informațiile modelelor
    try:
        with open('models/saved/model_info.json', 'r') as f:
            info_simplu = json.load(f)
        print(f"\n✅ Model simplu (Naive Bayes):")
        print(f"   Acuratețe: {info_simplu['acuratete']*100:.2f}%")
    except:
        print("\n❌ Modelul simplu nu a fost găsit. Rulează mai întâi model_simplu.py")
    
    try:
        with open('models/saved/model_info_svm.json', 'r') as f:
            info_svm = json.load(f)
        print(f"\n✅ Model avansat (SVM):")
        print(f"   Acuratețe: {info_svm['acuratete']*100:.2f}%")
        print(f"   Cross-validation: {info_svm['cv_score_mean']*100:.2f}% (+/- {info_svm['cv_score_std']*2*100:.2f}%)")
    except:
        print("\n❌ Modelul avansat nu a fost găsit.")

if __name__ == "__main__":
    model, path = antreneaza_model_svm()
    compara_modele()
    
    print("\n" + "=" * 60)
    print("✅ MODELUL AVANSAT ESTE GATA!")
    print("=" * 60)