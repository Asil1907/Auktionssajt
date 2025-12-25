# myblueprints/auctions/__init__.py
"""
Blueprint för auktionsfunktionalitet.
"""
from flask import Blueprint

# Skapa blueprint för auktioner
auctions_bp = Blueprint('auctions', __name__, 
                       url_prefix='/auctions',
                       template_folder='templates')

# TODO: Importera routes när de är skapade
# from . import auctions_routes
