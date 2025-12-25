# Flask Projekt - Status och Dokumentation

## ✅ Vad som är klart:

### 1. Flask-projekt med Blueprints
- **Huvudfil**: `flask_app.py` - Application Factory Pattern
- **Blueprints**:
  - `myblueprints/bostader/` - Bostadshantering (komplett)
  - `myblueprints/auctions/` - Auktioner (struktur finns, behöver implementeras)

### 2. SQLite-databas
- **Konfiguration**: `database.py`
- **Databastyp**: SQLite (`blgeestates.db`)
- **ORM**: Flask-SQLAlchemy
- **Modeller**: `models/bostad.py` (Bostad-modell finns)

### 3. Repository Pattern
- **Implementerat**: `dbrepositories/bostad_repository.py`
- **CRUD-operationer**: Hämta, skapa, uppdatera, ta bort bostäder
- **Separation of Concerns**: Databaslogik separerad från routes

### 4. Templates
- **Base template**: `templates/base.html` - Bootstrap 5
- **Bostäder**: `myblueprints/bostader/templates/`
  - `bostader_lista.html`
  - `bostad_detalj.html`

## 📋 Projektstruktur:

```
vscodefastighetmaklare/
├── flask_app.py              # Huvudfil (Application Factory)
├── database.py               # Databasinitiering
├── models/
│   └── bostad.py            # Databasmodeller
├── dbrepositories/
│   └── bostad_repository.py # CRUD-operationer (Repository Pattern)
├── myblueprints/
│   ├── bostader/            # Blueprint för bostäder
│   │   ├── __init__.py
│   │   ├── bostader_routes.py
│   │   └── templates/
│   └── auctions/            # Blueprint för auktioner (tom)
│       └── __init__.py
├── templates/               # Globala templates
│   ├── base.html
│   ├── home.html
│   └── index.html
└── instance/                # Databasfil skapas här
```

## 🚀 Kör projektet lokalt:

```bash
# 1. Aktivera virtual environment
.venv\Scripts\Activate  # Windows
source .venv/bin/activate  # Linux/Mac

# 2. Installera beroenden (om inte redan gjort)
pip install flask flask-sqlalchemy

# 3. Kör applikationen
python flask_app.py

# 4. Öppna i webbläsare
# http://127.0.0.1:5000
```

## 🌐 PythonAnywhere Deployment - Nästa steg:

Se `pythonanywhere_setup.md` för detaljerade instruktioner.

## 📝 Att göra:

- [ ] Implementera auctions blueprint (modeller, routes, templates)
- [ ] Lägg till användarautentisering
- [ ] Deploya till PythonAnywhere
- [ ] Konfigurera production SECRET_KEY
- [ ] Sätt upp HTTPS
