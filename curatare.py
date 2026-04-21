import json
import unicodedata
import re

def elimina_diacritice(text):
    return ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )

def curata_text(text):
    text = text.lower()
    text = elimina_diacritice(text)
    text = re.sub(r'[^a-z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Test demo
exemple = [
    "Cum se face Pizza Margherita?",
    "Cât se coace cozonacul?",
    "Ce pun în clătite?"
]

for e in exemple:
    print(f"Original: {e}")
    print(f"Curatat: {curata_text(e)}\n")