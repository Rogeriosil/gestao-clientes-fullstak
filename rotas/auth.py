# Importa Blueprint para criar um "grupo de rotas"
# request para pegar dados enviados pelo cliente (JSON)
# jsonify para retornar resposta em formato JSON
from flask import Blueprint, request, jsonify

# Função que cria o token JWT após login
from flask_jwt_extended import create_access_token

# Importa a instância do banco criada no app.py
from app import db

# Importa o modelo Usuario (tabela do banco)
from modelos import Usuario


# Cria um Blueprint chamado "auth"
# url_prefix="/auth" significa que todas as rotas aqui começam com /auth
# Exemplo: /auth/registrar, /auth/login
bp_auth = Blueprint("auth", __name__, url_prefix="/auth")


# ---------------------------
# ROTA DE REGISTRO
# ---------------------------
@bp_auth.post("/registrar")
def registrar():

    # Pega o JSON enviado pelo cliente
    # silent=True evita erro se não vier JSON
    dados = request.get_json(silent=True) or {}

    # Extrai email e senha do JSON
    # strip() remove espaços
    # lower() padroniza em minúsculo
    email = (dados.get("email") or "").strip().lower()
    senha = dados.get("senha") or ""

    # Validação básica
    # Se email ou senha não existirem ou senha for menor que 6 caracteres
    if not email or not senha or len(senha) < 6:
        return jsonify({"erro": "Informe email e senha (mínimo 6 caracteres)."}), 400

    # Verifica se já existe usuário com esse email
    if Usuario.query.filter_by(email=email).first():
        return jsonify({"erro": "Email já cadastrado."}), 409

    # Cria novo usuário
    usuario = Usuario(email=email)

    # Define a senha (provavelmente faz hash da senha)
    # Essa função deve estar dentro do modelo Usuario
    usuario.definir_senha(senha)

    # Adiciona no banco
    db.session.add(usuario)

    # Confirma no banco (salva de verdade)
    db.session.commit()

    # Retorna sucesso
    return jsonify({"mensagem": "Usuário criado com sucesso."}), 201


# ---------------------------
# ROTA DE LOGIN
# ---------------------------
@bp_auth.post("/login")
def login():

    # Pega dados enviados
    dados = request.get_json(silent=True) or {}

    email = (dados.get("email") or "").strip().lower()
    senha = dados.get("senha") or ""

    # Busca usuário no banco pelo email
    usuario = Usuario.query.filter_by(email=email).first()

    # Se usuário não existir ou senha estiver errada
    # verificar_senha provavelmente compara hash
    if not usuario or not usuario.verificar_senha(senha):
        return jsonify({"erro": "Credenciais inválidas."}), 401

    # Cria o token JWT
    # identity=str(usuario.id) → identifica o usuário pelo ID
    # additional_claims adiciona informações extras no token
    token = create_access_token(
        identity=str(usuario.id),
        additional_claims={"email": usuario.email}
    )

    # Retorna o token para o frontend
    return jsonify({"access_token": token})
