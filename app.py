import os
from datetime import timedelta

# Flask: cria o servidor e responde rotas
from flask import Flask, jsonify, send_from_directory

# Banco de dados (ORM): trabalha com tabelas como se fossem classes Python
from flask_sqlalchemy import SQLAlchemy

# JWT: autenticação por token (login gera token; rotas protegidas exigem token)
from flask_jwt_extended import JWTManager

# Carrega variáveis do arquivo .env (SECRET_KEY, DATABASE_URL etc.)
from dotenv import load_dotenv


# Instâncias globais (extensões) - criadas fora e "ligadas" depois no app
db = SQLAlchemy()
jwt = JWTManager()


def create_app():
    # Carrega as variáveis do arquivo .env para o ambiente do sistema
    load_dotenv()

    # Cria a aplicação Flask.
    # static_folder/template_folder apontam para sua pasta "web"
    # (onde ficam index.html, css e js)
    app = Flask(__name__, static_folder="web/static", template_folder="web")

    # Chaves secretas:
    # - SECRET_KEY: protege sessões/assinaturas internas do Flask
    # - JWT_SECRET_KEY: assina os tokens JWT (se mudar, tokens antigos param de funcionar)
    # Se não existir no .env, usa valores "dev-..." (bom só para desenvolvimento)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "dev-jwt-secret")

    # Tempo de validade do token JWT (aqui: 8 horas)
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=8)

    # URL do banco:
    # Por padrão usa SQLite (arquivo local dados.sqlite3)
    # Se você colocar DATABASE_URL no .env, ele usa o que estiver lá
    database_url = os.getenv("DATABASE_URL", "sqlite:///dados.sqlite3")
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url

    # Evita warning e reduz overhead
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # "Conecta" as extensões ao app Flask
    db.init_app(app)
    jwt.init_app(app)

    # Importa os blueprints (pacotes de rotas)
    # auth: rotas de login/registro
    # clientes: rotas CRUD de clientes (normalmente protegidas com JWT)
    from rotas.auth import bp_auth
    from rotas.clientes import bp_clientes

    # Registra os blueprints no app principal
    app.register_blueprint(bp_auth)
    app.register_blueprint(bp_clientes)

    # Endpoint simples para testar se a API está no ar
    @app.get("/api")
    def raiz_api():
        return jsonify({"status": "ok", "projeto": "API de Gestão de Clientes (Fullstack)"})

    # ----------------------
    # FRONT-END (arquivos web)
    # ----------------------

    # Serve o index.html (tela do front)
    @app.get("/")
    def home():
        return send_from_directory("web", "index.html")

    # Serve arquivos estáticos (CSS/JS)
    # Ex: /static/app.js, /static/estilos.css
    @app.get("/static/<path:filename>")
    def static_files(filename):
        return send_from_directory("web/static", filename)

    # Cria as tabelas do banco automaticamente na primeira execução
    # (com base nas classes do arquivo modelos.py)
    with app.app_context():
        from modelos import Usuario, Cliente  # noqa: F401 (import só para registrar os modelos)
        db.create_all()

    # Retorna o app configurado (padrão Factory Pattern)
    return app


# Cria a aplicação chamando a fábrica
app = create_app()

# Se rodar este arquivo diretamente: python app.py
# inicia o servidor Flask em modo debug
if __name__ == "__main__":
    app.run(debug=True)
