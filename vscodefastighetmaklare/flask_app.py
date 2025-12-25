# flask_app.py
"""
HUVUDFIL FÖR FLASK-APPLIKATIONEN (Applikationens Nav)

SYFTE: Att initiera och konfigurera alla delar (databaser, inloggning, moduler)
som applikationen behöver för att fungera.

DESIGNPRINCIP: Denna fil följer "Application Factory Pattern" (skapa_app),
vilket är bäst praxis för att skapa en skalbar och testbar Flask-applikation.

SINGLE RESPONSIBILITY:
1. Skapa Flask-applikationen.
2. Konfigurera applikationen (inställningar).
3. Initiera databas och inloggning.
4. Registrera alla blueprints.
5. Definiera routes för huvudnivån (t.ex. startsidan).
6. Starta applikationen.
"""
from flask import Flask, render_template
# Importera init_db-funktionen som sätter upp SQLAlchemy (databasen)
from database import init_db




def skapa_app():
    """
    Application Factory: Skapar och konfigurerar Flask-applikationen.

    Returns:
        Flask: Den färdiga Flask-applikationen-instansen.
    """
    # 1. Skapa Flask-appen
    app = Flask(__name__)

    # ============================================================
    # 2. KONFIGURATION (Applikationsinställningar)
    # ============================================================
    # SECRET_KEY: Nödvändig för att skydda session cookies (inloggning). BYT DENNA I PRODUKTION!
    # Använd miljövariabel för produktion (PythonAnywhere)
    import os
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'din_superhemliga_nyckel')
    # SQLALCHEMY_DATABASE_URI: Anger vilken databas vi ska använda (en SQLite-fil).
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blgeestates.db'
    # SQLALCHEMY_TRACK_MODIFICATIONS: Stängs av för att spara resurser (bäst praxis).
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # ============================================================
    # 3. INITIERA DATABASEN
    # ============================================================
    # init_db: Anropar funktionen som kopplar SQLAlchemy till appen och skapar tabellerna.
    init_db(app)

    # ============================================================
    # 4. REGISTRERA BLUEPRINTS
    # ============================================================
    # Anropar hjälpfunktionen som kopplar alla moduler till appen.
    registrera_blueprints(app)

    # ============================================================
    # 5. REGISTRERA ROUTES (URL:er för hela appen)
    # ============================================================
    # Anropar hjälpfunktionen som definierar startsidor och huvud-rutter.
    create_routes(app)



    return app


def registrera_blueprints(app):
    """
    Registrerar alla blueprints i applikationen.
    Kopplar ihop de separata modulerna (Blueprints) med huvudapplikationen.

    Args:
        app (Flask): Flask-applikationen
    """
    # Importera blueprint-objekten från deras respektive moduler
    from myblueprints.bostader import bostader_bp
    # from myblueprints.auctions import auctions_bp  # Kommenterad tills auctions är implementerat
    #imporetera fler blueprint om det behövs


    # app.register_blueprint: Den faktiska kopplingen sker här.
    # url_prefix: Anger det prefix som alla routes i blueprintet kommer att ha.
    app.register_blueprint(bostader_bp, url_prefix='/bostader')
    # app.register_blueprint(auctions_bp, url_prefix='/auctions')  # Kommenterad tills auctions är implementerat
    #registera fler blueprint om det behövs


def create_routes(app):
    """
    Skapar routes som hör till hela appen (globala routes).

    Args:
        app (Flask): Flask-applikationen
    """

    @app.route("/hello")
    def hello_world():
        """En enkel test-rutt."""
        return "<p>Hej Världen! Min första Flask-app!</p>"

    @app.route('/')
    def index():
        """Startsidan."""
        # render_template: Letar efter home.html i mappen 'templates' i roten
        return render_template('home.html', titel='Välkommen')


# ============================================================
# STARTPUNKT
# ============================================================
# Anropar Application Factory för att bygga hela appen
app = skapa_app()

if __name__ == '__main__':
    # Kör applikationen!
    # debug=True: Aktiverar debug-läget, vilket gör att koden laddas om vid ändring i vscode
    app.run(debug=True)