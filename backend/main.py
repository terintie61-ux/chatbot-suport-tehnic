"""
API pentru Chatbot Culinar - "Bucătarul Virtual"
Autor: Vasilache Dumitru
Data: 2024
"""

from flask import Flask, jsonify, request
import json
import os
from datetime import datetime
import random

# Creează aplicația Flask
app = Flask(__name__)

# Încarcă răspunsurile predefinite
def incarca_raspunsuri():
    try:
        with open('data/raw_data/scheme_raspuns.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Fișierul scheme_raspuns.json nu a fost găsit!")
        return {"raspunsuri": []}

# Încarcă întrebările și răspunsurile
def incarca_intrebari():
    try:
        with open('data/raw_data/intrebari_culinare.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Fișierul intrebari_culinare.json nu a fost găsit!")
        return []

# Încarcă datele la pornire
raspunsuri_predefinite = incarca_raspunsuri()
intrebari_culinare = incarca_intrebari()

# ==================== RUTE API ====================

@app.route('/health', methods=['GET'])
def health():
    """
    Verifică dacă API-ul funcționează
    """
    return jsonify({
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "versiune": "1.0",
        "raspunsuri_incarcate": len(raspunsuri_predefinite.get('raspunsuri', [])),
        "intrebari_incarcate": len(intrebari_culinare)
    })


@app.route('/chat', methods=['POST'])
def chat():
    """
    Primește un mesaj și returnează un răspuns
    """
    
    """
    try:
        # Primește datele de la utilizator
        data = request.json
        
        if not data or 'mesaj' not in data:
            return jsonify({
                "error": "Te rog să trimiți un mesaj valid",
                "exemplu": {"mesaj": "Cum se face pizza?"}
            }), 400
        
        mesaj = data['mesaj'].lower()
        
        # Loghează cererea
        log_cerere(mesaj)
        
        # Caută răspunsul potrivit
        raspuns, intentie = gaseste_raspuns(mesaj)
        
        # Returnează răspunsul
        return jsonify({
            "mesaj_original": data['mesaj'],
            "raspuns": raspuns,
            "intentie_detectata": intentie,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "error": "A apărut o eroare",
            "details": str(e)
        }), 500
    """

    
    


@app.route('/stats', methods=['GET'])
def stats():
    """
    Afișează statistici despre API
    """
    return jsonify({
        "total_raspunsuri": len(raspunsuri_predefinite.get('raspunsuri', [])),
        "total_intrebari": len(intrebari_culinare),
        "categorii_raspunsuri": get_categorii_raspunsuri(),
        "api_status": "active"
    })


@app.route('/ping', methods=['GET'])
def ping():
    """
    Endpoint simplu pentru testare rapidă
    """
    return jsonify({"pong": "API-ul funcționează!"})

# ==================== FUNCȚII DE AJUTOR ====================

def gaseste_raspuns(mesaj):
    """
    Găsește cel mai potrivit răspuns pentru mesajul primit
    """
    # 1. Caută în întrebările predefinite (intrebari_culinare.json)
    for item in intrebari_culinare:
        if item.get('intrebare', '').lower() in mesaj or mesaj in item.get('intrebare', '').lower():
            return item.get('raspuns', 'Îmi pare rău, nu am un răspuns'), 'intrebare_predefinita'
    
    # 2. Caută în răspunsurile predefinite după cuvinte cheie
    for raspuns in raspunsuri_predefinite.get('raspunsuri', []):
        for keyword in raspuns.get('keywords', []):
            if keyword in mesaj:
                return raspuns['raspuns'], raspuns['categorie']
    
    # 3. Salut
    if any(word in mesaj for word in ['salut', 'buna', 'bună', 'hey', 'hello', 'hi']):
        return gaseste_raspuns_categorie('salut'), 'salut'
    
    # 4. Mulțumesc
    if any(word in mesaj for word in ['multumesc', 'mersi', 'merci', 'thanks']):
        return gaseste_raspuns_categorie('multumesc'), 'multumesc'
    
    # 5. Răspuns default
    return "Îmi pare rău, nu am înțeles întrebarea. Încearcă să mă întrebi despre rețete, ingrediente sau timpi de preparare!", 'necunoscut'

def gaseste_raspuns_categorie(categorie):
    """
    Găsește un răspuns aleatoriu dintr-o categorie
    """
    raspunsuri_categorie = [r for r in raspunsuri_predefinite.get('raspunsuri', []) 
                           if r.get('categorie') == categorie]
    
    if raspunsuri_categorie:
        return random.choice(raspunsuri_categorie)['raspuns']
    
    # Răspuns fallback
    if categorie == 'salut':
        return "Salut! Cu ce te pot ajuta în bucătărie?"
    elif categorie == 'multumesc':
        return "Cu plăcere! Poftă bună!"
    else:
        return "Te rog să reformulezi întrebarea."

def get_categorii_raspunsuri():
    """
    Returnează numărul de răspunsuri pe categorii
    """
    categorii = {}
    for r in raspunsuri_predefinite.get('raspunsuri', []):
        cat = r.get('categorie', 'necunoscut')
        categorii[cat] = categorii.get(cat, 0) + 1
    return categorii

def log_cerere(mesaj):
    """
    Salvează cererile în fișierul de log
    """
    try:
        with open('src/api/logs/requests.log', 'a', encoding='utf-8') as f:
            f.write(f"{datetime.now().isoformat()} - {mesaj}\n")
    except:
        pass  # Dacă nu se poate scrie, ignoră

# ==================== PORNIRE SERVER ====================

if __name__ == '__main__':
    print("=" * 50)
    print("🍳 API CHATBOT CULINAR - 'BUCĂTARUL VIRTUAL'")
    print("=" * 50)
    print(f"📊 Răspunsuri încărcate: {len(raspunsuri_predefinite.get('raspunsuri', []))}")
    print(f"📊 Întrebări încărcate: {len(intrebari_culinare)}")
    print("=" * 50)
    print("🚀 Serverul pornește la http://localhost:5000")
    print("📋 Endpoint-uri disponibile:")
    print("   GET  /health  - verifică starea")
    print("   GET  /ping    - test rapid")
    print("   GET  /stats   - statistici")
    print("   POST /chat    - trimite un mesaj")
    print("=" * 50)
    print("ℹ️  Pentru a opri serverul: CTRL + C")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)