# WSGI Configuration för PythonAnywhere
"""
Detta är en mall för WSGI-konfigurationsfilen som används på PythonAnywhere.
Kopiera detta innehåll till din WSGI-fil på PythonAnywhere och anpassa paths.
"""

import sys
import os

# ============================================================
# VIKTIGT: Byt ut 'ditt_användarnamn' och 'ditt-repo' nedan!
# ============================================================

# Lägg till projektmappen till Python path
project_home = '/home/ditt_användarnamn/ditt-repo/vscodefastighetmaklare'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Aktivera virtual environment genom att lägga till site-packages
venv_path = os.path.join(project_home, 'venv/lib/python3.10/site-packages')
if venv_path not in sys.path:
    sys.path.insert(0, venv_path)

# ============================================================
# SÄKERHET: Generera en ny SECRET_KEY för produktion!
# Kör i Python: import secrets; print(secrets.token_hex(32))
# ============================================================
os.environ['SECRET_KEY'] = 'generera-en-riktigt-hemlig-nyckel-här-64-tecken-lång'

# Importera Flask-appen
# Viktigt: Vi importerar 'app' från flask_app.py
from flask_app import app as application

# Om du behöver logga något för debugging:
# import logging
# logging.basicConfig(level=logging.DEBUG)
