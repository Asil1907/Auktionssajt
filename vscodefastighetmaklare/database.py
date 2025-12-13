"""
💾 DATABASHANTERING (database.py) - En fil för allt som har med databasanslutning att göra.

SINGLE RESPONSIBILITY: Denna fil har ENDAST ansvar för:
1. Skapa SQLAlchemy-objektet (databasanslutningen).
2. Initiera databasen och koppla den till Flask-appen (init_db).
3. Skapa alla tabeller baserat på modellerna (db.create_all).
4. Köra alla startdatafunktioner (seeding).

Denna fil känner INTE till affärslogik eller routing – den är bara databasens centrala nav!
"""
from flask_sqlalchemy import SQLAlchemy

# Skapa SQLAlchemy-instansen. Denna instans är vårt gränssnitt till databasen.
# Detta objekt (db) importeras och används sedan av ALLA modell-klasser (t.ex. Maklare(db.Model)).
db = SQLAlchemy()


def init_db(app):
    """
    Initierar databasen för Flask-applikationen.

    Denna funktion är nödvändig för att SQLAlchemy ska känna till appens konfiguration
    (som databasens anslutnings-URL).

    Args:
        app: Flask-applikationen (Måste vara den instans som skapades i flask_app.py).
    """
    # 1. Koppla db-objektet till vår Flask-app.
    # Nu har db-objektet tillgång till konfigurationen (t.ex. SQLALCHEMY_DATABASE_URI).
    db.init_app(app)

    # 2. Skapa ett App Context.
    # Databasoperationer som att skapa tabeller måste ske inuti en "app-miljö".
    with app.app_context():
        # --- A. Importera alla Modeller ---
        # SQLAlchemy MÅSTE känna till alla modellklasser (Maklare, Bostad, etc.)
        # INNAN den kan skapa tabellerna. Importen säkerställer detta.
        from models.bostad import Bostad


        # --- B. Skapa alla Tabeller ---
        # db.create_all(): Går igenom alla importerade modeller och skapar motsvarande
        # tabeller i databasen om de INTE redan existerar.
        db.create_all()

        # --- C. Fyll Tabellerna med Startdata (Seeding) ---
        # Importera alla funktioner som lägger till startdata i databasen.

        from models.bostad import skapa_start_bostader

        # Kör alla startdata-funktioner för att fylla databasen med initial data.

        skapa_start_bostader()
