"""
API pentru Chatbot Culinar - "Bucătarul Virtual"
Cu integrare model machine learning antrenat de Carai Maria
Autor: Vasilache Dumitru
Data: 2024
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
from datetime import datetime
import joblib
import warnings
warnings.filterwarnings('ignore')

# Creează aplicația Flask
app = Flask(__name__)

# ACTIVARE CORS - PERMITE CERERI DE LA ORICE ORIGIN (inclusiv frontend-ul lui Debora)
CORS(app)  # Aceasta permite frontend-ului să comunice cu API-ul


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
RAW_DATA_PATH = os.path.join(DATA_DIR, 'raw_data')
PROCESSED_DATA_PATH = os.path.join(DATA_DIR, 'processed_data')



# ==================== ÎNCĂRCARE MODEL ====================





def incarca_modelul():
    """Încarcă modelul antrenat de Carai Maria"""
    # Încearcă mai întâi în folderul API
    model_path = 'src/api/models/model_latest.pkl'
    if not os.path.exists(model_path):
        # Alternativ, încearcă în folderul principal
        model_path = 'models/saved/model_latest.pkl'
    
    if os.path.exists(model_path):
        try:
            model = joblib.load(model_path)
            print(f"✅ Model încărcat cu succes din: {model_path}")
            return model
        except Exception as e:
            print(f"❌ Eroare la încărcarea modelului: {e}")
            return None
    else:
        print(f"⚠️ Modelul nu a fost găsit la: {model_path}")
        print("   Rulează mai întâi: python src/model/antreneaza_model.py")
        return None

# Încarcă modelul la pornirea API-ului
model_ml = incarca_modelul()

# ==================== ÎNCĂRCARE DATE ====================

def incarca_raspunsuri():
    """Încarcă răspunsurile predefinite"""
    try:
        with open(os.path.join(PROCESSED_DATA_PATH,'scheme_raspuns.json'), 'r', encoding='utf-8') as f:
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
    #print("Intrebari culinare: ",intrebari_culinare);
    
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
    Folosește modelul ML pentru a detecta intenția
    Dacă modelul nu e disponibil, folosește reguli simple (fallback)
    """
    # Folosește modelul ML dacă e disponibil
    if model_ml is not None:
        try:
            intentie = model_ml.predict([mesaj])[0]
            print(f"   [ML] Intenție detectată: {intentie}")
            return intentie
        except Exception as e:
            print(f"   [ML] Eroare: {e}, folosesc fallback")
    
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

def log_cerere(mesaj, intentie, raspuns):
    """Salvează cererile în fișierul de log"""
    try:
        os.makedirs('src/api/logs', exist_ok=True)
        with open('src/api/logs/requests.log', 'a', encoding='utf-8') as f:
            f.write(f"{datetime.now().isoformat()} | Intenție: {intentie} | Mesaj: {mesaj[:100]}\n")
    except:
        pass  # Dacă nu se poate scrie, ignoră

# ==================== RUTE API ====================

@app.route('/health', methods=['GET'])
def health():
    """Verifică dacă API-ul funcționează"""
    return jsonify({
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "versiune": "2.0",
        "model_incarcat": model_ml is not None,
        "raspunsuri_incarcate": len(raspunsuri_predefinite.get('raspunsuri', [])),
        "intrebari_incarcate": len(intrebari_culinare),
        "cors_activ": True
    })

@app.route('/ping', methods=['GET'])
def ping():
    """Endpoint simplu pentru testare rapidă"""
    return jsonify({
        "pong": "API-ul funcționează!", 
        "model_ready": model_ml is not None,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/stats', methods=['GET'])
def stats():
    """Afișează statistici despre API și model"""
    return jsonify({
        "api_status": "active",
        "model_incarcat": model_ml is not None,
        "total_raspunsuri": len(raspunsuri_predefinite.get('raspunsuri', [])),
        "total_intrebari": len(intrebari_culinare),
        "categorii_raspunsuri": get_categorii_raspunsuri(),
        "intentii_disponibile": list(RASPUNSURI_INTENTII.keys())
    })

@app.route('/chat', methods=['POST'])
def chat():
    """
    Primește un mesaj și returnează un răspuns folosind modelul ML
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
        
        # 1. Detectează intenția folosind modelul ML
        intentie = obtine_intentie_cu_model(mesaj)
        
        print("Intentie Model:", intentie)
        
        # 2. Găsește răspunsul potrivit
        raspuns = gaseste_raspuns_intentie(intentie, mesaj)
        
        # 3. Loghează cererea
        log_cerere(mesaj, intentie, raspuns)
        
        # 4. Returnează răspunsul
        return jsonify({
            "success": True,
            "mesaj_original": mesaj_original,
            "raspuns": raspuns,
            "intentie_detectata": intentie,
            "model_folosit": model_ml is not None,
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
    Endpoint special pentru testare - afișează și intenția detectată
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
            "mesaj": mesaj,
            "intentie_detectata": intentie,
            "raspuns": raspuns,
            "model_folosit": model_ml is not None,
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
        raspuns = gaseste_raspuns_intentie(intentie, mesaj)
        
        return jsonify({
            "mesaj_original": mesaj,
            "intentie": intentie,
            "raspuns": raspuns,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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
    print(f"🤖 Model ML: {'ÎNCĂRCAT ✅' if model_ml is not None else 'NEDISPONIBIL ⚠️'}")
    print(f"📊 Răspunsuri încărcate: {len(raspunsuri_predefinite.get('raspunsuri', []))}")
    print(f"📊 Întrebări încărcate: {len(intrebari_culinare)}")
    print(f"🔓 CORS: ACTIVAT ✅")
    print("=" * 60)
    print("🚀 Serverul pornește la http://localhost:5000")
    print("📋 Endpoint-uri disponibile:")
    print("   GET  /health      - verifică starea")
    print("   GET  /ping        - test rapid")
    print("   GET  /stats       - statistici")
    print("   POST /chat        - trimite un mesaj (folosește modelul ML)")
    print("   POST /chat/test   - test cu afișare intenție")
    print("   POST /chat/raw    - răspuns brut (debugging)")
    print("=" * 60)
    print("ℹ️  Pentru a opri serverul: CTRL + C")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)