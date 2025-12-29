import sqlite3
from flask import g

DATABASE = "auction.db"

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop("db", None)
    if db:
        db.close()

def init_db(app):
    app.teardown_appcontext(close_db)
    with app.app_context():
        db = get_db()
        # Kontrollera om tabellerna redan finns
        tables = db.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='auctions'"
        ).fetchone()
        
        # Kör bara schema.sql om tabellerna inte finns
        if not tables:
            with open("schema.sql", encoding="utf-8") as f:
                db.executescript(f.read())
