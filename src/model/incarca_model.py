"""
Script pentru încărcarea rapidă a modelului (folosit de API)
Autor: Carai Maria
"""

import joblib
import os

def incarca_model():
    """Încarcă cel mai recent model antrenat"""
    model_path = 'models/saved/model_latest.pkl'
    
    if not os.path.exists(model_path):
        print(f"❌ Modelul nu există la calea: {model_path}")
        print("   Rulează mai întâi: python src/model/antreneaza_model.py")
        return None
    
    model = joblib.load(model_path)
    print(f"✅ Model încărcat din: {model_path}")
    return model

def prezice_intentie(model, text):
    """Prezice intenția pentru un text dat"""
    if model is None:
        return "necunoscut"
    
    intentie = model.predict([text])[0]
    return intentie

# Test rapid
if __name__ == "__main__":
    model = incarca_model()
    if model:
        test = "Cum se face pizza?"
        intentie = prezice_intentie(model, test)
        print(f"Întrebare: {test}")
        print(f"Intenție detectată: {intentie}")