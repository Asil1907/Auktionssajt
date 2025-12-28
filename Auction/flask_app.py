from flask import Flask
from database import init_db
from myblueprints.auctions.auctions_routes import auctions_bp

app = Flask(__name__)
app.secret_key = "secret"

app.register_blueprint(auctions_bp)

init_db(app)

if __name__ == "__main__":
    app.run(debug=True)
