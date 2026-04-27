"""
API pentru Chatbot Culinar - "Bucătarul Virtual"
Cu DUBLU MODEL:
1. Model ML (SVM) - pentru clasificare intenții (reteta, timp, ingrediente, etc.)
2. Model Neural (PyTorch) - pentru clasificare categorii (Cakes, Breakfast, Soups, etc.)

Autor: Vasilache Dumitru
Data: 2024
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
from datetime import datetime
import joblib
import torch
import torch.nn as nn
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# ==================== CREARE APLICAȚIE FLASK ====================

app = Flask(__name__)

# ACTIVARE CORS - PERMITE CERERI DE LA ORICE ORIGIN (inclusiv frontend-ul lui Debora)
CORS(app)  # Aceasta permite frontend-ului să comunice cu API-ul

# ==================== CONFIGURARE CĂI (păstrat ca în codul tău) ====================

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
RAW_DATA_PATH = os.path.join(DATA_DIR, 'raw_data')
PROCESSED_DATA_PATH = os.path.join(DATA_DIR, 'processed_data')

# ==================== MODELUL 1: INTENȚII (SVM) - model vechi ====================

def incarca_modelul_intentii():
    """Încarcă modelul SVM antrenat de Carai Maria (pentru intenții)"""
    # Încearcă mai întâi în folderul API
    model_path = 'models/model_latest.pkl'
    if not os.path.exists(model_path):
        # Alternativ, încearcă în folderul principal
        model_path = 'models/saved/model_latest.pkl'
    
    if os.path.exists(model_path):
        try:
            model = joblib.load(model_path)
            print(f"✅ Model intenții (SVM) încărcat cu succes din: {model_path}")
            return model
        except Exception as e:
            print(f"❌ Eroare la încărcarea modelului intenții: {e}")
            return None
    else:
        print(f"⚠️ Modelul intenții nu a fost găsit la: {model_path}")
        print("   Rulează mai întâi: python src/model/antreneaza_model.py")
        return None

# ==================== MODELUL 2: CATEGORII (PyTorch) - model nou ====================

class AttentionLayer(nn.Module):
    """Strat de atenție pentru focus pe cuvinte importante"""
    def __init__(self, hidden_size):
        super(AttentionLayer, self).__init__()
        self.attention = nn.Linear(hidden_size, 1)
    
    def forward(self, x):
        attention_weights = torch.softmax(self.attention(x), dim=1)
        weighted_output = x * attention_weights
        return weighted_output.sum(dim=1)

class EnhancedNeuralClassifier(nn.Module):
    """Model neuronal îmbunătățit cu atenție și residual connections"""
    def __init__(self, input_size, num_classes, hidden_sizes=[1024, 512, 256, 128]):
        super(EnhancedNeuralClassifier, self).__init__()
        
        self.layers = nn.ModuleList()
        self.batch_norms = nn.ModuleList()
        self.dropouts = nn.ModuleList()
        self.residual_connections = []
        
        prev_size = input_size
        
        for i, hidden_size in enumerate(hidden_sizes):
            self.layers.append(nn.Linear(prev_size, hidden_size))
            self.batch_norms.append(nn.BatchNorm1d(hidden_size))
            self.dropouts.append(nn.Dropout(0.3))
            
            # Residual connection dacă dimensiunile se potrivesc
            self.residual_connections.append(prev_size == hidden_size)
            prev_size = hidden_size
        
        # Strat final
        self.final_layer = nn.Linear(hidden_sizes[-1], num_classes)
        
        # Funcții de activare
        self.relu = nn.ReLU()
        self.softmax = nn.LogSoftmax(dim=1)
    
    def forward(self, x):
        for i, (layer, bn, dropout, use_residual) in enumerate(zip(
            self.layers, self.batch_norms, self.dropouts, self.residual_connections
        )):
            identity = x
            
            x = layer(x)
            x = bn(x)
            x = self.relu(x)
            
            # Residual connection
            if use_residual and i > 0:
                if identity.shape[1] != x.shape[1]:
                    identity = identity[:, :x.shape[1]]
                x = x + identity
            
            x = dropout(x)
        
        x = self.final_layer(x)
        return self.softmax(x)


def incarca_modelul_categorii():
    """Încarcă modelul PyTorch antrenat de Carai Maria (pentru categorii)"""
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model_path = 'models/saved/model_optimizat.pt'
    
    if not os.path.exists(model_path):
        print(f"⚠️ Modelul categorii nu a fost găsit la: {model_path}")
        print("   Rulează mai întâi scriptul de antrenare optimizat")
        return None, None, None, device
    
    try:
        # Încarcă vectorizatorul, encoderul și scalerul
        vectorizer = joblib.load('models/saved/vectorizer_optimizat.pkl')
        label_encoder = joblib.load('models/saved/label_encoder_optimizat.pkl')
        scaler = joblib.load('models/saved/scaler.pkl')
        
        # Încarcă modelul PyTorch
        checkpoint = torch.load(model_path, map_location=device)
        
        model_config = checkpoint['model_config']
        model = EnhancedNeuralClassifier(
            input_size=model_config['input_size'],
            num_classes=model_config['num_classes'],
            hidden_sizes=model_config['hidden_sizes']
        ).to(device)
        
        model.load_state_dict(checkpoint['model_state_dict'])
        model.eval()
        
        print(f"✅ Model categorii (PyTorch) încărcat cu succes")
        print(f"   - GPU activ: {device.type == 'cuda'}")
        print(f"   - Clase disponibile: {len(label_encoder.classes_)}")
        
        return model, vectorizer, label_encoder, scaler
        
    except Exception as e:
        print(f"❌ Eroare la încărcarea modelului categorii: {e}")
        return None, None, None, device


# ==================== ÎNCĂRCARE MODELE ====================

# Încarcă modelul de intenții (SVM) - model vechi
model_intentii = incarca_modelul_intentii()

# Încarcă modelul de categorii (PyTorch) - model nou
model_categorii, vectorizer_categorii, label_encoder_categorii, scaler_categorii = incarca_modelul_categorii()

# ==================== ÎNCĂRCARE DATE ====================

def incarca_raspunsuri():
    """Încarcă răspunsurile predefinite"""
    try:
        with open(os.path.join(PROCESSED_DATA_PATH, 'scheme_raspuns.json'), 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("⚠️ Fișierul scheme_raspuns.json nu a fost găsit!")
        return {"raspunsuri": []}

def incarca_intrebari():
    """Încarcă întrebările și răspunsurile"""
    try:
        with open(os.path.join(PROCESSED_DATA_PATH, 'intrebari_curatate.json'), 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("⚠️ Fișierul intrebari_curatate.json nu a fost găsit!")
        return []

# Încarcă datele la pornire
raspunsuri_predefinite = incarca_raspunsuri()
intrebari_culinare = incarca_intrebari()

# Dicționar de răspunsuri pentru fiecare intenție
RASPUNSURI_INTENTII = {
    'reteta': "Iată rețeta pe care o cauți! 🍳",
    'timp': "Timpul de preparare este... ⏱️",
    'ingrediente': "Iată ingredientele necesare! 📝",
    'inlocuitori': "Poți înlocui cu... 🔄",
    'dificultate': "Nivelul de dificultate este... 📊",
    'salut': "Salut! Cu ce te pot ajuta în bucătărie? 👨‍🍳",
    'multumesc': "Cu plăcere! Poftă bună! 😊",
    'la_revedere': "La revedere! Pe curând! 👋",
    'general': "Te pot ajuta cu rețete, timpi de preparare sau ingrediente!"
}

# ==================== FUNCȚII DE AJUTOR ====================

def gaseste_raspuns_intentie(intentie, mesaj):
    """Găsește răspunsul potrivit pentru intenția detectată"""
    
    # Caută în întrebările predefinite (dacă există potrivire exactă)
    for item in intrebari_culinare:
        if item.get('intrebare', '').lower() in mesaj.lower():
            return item.get('raspuns', RASPUNSURI_INTENTII.get(intentie, "Îmi pare rău, nu am un răspuns."))
    
    # Caută în răspunsurile predefinite după cuvinte cheie
    for raspuns in raspunsuri_predefinite.get('raspunsuri', []):
        for keyword in raspuns.get('keywords', []):
            if keyword in mesaj.lower():
                return raspuns['raspuns']
    
    # Răspuns bazat pe intenție
    return RASPUNSURI_INTENTII.get(intentie, "Îmi pare rău, nu am înțeles întrebarea. Încearcă să mă întrebi despre rețete, ingrediente sau timpi de preparare!")

def obtine_intentie_cu_model(mesaj):
    """
    Folosește modelul SVM pentru a detecta intenția
    Dacă modelul nu e disponibil, folosește reguli simple (fallback)
    """
    # Folosește modelul ML dacă e disponibil
    if model_intentii is not None:
        try:
            intentie = model_intentii.predict([mesaj])[0]
            print(f"   [ML-Intenții] Intenție detectată: {intentie}")
            return intentie
        except Exception as e:
            print(f"   [ML-Intenții] Eroare: {e}, folosesc fallback")
    
    # FALLBACK: Reguli simple dacă modelul nu e disponibil
    mesaj_lower = mesaj.lower()
    
    if any(word in mesaj_lower for word in ['reteta', 'cum se face', 'cum fac', 'prepar', 'retetă']):
        return 'reteta'
    elif any(word in mesaj_lower for word in ['timp', 'cat timp', 'cate minute', 'dureaza', 'cât']):
        return 'timp'
    elif any(word in mesaj_lower for word in ['ingrediente', 'ce pun', 'ce am nevoie', 'lista', 'ce ingrediente']):
        return 'ingrediente'
    elif any(word in mesaj_lower for word in ['inlocuiesc', 'inlocuitor', 'alternative', 'in loc de', 'înlocuiesc']):
        return 'inlocuitori'
    elif any(word in mesaj_lower for word in ['greu', 'dificil', 'complicat', 'dificultate']):
        return 'dificultate'
    elif any(word in mesaj_lower for word in ['salut', 'buna', 'bună', 'hey', 'hello', 'hi', 'bună ziua']):
        return 'salut'
    elif any(word in mesaj_lower for word in ['multumesc', 'mersi', 'merci', 'thanks', 'mulțumesc']):
        return 'multumesc'
    elif any(word in mesaj_lower for word in ['la revedere', 'pa', 'bye', 'ne vedem']):
        return 'la_revedere'
    else:
        return 'general'

def obtine_categorie(mesaj):
    """
    Folosește modelul PyTorch pentru a detecta categoria rețetei
    """
    if model_categorii is not None and vectorizer_categorii is not None:
        try:
            # Vectorizare
            X = vectorizer_categorii.transform([mesaj]).toarray()
            
            # Standardizare
            X = scaler_categorii.transform(X)
            
            # Convertire la tensor
            X_tensor = torch.FloatTensor(X).to(next(model_categorii.parameters()).device)
            
            # Predicție
            with torch.no_grad():
                output = model_categorii(X_tensor)
                proba = torch.softmax(output, dim=1)
                pred_idx = proba.argmax(dim=1).item()
                confidenta = proba[0][pred_idx].item()
            
            categorie = label_encoder_categorii.inverse_transform([pred_idx])[0]
            print(f"   [ML-Categorii] Categorie detectată: {categorie} (conf: {confidenta:.2%})")
            return categorie, confidenta
        except Exception as e:
            print(f"   [ML-Categorii] Eroare: {e}")
            return "general", 0.0
    return "general", 0.0

def log_cerere(mesaj, intentie, categorie, raspuns):
    """Salvează cererile în fișierul de log"""
    try:
        os.makedirs('src/api/logs', exist_ok=True)
        with open('src/api/logs/requests.log', 'a', encoding='utf-8') as f:
            f.write(f"{datetime.now().isoformat()} | Intenție: {intentie} | Categorie: {categorie} | Mesaj: {mesaj[:100]}\n")
    except:
        pass  # Dacă nu se poate scrie, ignoră

# ==================== RUTE API ====================

@app.route('/health', methods=['GET'])
def health():
    """Verifică dacă API-ul funcționează"""
    return jsonify({
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "versiune": "3.0",
        "modele": {
            "intentii_svm": model_intentii is not None,
            "categorii_pytorch": model_categorii is not None
        },
        "raspunsuri_incarcate": len(raspunsuri_predefinite.get('raspunsuri', [])),
        "intrebari_incarcate": len(intrebari_culinare),
        "cors_activ": True
    })

@app.route('/ping', methods=['GET'])
def ping():
    """Endpoint simplu pentru testare rapidă"""
    return jsonify({
        "pong": "API-ul funcționează!", 
        "modele": {
            "intentii": model_intentii is not None,
            "categorii": model_categorii is not None
        },
        "timestamp": datetime.now().isoformat()
    })

@app.route('/stats', methods=['GET'])
def stats():
    """Afișează statistici despre API și model"""
    return jsonify({
        "api_status": "active",
        "modele": {
            "intentii_svm": {
                "available": model_intentii is not None,
                "type": "SVM + TF-IDF"
            },
            "categorii_pytorch": {
                "available": model_categorii is not None,
                "type": "Neural Network + Attention",
                "classes": len(label_encoder_categorii.classes_) if label_encoder_categorii is not None else 0
            }
        },
        "total_raspunsuri": len(raspunsuri_predefinite.get('raspunsuri', [])),
        "total_intrebari": len(intrebari_culinare),
        "categorii_raspunsuri": get_categorii_raspunsuri(),
        "intentii_disponibile": list(RASPUNSURI_INTENTII.keys())
    })

@app.route('/chat', methods=['POST'])
def chat():
    """
    Primește un mesaj și returnează un răspuns folosind ambele modele
    """
    try:
        # Primește datele de la utilizator
        data = request.json
        
        if not data or 'mesaj' not in data:
            return jsonify({
                "success": False,
                "error": "Te rog să trimiți un mesaj valid",
                "exemplu": {"mesaj": "Cum se face pizza?"}
            }), 400
        
        mesaj = data['mesaj']
        mesaj_original = mesaj
        
        # 1. Detectează intenția folosind modelul SVM
        intentie = obtine_intentie_cu_model(mesaj)
        
        # 2. Detectează categoria folosind modelul PyTorch
        categorie, confidenta_categorie = obtine_categorie(mesaj)
        
        # 3. Găsește răspunsul potrivit
        raspuns = gaseste_raspuns_intentie(intentie, mesaj)
        
        # 4. Îmbogățește răspunsul cu informații din categorie (dacă e relevant)
        if categorie != 'general' and confidenta_categorie > 0.7:
            raspuns = f"[{categorie}] {raspuns}"
        
        # 5. Loghează cererea
        log_cerere(mesaj, intentie, categorie, raspuns)
        
        # 6. Returnează răspunsul
        return jsonify({
            "success": True,
            "mesaj_original": mesaj_original,
            "raspuns": raspuns,
            "intentie_detectata": intentie,
            "categorie_detectata": categorie,
            "confidenta_categorie": confidenta_categorie,
            "modele_folosite": {
                "intentii": model_intentii is not None,
                "categorii": model_categorii is not None
            },
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "A apărut o eroare",
            "details": str(e)
        }), 500

@app.route('/chat/test', methods=['POST'])
def chat_test():
    """
    Endpoint special pentru testare - afișează intenția și categoria detectată
    """
    try:
        data = request.json
        if not data or 'mesaj' not in data:
            return jsonify({"error": "Trimite un mesaj valid"}), 400
        
        mesaj = data['mesaj']
        
        intentie = obtine_intentie_cu_model(mesaj)
        categorie, confidenta_categorie = obtine_categorie(mesaj)
        raspuns = gaseste_raspuns_intentie(intentie, mesaj)
        
        return jsonify({
            "success": True,
            "mesaj": mesaj,
            "intentie_detectata": intentie,
            "categorie_detectata": categorie,
            "confidenta_categorie": confidenta_categorie,
            "raspuns": raspuns,
            "modele_folosite": {
                "intentii": model_intentii is not None,
                "categorii": model_categorii is not None
            },
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/chat/raw', methods=['POST'])
def chat_raw():
    """
    Endpoint care returnează răspunsul brut (pentru debugging)
    """
    try:
        data = request.json
        if not data or 'mesaj' not in data:
            return jsonify({"error": "Trimite un mesaj valid"}), 400
        
        mesaj = data['mesaj']
        intentie = obtine_intentie_cu_model(mesaj)
        categorie, confidenta_categorie = obtine_categorie(mesaj)
        raspuns = gaseste_raspuns_intentie(intentie, mesaj)
        
        return jsonify({
            "mesaj_original": mesaj,
            "intentie": intentie,
            "categorie": categorie,
            "confidenta_categorie": confidenta_categorie,
            "raspuns": raspuns,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/chat/intent-only', methods=['POST'])
def chat_intent_only():
    """
    Endpoint care folosește DOAR modelul de intenții (compatibilitate cu versiunea veche)
    """
    try:
        data = request.json
        if not data or 'mesaj' not in data:
            return jsonify({"error": "Trimite un mesaj valid"}), 400
        
        mesaj = data['mesaj']
        intentie = obtine_intentie_cu_model(mesaj)
        raspuns = gaseste_raspuns_intentie(intentie, mesaj)
        
        return jsonify({
            "success": True,
            "mesaj_original": mesaj,
            "raspuns": raspuns,
            "intentie_detectata": intentie,
            "model_folosit": model_intentii is not None,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

def get_categorii_raspunsuri():
    """Returnează numărul de răspunsuri pe categorii"""
    categorii = {}
    for r in raspunsuri_predefinite.get('raspunsuri', []):
        cat = r.get('categorie', 'necunoscut')
        categorii[cat] = categorii.get(cat, 0) + 1
    return categorii

# ==================== PORNIRE SERVER ====================

if __name__ == '__main__':
    print("=" * 60)
    print("🍳 API CHATBOT CULINAR - 'BUCĂTARUL VIRTUAL'")
    print("=" * 60)
    print(f"🤖 Model intenții (SVM): {'ÎNCĂRCAT ✅' if model_intentii is not None else 'NEDISPONIBIL ⚠️'}")
    print(f"🧠 Model categorii (PyTorch): {'ÎNCĂRCAT ✅' if model_categorii is not None else 'NEDISPONIBIL ⚠️'}")
    print(f"📊 Răspunsuri încărcate: {len(raspunsuri_predefinite.get('raspunsuri', []))}")
    print(f"📊 Întrebări încărcate: {len(intrebari_culinare)}")
    print(f"🔓 CORS: ACTIVAT ✅")
    print("=" * 60)
    print("🚀 Serverul pornește la http://localhost:5000")
    print("📋 Endpoint-uri disponibile:")
    print("   GET  /health           - verifică starea și modelele")
    print("   GET  /ping             - test rapid")
    print("   GET  /stats            - statistici")
    print("   POST /chat             - trimite un mesaj (folosește AMBELE modele)")
    print("   POST /chat/test        - test cu afișare intenție și categorie")
    print("   POST /chat/raw         - răspuns brut (debugging)")
    print("   POST /chat/intent-only - DOAR model intenții (compatibilitate)")
    print("=" * 60)
    print("ℹ️  Pentru a opri serverul: CTRL + C")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)