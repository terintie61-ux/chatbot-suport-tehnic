"""
Script pentru testarea rapidă a API-ului cu model integrat
Autor: Vasilache Dumitru
"""

import requests
import json

API_URL = "http://localhost:5000"

def test_health():
    print("=" * 50)
    print("TEST 1: Verificare sănătate API")
    print("=" * 50)
    response = requests.get(f"{API_URL}/health")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

def test_chat(mesaj):
    print("\n" + "=" * 50)
    print(f"TEST: {mesaj}")
    print("=" * 50)
    response = requests.post(
        f"{API_URL}/chat/test",
        json={"mesaj": mesaj}
    )
    result = response.json()
    print(f"📝 Mesaj: {result['mesaj']}")
    print(f"🎯 Intenție detectată: {result['intentie_detectata']}")
    print(f"🤖 Model folosit: {result['model_folosit']}")
    print(f"💬 Răspuns: {result['raspuns'][:200]}...")

if __name__ == "__main__":
    test_health()
    
    test_chat("Cum se face pizza acasă?")
    test_chat("Cât timp se coace cozonacul?")
    test_chat("Ce ingrediente pentru sarmale?")
    test_chat("Cu ce înlocuiesc ouăle?")
    test_chat("Salut, ce faci?")
    test_chat("Mulțumesc pentru ajutor!")
