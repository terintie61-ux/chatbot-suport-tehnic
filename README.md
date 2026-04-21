# Chatbot Suport Tehnic



## Descriere
Proiect pentru facultate - Un chatbot care răspunde la întrebări culinare.


```markdown
# API Chatbot Culinar - Backend

**Branch:** `feature/backend-api`

---

##  Descriere

Acest modul implementează API-ul RESTful pentru Chatbot-ul Culinar "Bucătarul Virtual". API-ul primește întrebări de la utilizatori și returnează răspunsuri generate pe baza bazei de date culinare.

---

##  Pornirea serverului

### 1. Deschide un terminal (Command Prompt / Terminal)
```bash
cd C:\Users\HOME\Desktop\proiect-chatbot\chatbot-suport-tehnic
python src/api/app.py
```

### 2. Serverul va porni și vei vedea:
```
==================================================
 API CHATBOT CULINAR - 'BUCĂTARUL VIRTUAL'
==================================================
 Răspunsuri încărcate: 100
 Întrebări încărcate: 100
==================================================
 Serverul pornește la http://localhost:5000
 Endpoint-uri disponibile:
   GET  /health  - verifică starea
   GET  /ping    - test rapid
   GET  /stats   - statistici
   POST /chat    - trimite un mesaj
==================================================
```

### 3. Pentru a opri serverul:
Apasă `CTRL + C` în terminal

---

##  Endpoint-uri API

### GET `/health`
Verifică dacă API-ul funcționează.

**Exemplu:**
```bash
curl http://localhost:5000/health
```

**Răspuns:**
```json
{
  "status": "ok",
  "timestamp": "2024-04-01T10:30:00",
  "versiune": "1.0",
  "raspunsuri_incarcate": 100,
  "intrebari_incarcate": 100
}
```

---

### GET `/ping`
Test rapid pentru a verifica dacă serverul răspunde.

**Exemplu:**
```bash
curl http://localhost:5000/ping
```

**Răspuns:**
```json
{
  "pong": "API-ul funcționează!"
}
```

---

### GET `/stats`
Afișează statistici despre datele încărcate.

**Exemplu:**
```bash
curl http://localhost:5000/stats
```

**Răspuns:**
```json
{
  "total_raspunsuri": 100,
  "total_intrebari": 100,
  "categorii_raspunsuri": {
    "retete": 25,
    "ingrediente": 15,
    "timp_preparare": 12,
    "salut": 5,
    "multumesc": 5
  },
  "api_status": "active"
}
```

---

### POST `/chat`
Trimite un mesaj și primește un răspuns de la chatbot.

**Exemplu cu curl:**
```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d "{\"mesaj\":\"Cum se face pizza?\"}"
```

**Exemplu cu PowerShell:**
```powershell
Invoke-RestMethod -Uri http://localhost:5000/chat `
  -Method POST `
  -Body '{"mesaj":"Cum se face pizza?"}' `
  -ContentType "application/json"
```

**Răspuns:**
```json
{
  "mesaj_original": "Cum se face pizza?",
  "raspuns": "Pentru pizza ai nevoie de aluat (făină, apă, drojdie), sos de roșii și mozzarella. Coace la 250°C pentru 12-15 minute.",
  "intentie_detectata": "intrebare_predefinita",
  "timestamp": "2024-04-01T10:30:00"
}
```

---

##  Testare rapidă

### Test 1: Verifică sănătatea API-ului
Deschide browserul și accesează:
```
http://localhost:5000/health
```

### Test 2: Trimite un mesaj
În terminal, rulează:
```bash
curl -X POST http://localhost:5000/chat -H "Content-Type: application/json" -d "{\"mesaj\":\"Salut\"}"
```

### Test 3: Verifică statisticile
```
http://localhost:5000/stats
```

---

## 📁 Structura fișierelor

```
src/api/
├── app.py                 # Aplicația principală Flask
├── data/
│   └── scheme_raspuns.json # Răspunsuri predefinite (100+)
└── logs/
    └── requests.log       # Log-ul cererilor (se generează automat)
```

---

##  Dependențe

Asigură-te că ai instalat pachetele necesare:

```bash
pip install flask==2.3.0
pip install flask-cors==4.0.0
```

Sau rulează:
```bash
pip install -r requirements.txt
```

---

##  Depanare (Troubleshooting)

### Eroare: "ModuleNotFoundError: No module named 'flask'"
**Soluție:**
```bash
pip install flask flask-cors
```

### Eroare: "FileNotFoundError: scheme_raspuns.json"
**Soluție:**
Verifică dacă fișierul există:
```bash
dir src\api\data\
```
Dacă nu există, creează folderul și adaugă fișierul:
```bash
mkdir src\api\data
# Copiază scheme_raspuns.json în src/api/data/
```

### Eroare: "Port 5000 already in use"
**Soluție:**
Oprește orice program care folosește portul 5000 sau schimbă portul în `app.py`:
```python
app.run(debug=True, port=5001)
```

### Eroare: "Access is denied" la scrierea în logs
**Soluție:**
Creează manual folderul logs:
```bash
mkdir src\api\logs
```

---

##  Integrare cu Frontend

Pentru ca Debora (frontend) să poată folosi API-ul, aceasta va face cereri la:
```
http://localhost:5000/chat
```

**Exemplu de cod JavaScript pentru frontend:**
```javascript
fetch('http://localhost:5000/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ mesaj: "Cum se face pizza?" })
})
.then(response => response.json())
.then(data => console.log(data.raspuns));
```

---

##  Log-uri

Toate cererile sunt salvate în `src/api/logs/requests.log` pentru debugging.

**Exemplu de log:**
```
2024-04-01T10:30:00 - cum se face pizza?
2024-04-01T10:31:00 - salut
2024-04-01T10:32:00 - mulțumesc
```

---

##  Checklist pentru Vasilache Dumitru

- [ ] Serverul pornește fără erori (`python src/api/app.py`)
- [ ] Endpoint-ul `/health` funcționează
- [ ] Endpoint-ul `/ping` funcționează
- [ ] Endpoint-ul `/stats` funcționează
- [ ] Endpoint-ul `/chat` returnează răspunsuri corecte
- [ ] Răspunsurile sunt încărcate din JSON
- [ ] Log-urile se scriu corect
- [ ] Codul este în Git pe branch-ul `feature/backend-api`

---

**Ultima actualizare:** 1 Aprilie 2024
```
