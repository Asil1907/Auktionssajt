# PythonAnywhere Deployment Guide

## 📋 Förberedelser

### 1. Skapa ett PythonAnywhere-konto
1. Gå till [www.pythonanywhere.com](https://www.pythonanywhere.com)
2. Registrera ett gratis konto
3. Verifiera din e-post

### 2. Förbered projektet för deployment

#### A. Skapa requirements.txt
```bash
# Kör detta i din lokala miljö
pip freeze > requirements.txt
```

Eller skapa manuellt:
```text
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
```

#### B. Uppdatera SECRET_KEY för produktion
I `flask_app.py`, ändra:
```python
# Använd miljövariabel i produktion
import os
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'din_superhemliga_nyckel')
```

## 🚀 Deployment-steg på PythonAnywhere

### Steg 1: Ladda upp filer

#### Alternativ A: Via GitHub (REKOMMENDERAT)
```bash
# 1. Skapa git repo lokalt (om du inte har)
git init
git add .
git commit -m "Initial commit"

# 2. Pusha till GitHub
# (skapa repo på github.com först)
git remote add origin https://github.com/ditt-användarnamn/ditt-repo.git
git push -u origin main
```

På PythonAnywhere:
1. Öppna **Bash Console**
2. Klona repot:
```bash
git clone https://github.com/ditt-användarnamn/ditt-repo.git
cd ditt-repo
```

#### Alternativ B: Via PythonAnywhere File Upload
1. Gå till **Files** tab
2. Ladda upp alla projektfiler manuellt

### Steg 2: Skapa Virtual Environment

I Bash Console:
```bash
# Navigera till din projektmapp
cd ~/ditt-repo/vscodefastighetmaklare

# Skapa virtual environment
python3.10 -m venv venv

# Aktivera
source venv/bin/activate

# Installera beroenden
pip install -r requirements.txt
```

### Steg 3: Konfigurera Web App

1. Gå till **Web** tab
2. Klicka **Add a new web app**
3. Välj **Manual configuration**
4. Välj **Python 3.10**

### Steg 4: Konfigurera WSGI-filen

1. I **Web** tab, klicka på WSGI configuration file länken
2. Ersätt innehållet med:

```python
# /var/www/ditt_användarnamn_pythonanywhere_com_wsgi.py

import sys
import os

# Lägg till projektmappen till Python path
project_home = '/home/ditt_användarnamn/ditt-repo/vscodefastighetmaklare'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Aktivera virtual environment
activate_this = os.path.join(project_home, 'venv/bin/activate_this.py')
# För Python 3.10+ kan activate_this.py saknas, så vi sätter path direkt
venv_path = os.path.join(project_home, 'venv/lib/python3.10/site-packages')
sys.path.insert(0, venv_path)

# Sätt miljövariabel för SECRET_KEY
os.environ['SECRET_KEY'] = 'generera-en-riktigt-hemlig-nyckel-här'

# Importera Flask-appen
from flask_app import app as application
```

### Steg 5: Konfigurera Virtual Environment Path

1. I **Web** tab, scrolla till **Virtualenv** sektionen
2. Sätt path till: `/home/ditt_användarnamn/ditt-repo/vscodefastighetmaklare/venv`

### Steg 6: Konfigurera Static Files (valfritt)

Om du har statiska filer (CSS, JS, bilder):
1. I **Web** tab, scrolla till **Static files**
2. Lägg till mapping:
   - URL: `/static/`
   - Directory: `/home/ditt_användarnamn/ditt-repo/vscodefastighetmaklare/static/`

### Steg 7: Initiera databas

I Bash Console:
```bash
cd ~/ditt-repo/vscodefastighetmaklare
source venv/bin/activate
python3
```

I Python-interpretern:
```python
from flask_app import app
from database import db

with app.app_context():
    db.create_all()
    # Kör seeding-funktioner om du vill
    from models.bostad import skapa_start_bostader
    skapa_start_bostader()

exit()
```

### Steg 8: Starta appen

1. Gå tillbaka till **Web** tab
2. Klicka **Reload** knappen (grön knapp)
3. Din app finns nu på: `http://ditt_användarnamn.pythonanywhere.com`

## 🔧 Felsökning

### Kolla Error Log
1. Gå till **Web** tab
2. Klicka på **Error log** länken
3. Läs felmeddelandena

### Vanliga problem:

**Problem: ModuleNotFoundError**
- Lösning: Kontrollera att alla paket är installerade i virtual environment
- Kör: `pip install -r requirements.txt` igen

**Problem: Database locked**
- Lösning: SQLite kan ha problem med många samtidiga användare
- Överväg att uppgradera till MySQL/PostgreSQL för produktion

**Problem: 404 eller 500-fel**
- Lösning: Kontrollera WSGI-filen och Error log
- Verifiera att paths är korrekta

## 📝 Uppdatera appen

När du gör ändringar:

### Via GitHub:
```bash
# Lokalt
git add .
git commit -m "Beskrivning av ändringar"
git push

# På PythonAnywhere (Bash Console)
cd ~/ditt-repo
git pull
# Reload web app i Web tab
```

### Via File Upload:
1. Ladda upp ändrade filer
2. Klicka **Reload** i Web tab

## 🔒 Säkerhet

### Generera säker SECRET_KEY
```python
import secrets
print(secrets.token_hex(32))
```

Använd denna nyckel i WSGI-filen.

### Databasskydd
- SQLite-databasen ligger i `instance/` mappen
- Den är INTE tillgänglig via web (skyddad automatiskt)

## 💰 Free vs Paid Account

**Free Account begränsningar:**
- 1 web app
- 512 MB diskutrymme
- Daglig CPU-tid begränsning
- Appen "sover" efter inaktivitet (startas vid nästa besök)

**Paid Account fördelar:**
- Flera web apps
- Mer diskutrymme och CPU
- Alltid aktiv
- Custom domains
- HTTPS för custom domains

## 📚 Ytterligare resurser

- [PythonAnywhere Help](https://help.pythonanywhere.com/)
- [Flask Deployment Guide](https://flask.palletsprojects.com/en/3.0.x/deploying/)
- [PythonAnywhere Forums](https://www.pythonanywhere.com/forums/)
