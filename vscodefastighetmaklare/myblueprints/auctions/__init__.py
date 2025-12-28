# myblueprints/auctions/__init__.py
"""
🔨 AUCTIONS BLUEPRINT - Initiering av Blueprint för auktionsfunktionalitet.

SYFTE: Denna fil initierar Blueprintet för auktionsmodulen.
Ett Blueprint är en Flask-komponent som grupperar relaterade routes, 
templates och statiska filer.

DESIGNMÖNSTER: Blueprint Pattern
- Separerar auktionsfunktionalitet från huvudapplikationen
- Gör koden modulär och återanvändbar
- Möjliggör att flera utvecklare kan arbeta på olika moduler samtidigt

SINGLE RESPONSIBILITY: 
- Skapa Blueprint-objektet
- (Framtida) Importera routes när de implementeras
"""

# Importera Flask's Blueprint-klass
from flask import Blueprint

# ============================================================
# SKAPA BLUEPRINT
# ============================================================
# Blueprint('name', __name__, konfiguration...)
# 
# Parametrar:
# - 'auctions' = Namnet på blueprintet (används i url_for('auctions.route_name'))
# - __name__ = Anger var blueprintet finns (hjälper Flask hitta templates/static)
# - url_prefix = Alla routes i detta blueprint kommer att börja med '/auctions'
#   Exempel: Om du har en route @auctions_bp.route('/list'), 
#            blir den fullständiga URL:en '/auctions/list'
# - template_folder = Blueprintet letar efter templates i 'templates/'-mappen
#   relativ till denna fil
auctions_bp = Blueprint(
    'auctions',              # Blueprint-namn
    __name__,                # Modul-namn
    url_prefix='/auctions',  # URL-prefix för alla routes
    template_folder='templates'  # Mapp för HTML-templates
)

# ============================================================
# IMPORTERA ROUTES (När de är skapade)
# ============================================================
# När auctions_routes.py är implementerad, avkommentera denna rad:
# from . import auctions_routes
# 
# Detta importerar alla @auctions_bp.route() dekoratorer från routes-filen
# och kopplar dem till detta blueprint.
# 
# VIKTIGT: Denna import måste komma EFTER att blueprintet skapats,
# eftersom routes-filen kommer att använda 'auctions_bp' objektet.
