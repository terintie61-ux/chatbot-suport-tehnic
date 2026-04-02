"""
Compară diferite modele de clasificare
Autor: Carai Maria
"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score
from sklearn.pipeline import make_pipeline
import time

def compara_modele():
    print("=" * 60)
    print("📊 COMPARAȚIE MODELE - CARAI MARIA")
    print("=" * 60)
    
    # Încarcă datele
    df = pd.read_csv('data/processed/date_antrenare.csv')
    X = df['intrebare'].values
    y = df['intentie'].values
    
    # Împarte datele
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Definește modelele de testat
    modele = {
        'Naive Bayes': make_pipeline(
            TfidfVectorizer(max_features=5000),
            MultinomialNB()
        ),
        'SVM (Linear)': make_pipeline(
            TfidfVectorizer(max_features=5000),
            SVC(kernel='linear', C=1.0)
        ),
        'Logistic Regression': make_pipeline(
            TfidfVectorizer(max_features=5000),
            LogisticRegression(max_iter=1000)
        ),
        'Random Forest': make_pipeline(
            TfidfVectorizer(max_features=5000),
            RandomForestClassifier(n_estimators=100, random_state=42)
        )
    }
    
    # Testează fiecare model
    rezultate = {}
    
    for nume, model in modele.items():
        print(f"\n🤖 Testez: {nume}")
        
        start_time = time.time()
        
        # Antrenează
        model.fit(X_train, y_train)
        
        # Evaluează
        y_pred = model.predict(X_test)
        acuratete = accuracy_score(y_test, y_pred)
        
        # Cross-validation
        cv_scores = cross_val_score(model, X_train, y_train, cv=5)
        
        end_time = time.time()
        
        rezultate[nume] = {
            'acuratete': acuratete,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std(),
            'timp': end_time - start_time
        }
        
        print(f"   Acuratețe: {acuratete:.2%}")
        print(f"   Cross-val: {cv_scores.mean():.2%} (+/- {cv_scores.std():.2%})")
        print(f"   Timp: {end_time - start_time:.2f} secunde")
    
    # Afișează rezumatul
    print("\n" + "=" * 60)
    print("📊 REZUMAT COMPARAȚIE:")
    print("=" * 60)
    
    df_rezultate = pd.DataFrame(rezultate).T
    df_rezultate = df_rezultate.sort_values('acuratete', ascending=False)
    print(df_rezultate.round(4))
    
    # Recomandare
    cel_mai_bun = df_rezultate.index[0]
    print(f"\n🏆 Cel mai bun model: {cel_mai_bun}")
    print(f"   Acuratețe: {df_rezultate.iloc[0]['acuratete']:.2%}")
    
    return cel_mai_bun

if __name__ == "__main__":
    compara_modele()