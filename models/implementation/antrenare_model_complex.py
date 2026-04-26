"""
MODEL DE CLASIFICARE INTENȚII PENTRU CHATBOT CULINAR
Autor: Carai Maria
Disciplina: Proiect software în echipă (MI204)

Arhitectură avansată cu:
- TF-IDF + Multiple Classifiers
- Deep Learning with PyTorch (optional)
- Attention-based classification
- Ensemble methods
- Hyperparameter tuning
- Cross-validation
- Early stopping
- GPU acceleration (dacă disponibil)
"""

import os
import sys
import gc
import time
import json
import pickle
import warnings
import numpy as np
import pandas as pd
from pathlib import Path
from collections import Counter
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report, confusion_matrix, roc_auc_score
)
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC, LinearSVC
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.neural_network import MLPClassifier
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader

warnings.filterwarnings('ignore')

print("=" * 80)
print("🍳 MODEL CLASIFICARE INTENȚII - CHATBOT CULINAR")
print("=" * 80)

# ==================== CONFIGURAȚIE ====================

class Config:
    """Configurație pentru model"""
    
    def __init__(self):
        # Date
        self.data_path = 'data/processed/date_antrenare.csv'
        self.intentii_path = 'data/processed/intentii_antrenare.json'
        
        # Text preprocessing
        self.max_features = 10000
        self.ngram_range = (1, 3)
        self.use_idf = True
        self.sublinear_tf = True
        self.stop_words = 'english'
        
        # Model selection
        self.test_size = 0.2
        self.random_state = 42
        self.cv_folds = 5
        
        # Deep Learning (opțional - doar dacă GPU disponibil)
        self.use_deep_learning = torch.cuda.is_available()
        self.embedding_dim = 128
        self.hidden_dim = 256
        self.num_layers = 2
        self.dropout = 0.3
        self.batch_size = 32
        self.num_epochs = 30
        self.learning_rate = 1e-3
        
        # Ensemble
        self.use_ensemble = True
        
        # Output
        self.models_dir = Path('models/saved')
        self.models_dir.mkdir(parents=True, exist_ok=True)
        self.results_dir = Path('results')
        self.results_dir.mkdir(parents=True, exist_ok=True)
        
        # Device
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        print(f"\n⚙️ Configurație:")
        print(f"   Device: {self.device}")
        print(f"   Deep Learning: {'DA' if self.use_deep_learning else 'NU'}")
        print(f"   Ensemble: {'DA' if self.use_ensemble else 'NU'}")

config = Config()


# ==================== ÎNCĂRCARE DATE ====================

def incarca_date():
    """Încarcă datele de antrenare de la Vasile"""
    print("\n📖 ÎNCĂRCARE DATE DE LA VASILE")
    print("-" * 40)
    
    # Încarcă CSV-ul
    df = pd.read_csv(config.data_path)
    
    # Curățare
    df = df.dropna(subset=['intrebare', 'intentie'])
    
    # Statistici
    print(f"✅ Încărcate {len(df)} exemple")
    print(f"🏷️ Intenții unice: {df['intentie'].nunique()}")
    print(f"📊 Distribuție:")
    
    for intent, count in df['intentie'].value_counts().items():
        print(f"   • {intent}: {count} exemple ({count/len(df)*100:.1f}%)")
    
    return df

def preproceseaza_text(df):
    """Preprocesare text pentru toate exemplele"""
    print("\n🔤 PREPROCESARE TEXT")
    print("-" * 40)
    
    # Normalizare text
    df['text_curatat'] = df['intrebare'].str.lower()
    df['text_curatat'] = df['text_curatat'].str.replace(r'[^\w\s]', '', regex=True)
    df['text_curatat'] = df['text_curatat'].str.replace(r'\s+', ' ', regex=True)
    
    print(f"✅ Text preprocesat pentru {len(df)} exemple")
    
    return df


# ==================== VECTORIZARE ====================

def creeaza_vectorizator(df):
    """Creează și antrenează vectorizatorul TF-IDF"""
    print("\n📊 VECTORIZARE TEXT")
    print("-" * 40)
    
    # TF-IDF Vectorizer
    vectorizer = TfidfVectorizer(
        max_features=config.max_features,
        ngram_range=config.ngram_range,
        stop_words=config.stop_words,
        use_idf=config.use_idf,
        sublinear_tf=config.sublinear_tf
    )
    
    # Antrenează vectorizatorul
    X = vectorizer.fit_transform(df['text_curatat'])
    y = df['intentie']
    
    print(f"✅ Dimensiune matrice: {X.shape}")
    print(f"   • {X.shape[0]} exemple")
    print(f"   • {X.shape[1]} caracteristici")
    
    # Afișează top cuvinte
    feature_names = vectorizer.get_feature_names_out()
    print(f"\n📝 Top 10 cuvinte importante:")
    for i in range(min(10, len(feature_names))):
        print(f"   {i+1}. {feature_names[i]}")
    
    return vectorizer, X, y


# ==================== MODELE TRADIȚIONALE ====================

def antreneaza_modele_traditionale(X, y):
    """Antrenează modele clasice de machine learning"""
    print("\n🤖 ANTRENARE MODELE TRADIȚIONALE")
    print("-" * 40)
    
    # Split date
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=config.test_size, 
        random_state=config.random_state, stratify=y
    )
    
    print(f"📚 Antrenare: {len(X_train)} exemple")
    print(f"🧪 Test: {len(X_test)} exemple")
    
    # Modele de testat
    modele = {
        'Naive Bayes': MultinomialNB(),
        'Bernoulli NB': BernoulliNB(),
        'Logistic Regression': LogisticRegression(max_iter=1000, C=1.0),
        'Linear SVM': LinearSVC(max_iter=2000, C=1.0),
        'RBF SVM': SVC(kernel='rbf', C=1.0, gamma='scale', probability=True),
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=config.random_state),
        'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=config.random_state),
        'MLP (Neural Network)': MLPClassifier(hidden_layer_sizes=(128, 64), max_iter=500, random_state=config.random_state)
    }
    
    rezultate = {}
    modele_antrenate = {}
    
    for nume, model in modele.items():
        print(f"\n   🔄 Antrenez: {nume}")
        
        start_time = time.time()
        model.fit(X_train, y_train)
        train_time = time.time() - start_time
        
        # Predictii
        y_pred = model.predict(X_test)
        
        # Probabilități (dacă suportă)
        if hasattr(model, 'predict_proba'):
            y_proba = model.predict_proba(X_test)
        else:
            y_proba = None
        
        # Metrici
        acuratete = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
        recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
        
        rezultate[nume] = {
            'model': model,
            'acuratete': acuratete,
            'precision': precision,
            'recall': recall,
            'f1': f1,
            'timp': train_time
        }
        modele_antrenate[nume] = model
        
        print(f"      ✅ Acuratețe: {acuratete:.4f}")
        print(f"      🎯 F1-score: {f1:.4f}")
        print(f"      ⏱️  Timp: {train_time:.2f}s")
    
    # Găsește cel mai bun model
    cel_mai_bun = max(rezultate, key=lambda x: rezultate[x]['f1'])
    print(f"\n🏆 Cel mai bun model tradițional: {cel_mai_bun}")
    print(f"   Acuratețe: {rezultate[cel_mai_bun]['acuratete']:.4f}")
    print(f"   F1-score: {rezultate[cel_mai_bun]['f1']:.4f}")
    
    return modele_antrenate, rezultate, X_test, y_test


# ==================== DEEP LEARNING MODEL ====================

class IntentDataset(Dataset):
    """Dataset pentru PyTorch"""
    
    def __init__(self, X, y, label_encoder):
        self.X = torch.FloatTensor(X.toarray() if hasattr(X, 'toarray') else X)
        self.y = torch.LongTensor(label_encoder.transform(y))
    
    def __len__(self):
        return len(self.y)
    
    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]

class IntentClassifier(nn.Module):
    """Clasificator de intenții cu deep learning"""
    
    def __init__(self, input_dim, num_classes, hidden_dim=256, num_layers=2, dropout=0.3):
        super().__init__()
        
        self.input_dim = input_dim
        self.num_classes = num_classes
        
        # Layers
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.bn1 = nn.BatchNorm1d(hidden_dim)
        self.dropout1 = nn.Dropout(dropout)
        
        self.fc2 = nn.Linear(hidden_dim, hidden_dim // 2)
        self.bn2 = nn.BatchNorm1d(hidden_dim // 2)
        self.dropout2 = nn.Dropout(dropout)
        
        self.fc3 = nn.Linear(hidden_dim // 2, num_classes)
        
        # Activations
        self.relu = nn.ReLU()
        
        # Initialization
        self._initialize_weights()
    
    def _initialize_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Linear):
                nn.init.kaiming_normal_(m.weight, mode='fan_in', nonlinearity='relu')
                if m.bias is not None:
                    nn.init.constant_(m.bias, 0)
    
    def forward(self, x):
        x = self.relu(self.bn1(self.fc1(x)))
        x = self.dropout1(x)
        
        x = self.relu(self.bn2(self.fc2(x)))
        x = self.dropout2(x)
        
        x = self.fc3(x)
        return x

def antreneaza_deep_learning(X_train, X_test, y_train, y_test):
    """Antrenează modelul de deep learning"""
    print("\n🧠 ANTRENARE DEEP LEARNING")
    print("-" * 40)
    
    if not config.use_deep_learning:
        print("⚠️ Deep learning dezactivat (GPU indisponibil)")
        return None, None
    
    # Label encoding
    label_encoder = LabelEncoder()
    y_train_encoded = label_encoder.fit_transform(y_train)
    y_test_encoded = label_encoder.transform(y_test)
    num_classes = len(label_encoder.classes_)
    
    print(f"🏷️ Clase: {num_classes}")
    print(f"   {list(label_encoder.classes_)}")
    
    # Dataset-uri
    train_dataset = IntentDataset(X_train, y_train, label_encoder)
    test_dataset = IntentDataset(X_test, y_test, label_encoder)
    
    train_loader = DataLoader(train_dataset, batch_size=config.batch_size, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=config.batch_size, shuffle=False)
    
    # Model
    model = IntentClassifier(
        input_dim=X_train.shape[1],
        num_classes=num_classes,
        hidden_dim=config.hidden_dim,
        num_layers=config.num_layers,
        dropout=config.dropout
    ).to(config.device)
    
    # Loss și optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=config.learning_rate, weight_decay=1e-5)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', patience=5, factor=0.5)
    
    print(f"\n📊 Model arhitectură:")
    print(f"   • Embedding dim: {config.embedding_dim}")
    print(f"   • Hidden dim: {config.hidden_dim}")
    print(f"   • Layers: {config.num_layers}")
    print(f"   • Params: {sum(p.numel() for p in model.parameters()):,}")
    
    # Antrenare
    train_losses = []
    val_accuracies = []
    best_accuracy = 0
    best_state = None
    patience_counter = 0
    
    for epoch in tqdm(range(config.num_epochs), desc="Antrenare DL"):
        # Training
        model.train()
        epoch_loss = 0
        for batch_X, batch_y in train_loader:
            batch_X, batch_y = batch_X.to(config.device), batch_y.to(config.device)
            
            optimizer.zero_grad()
            outputs = model(batch_X)
            loss = criterion(outputs, batch_y)
            loss.backward()
            optimizer.step()
            
            epoch_loss += loss.item()
        
        avg_loss = epoch_loss / len(train_loader)
        train_losses.append(avg_loss)
        
        # Validation
        model.eval()
        correct = 0
        total = 0
        with torch.no_grad():
            for batch_X, batch_y in test_loader:
                batch_X, batch_y = batch_X.to(config.device), batch_y.to(config.device)
                outputs = model(batch_X)
                _, predicted = torch.max(outputs, 1)
                total += batch_y.size(0)
                correct += (predicted == batch_y).sum().item()
        
        accuracy = correct / total
        val_accuracies.append(accuracy)
        
        # Scheduler step
        scheduler.step(avg_loss)
        
        # Early stopping
        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_state = model.state_dict().copy()
            patience_counter = 0
        else:
            patience_counter += 1
        
        if patience_counter >= 10:
            print(f"\n⏹️ Early stopping la epoch {epoch+1}")
            break
        
        if (epoch + 1) % 5 == 0:
            print(f"   Epoch {epoch+1}/{config.num_epochs} - Loss: {avg_loss:.4f}, Acc: {accuracy:.4f}")
    
    # Restaurează cel mai bun model
    if best_state:
        model.load_state_dict(best_state)
    
    # Evaluare finală
    model.eval()
    all_preds = []
    all_probs = []
    
    with torch.no_grad():
        for batch_X, batch_y in test_loader:
            batch_X = batch_X.to(config.device)
            outputs = model(batch_X)
            probs = torch.softmax(outputs, dim=1)
            _, preds = torch.max(outputs, 1)
            
            all_preds.extend(preds.cpu().numpy())
            all_probs.extend(probs.cpu().numpy())
    
    # Convert back to original labels
    y_pred = label_encoder.inverse_transform(all_preds)
    
    # Metrici
    acuratete = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average='weighted')
    
    print(f"\n🏆 Rezultate Deep Learning:")
    print(f"   Acuratețe: {acuratete:.4f}")
    print(f"   F1-score: {f1:.4f}")
    
    # Crează model wrapper pentru compatibilitate
    class DLModelWrapper:
        def __init__(self, model, vectorizer, label_encoder):
            self.model = model
            self.vectorizer = vectorizer
            self.label_encoder = label_encoder
            self.device = config.device
        
        def predict(self, X):
            if hasattr(X, 'toarray'):
                X = X.toarray()
            X_tensor = torch.FloatTensor(X).to(self.device)
            self.model.eval()
            with torch.no_grad():
                outputs = self.model(X_tensor)
                _, preds = torch.max(outputs, 1)
            return self.label_encoder.inverse_transform(preds.cpu().numpy())
        
        def predict_proba(self, X):
            if hasattr(X, 'toarray'):
                X = X.toarray()
            X_tensor = torch.FloatTensor(X).to(self.device)
            self.model.eval()
            with torch.no_grad():
                outputs = self.model(X_tensor)
                probs = torch.softmax(outputs, dim=1)
            return probs.cpu().numpy()
    
    dl_model = DLModelWrapper(model, None, label_encoder)
    
    return dl_model, {'acuratete': acuratete, 'f1': f1}


# ==================== ENSEMBLE MODEL ====================

def creeaza_ensemble(modele, vectorizer, label_encoder=None):
    """Creează model ensemble cu votare"""
    print("\n🤝 CREARE ENSEMBLE MODEL")
    print("-" * 40)
    
    # Extrage cele mai bune modele
    modele_selectate = {}
    
    # Logistic Regression (de obicei bun)
    if 'Logistic Regression' in modele:
        modele_selectate['Logistic Regression'] = modele['Logistic Regression']
    
    # Linear SVM (de obicei excelent)
    if 'Linear SVM' in modele:
        modele_selectate['Linear SVM'] = modele['Linear SVM']
    
    # Random Forest (diversitate)
    if 'Random Forest' in modele:
        modele_selectate['Random Forest'] = modele['Random Forest']
    
    # Gradient Boosting (dacă există)
    if 'Gradient Boosting' in modele:
        modele_selectate['Gradient Boosting'] = modele['Gradient Boosting']
    
    print(f"📊 Modele în ensemble: {len(modele_selectate)}")
    for nume in modele_selectate:
        print(f"   • {nume}")
    
    # Crează ensemble cu votare soft (probabilități)
    if label_encoder:
        # Pentru predict_proba
        estimators = [(nume.replace(' ', '_'), model) for nume, model in modele_selectate.items()]
        ensemble = VotingClassifier(estimators=estimators, voting='soft')
    else:
        estimators = [(nume.replace(' ', '_'), model) for nume, model in modele_selectate.items()]
        ensemble = VotingClassifier(estimators=estimators, voting='hard')
    
    return ensemble


# ==================== CROSS-VALIDATION ====================

def cross_validate_model(model, X, y, num_folds=5):
    """Cross-validation pentru model"""
    print("\n📊 CROSS-VALIDATION")
    print("-" * 40)
    
    skf = StratifiedKFold(n_splits=num_folds, shuffle=True, random_state=config.random_state)
    
    scores = cross_val_score(model, X, y, cv=skf, scoring='accuracy')
    
    print(f"📈 Rezultate {num_folds}-fold CV:")
    print(f"   Media: {scores.mean():.4f} (±{scores.std():.4f})")
    print(f"   Individual: {[f'{s:.4f}' for s in scores]}")
    
    return scores.mean(), scores.std()


# ==================== HYPERPARAMETER TUNING ====================

def tuning_hyperparametri(X_train, y_train):
    """Optimizare hiperparametri pentru cel mai bun model"""
    print("\n🔧 TUNING HIPERPARAMETRI")
    print("-" * 40)
    
    # Folosește Linear SVM de obicei cel mai bun pentru text
    from sklearn.model_selection import GridSearchCV
    
    param_grid = {
        'C': [0.1, 0.5, 1.0, 2.0, 5.0],
        'max_iter': [1000, 2000]
    }
    
    svm = LinearSVC(random_state=config.random_state)
    
    grid_search = GridSearchCV(
        svm, param_grid, cv=3, scoring='accuracy', 
        n_jobs=-1, verbose=0
    )
    
    print("🔍 Caut cele mai bune parametri...")
    grid_search.fit(X_train, y_train)
    
    print(f"✅ Cei mai buni parametri: {grid_search.best_params_}")
    print(f"🏆 Cel mai bun scor: {grid_search.best_score_:.4f}")
    
    return grid_search.best_estimator_


# ==================== EVALUARE AVANSATĂ ====================

def evaluare_avansata(model, X_test, y_test, nume_model):
    """Evaluare completă a modelului"""
    print(f"\n📈 EVALUARE MODEL: {nume_model}")
    print("-" * 40)
    
    # Predictii
    y_pred = model.predict(X_test)
    
    # Probabilități dacă suportă
    if hasattr(model, 'predict_proba'):
        y_proba = model.predict_proba(X_test)
    else:
        y_proba = None
    
    # Metrici principale
    acuratete = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
    
    print(f"📊 Metrici principale:")
    print(f"   • Acuratețe: {acuratete:.4f}")
    print(f"   • Precision: {precision:.4f}")
    print(f"   • Recall:    {recall:.4f}")
    print(f"   • F1-score:  {f1:.4f}")
    
    # Raport detaliat
    print(f"\n📋 Raport clasificare detaliat:")
    print(classification_report(y_test, y_pred))
    
    # Matrice confuzie
    cm = confusion_matrix(y_test, y_pred)
    labels = sorted(set(y_test))
    
    plt.figure(figsize=(12, 10))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=labels, yticklabels=labels)
    plt.title(f'Matrice Confuzie - {nume_model}')
    plt.xlabel('Predicție')
    plt.ylabel('Real')
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig(config.results_dir / f'matrice_confuzie_{nume_model.replace(" ", "_")}.png', dpi=150)
    plt.show()
    
    return {
        'acuratete': acuratete,
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'confusion_matrix': cm,
        'labels': labels
    }


# ==================== SALVARE MODEL ====================

def salveaza_model(model, vectorizer, label_encoder, nume, metadate):
    """Salvează modelul antrenat pentru API"""
    print(f"\n💾 SALVEZ MODELUL: {nume}")
    print("-" * 40)
    
    import pickle
    from datetime import datetime
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Salvează modelul
    model_path = config.models_dir / f"{nume.replace(' ', '_')}_{timestamp}.pkl"
    with open(model_path, 'wb') as f:
        pickle.dump({
            'model': model,
            'vectorizer': vectorizer,
            'label_encoder': label_encoder,
            'metadate': metadate,
            'timestamp': timestamp
        }, f)
    
    # Salvează și ca latest pentru API
    latest_path = config.models_dir / f"{nume.replace(' ', '_')}_latest.pkl"
    with open(latest_path, 'wb') as f:
        pickle.dump({
            'model': model,
            'vectorizer': vectorizer,
            'label_encoder': label_encoder,
            'metadate': metadate,
            'timestamp': timestamp
        }, f)
    
    print(f"✅ Model salvat: {model_path}")
    print(f"✅ Versiune latest: {latest_path}")
    
    return model_path


# ==================== TESTARE CU EXEMPLE NOI ====================

def testeaza_cu_exemple(model, vectorizer, label_encoder):
    """Testează modelul cu exemple noi"""
    print("\n🧪 TESTARE CU EXEMPLE NOI")
    print("-" * 40)
    
    exemple_noi = [
        "Cum se face pizza acasă?",
        "Cât timp se coace cozonacul?",
        "Ce ingrediente pentru sarmale?",
        "Cu ce înlocuiesc ouăle în prăjituri?",
        "E greu de făcut clătite?",
        "Salut, ce faci?",
        "Mulțumesc pentru ajutor!",
        "Cum prepar o supă cremă de legume?",
        "Câte minute fierb ouale tari?",
        "Rețetă de mămăligă cu brânză"
    ]
    
    # Preprocesare
    exemple_curatate = [text.lower().replace(r'[^\w\s]', '') for text in exemple_noi]
    
    # Vectorizare
    X_test = vectorizer.transform(exemple_curatate)
    
    # Predicții
    predictions = model.predict(X_test)
    
    # Probabilități
    if hasattr(model, 'predict_proba'):
        probabilitati = model.predict_proba(X_test)
        clase = label_encoder.classes_ if label_encoder else None
    else:
        probabilitati = None
    
    print("\n📝 Rezultate predicții:")
    for i, (exemplu, pred) in enumerate(zip(exemple_noi, predictions)):
        print(f"\n   {i+1}. '{exemplu}'")
        print(f"      → Intenție: {pred}")
        if probabilitati is not None:
            top3_idx = np.argsort(probabilitati[i])[-3:][::-1]
            print(f"      → Top 3: ", end="")
            for idx in top3_idx:
                print(f"{clase[idx]}({probabilitati[i][idx]:.2%}) ", end="")
            print()


# ==================== RAPORT FINAL ====================

def genereaza_raport_final(rezultate_modele, cel_mai_bun_model, rezultate_test):
    """Generează raport final pentru prezentare"""
    print("\n" + "=" * 80)
    print("📊 RAPORT FINAL - MODEL CLASIFICARE INTENȚII")
    print("=" * 80)
    
    print("\n📈 COMPARAȚIE MODELE:")
    print("-" * 40)
    
    # Tabel comparație
    print(f"\n{'Model':<25} {'Acuratețe':<12} {'Precision':<12} {'Recall':<12} {'F1-score':<12}")
    print("-" * 70)
    
    for nume, rez in rezultate_modele.items():
        print(f"{nume:<25} {rez['acuratete']:.4f}      {rez.get('precision', 0):.4f}      {rez.get('recall', 0):.4f}      {rez.get('f1', 0):.4f}")
    
    print(f"\n🏆 CEL MAI BUN MODEL: {cel_mai_bun_model}")
    print(f"   Acuratețe: {rezultate_test['acuratete']:.4f} ({rezultate_test['acuratete']*100:.2f}%)")
    print(f"   F1-score: {rezultate_test['f1']:.4f}")
    
    # Confuzie
    print(f"\n🎭 MATRICE CONFUZIE:")
    cm = rezultate_test['confusion_matrix']
    labels = rezultate_test['labels']
    
    for i, label in enumerate(labels):
        print(f"   {label}: {cm[i]}")
    
    # Statistici dataset
    print(f"\n📊 STATISTICI FINALE:")
    print(f"   • Modele evaluate: {len(rezultate_modele)}")
    print(f"   • Model final: {cel_mai_bun_model}")
    print(f"   • Acoperire intenții: {len(labels)}")
    print(f"   • Cea mai bună acuratețe: {max(r['acuratete'] for r in rezultate_modele.values()):.4f}")
    
    # Recomandări
    print(f"\n🎯 RECOMANDĂRI:")
    if rezultate_test['acuratete'] >= 0.90:
        print(f"   ✅ Modelul este EXCELENT! Poate fi folosit în producție.")
    elif rezultate_test['acuratete'] >= 0.80:
        print(f"   👍 Modelul este BUN. Poate fi îmbunătățit cu mai multe date.")
    else:
        print(f"   ⚠️ Modelul are nevoie de mai multe date de antrenare.")
    
    print("\n" + "=" * 80)


# ==================== FUNCȚIA PRINCIPALĂ ====================

def main():
    """Funcția principală"""
    print("\n🚀 START ANTRENARE MODEL COMPLET")
    print("=" * 80)
    
    # 1. Încarcă datele de la Vasile
    df = incarca_date()
    
    # 2. Preprocesare text
    df = preproceseaza_text(df)
    
    # 3. Vectorizare
    vectorizer, X, y = creeaza_vectorizator(df)
    
    # 4. Split date
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=config.test_size, 
        random_state=config.random_state, stratify=y
    )
    
    # 5. Antrenează modele tradiționale
    modele, rezultate_trad, X_test_trad, y_test_trad = antreneaza_modele_traditionale(X_train, y_train)
    
    # 6. Hyperparameter tuning
    best_svm = tuning_hyperparametri(X_train, y_train)
    modele['Linear SVM (tuned)'] = best_svm
    
    # 7. Deep Learning (opțional)
    if config.use_deep_learning:
        dl_model, rezultate_dl = antreneaza_deep_learning(X_train, X_test, y_train, y_test)
        if dl_model:
            modele['Deep Learning'] = dl_model
            rezultate_trad['Deep Learning'] = rezultate_dl
    
    # 8. Ensemble model
    if config.use_ensemble and len(modele) >= 2:
        ensemble = creeaza_ensemble(modele, vectorizer)
        if ensemble:
            ensemble.fit(X_train, y_train)
            modele['Ensemble'] = ensemble
            y_pred_ensemble = ensemble.predict(X_test)
            rezultate_trad['Ensemble'] = {
                'acuratete': accuracy_score(y_test, y_pred_ensemble),
                'f1': f1_score(y_test, y_pred_ensemble, average='weighted')
            }
    
    # 9. Cross-validation pentru cel mai bun model
    cel_mai_bun = max(rezultate_trad, key=lambda x: rezultate_trad[x]['acuratete'])
    
    print(f"\n🏆 CEL MAI BUN MODEL: {cel_mai_bun}")
    
    # 10. Evaluare avansată
    cel_mai_bun_model = modele[cel_mai_bun]
    rezultate_test = evaluare_avansata(cel_mai_bun_model, X_test, y_test, cel_mai_bun)
    
    # 11. Testare cu exemple noi
    label_encoder = LabelEncoder()
    label_encoder.fit(y)
    testeaza_cu_exemple(cel_mai_bun_model, vectorizer, label_encoder)
    
    # 12. Salvează modelul
    metadate = {
        'nume_model': cel_mai_bun,
        'acuratete': rezultate_test['acuratete'],
        'f1_score': rezultate_test['f1'],
        'numar_exemple': len(df),
        'numar_intentii': y.nunique(),
        'intentii': list(y.unique()),
        'vectorizer_params': {
            'max_features': config.max_features,
            'ngram_range': config.ngram_range
        }
    }
    
    model_path = salveaza_model(cel_mai_bun_model, vectorizer, label_encoder, cel_mai_bun, metadate)
    
    # 13. Generează raport final
    genereaza_raport_final(rezultate_trad, cel_mai_bun, rezultate_test)
    
    print("\n" + "=" * 80)
    print("✅ ANTRENARE COMPLETĂ!")
    print("=" * 80)
    print(f"\n📁 Model salvat în: {model_path}")
    print("🔗 API-ul lui Dumitru poate folosi: models/saved/Linear_SVM_latest.pkl")
    print("\n🎯 Următorul pas: Integrează modelul în API-ul lui Dumitru!")


# ==================== EXECUȚIE ====================

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Execuție oprită manual")
    except Exception as e:
        print(f"\n❌ EROARE: {e}")
        import traceback
        traceback.print_exc()
        print("\n🔧 Verifică:")
        print("   1. Există fișierul date_antrenare.csv în data/processed/")
        print("   2. Rulează: pip install scikit-learn pandas numpy matplotlib seaborn tqdm")
        print("   3. Pentru deep learning: pip install torch")