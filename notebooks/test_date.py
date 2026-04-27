import pandas as pd
import re
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# 🔹 funcție de curățare
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text

# 1. Încarcă datele de antrenare
df = pd.read_csv('data/processed/date_antrenare.csv')
df['intrebare'] = df['intrebare'].apply(clean_text)

X = df['intrebare']
y = df['intentie']

# 2. Vectorizare + model
vectorizer = TfidfVectorizer(ngram_range=(1,2))
X_vec = vectorizer.fit_transform(X)

model = LogisticRegression(max_iter=1000, class_weight='balanced')
model.fit(X_vec, y)

#  3. Citește conversațiile reale
with open('data/processed/conversatii.log', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("\n🔍 Test pe conversații reale:\n")

for line in lines[:20]:  # primele 20
    text = clean_text(line.strip())
    vec = vectorizer.transform([text])
    pred = model.predict(vec)[0]

    print(f"Text: {line.strip()}")
    print(f"Predicție: {pred}")
    print("-" * 40)
