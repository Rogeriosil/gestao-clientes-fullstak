import os
from datetime import timedelta
from flask import Flask, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    load_dotenv()
    app = Flask(__name__, static_folder="web/static", template_folder="web")

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "dev-jwt-secret")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=8)

    database_url = os.getenv("DATABASE_URL", "sqlite:///dados.sqlite3")
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    jwt.init_app(app)

    from rotas.auth import bp_auth
    from rotas.clientes import bp_clientes

    app.register_blueprint(bp_auth)
    app.register_blueprint(bp_clientes)

    @app.get("/api")
    def raiz_api():
        return jsonify({"status": "ok", "projeto": "API de Gestão de Clientes (Fullstack)"})

    # --- Front-end ---
    @app.get("/")
    def home():
        return send_from_directory("web", "index.html")

    @app.get("/static/<path:filename>")
    def static_files(filename):
        return send_from_directory("web/static", filename)

    with app.app_context():
        from modelos import Usuario, Cliente  # noqa: F401
        db.create_all()

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
