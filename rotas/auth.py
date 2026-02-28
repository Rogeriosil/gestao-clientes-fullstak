from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app import db
from modelos import Usuario

bp_auth = Blueprint("auth", __name__, url_prefix="/auth")

@bp_auth.post("/registrar")
def registrar():
    dados = request.get_json(silent=True) or {}
    email = (dados.get("email") or "").strip().lower()
    senha = dados.get("senha") or ""

    if not email or not senha or len(senha) < 6:
        return jsonify({"erro": "Informe email e senha (mínimo 6 caracteres)."}), 400

    if Usuario.query.filter_by(email=email).first():
        return jsonify({"erro": "Email já cadastrado."}), 409

    usuario = Usuario(email=email)
    usuario.definir_senha(senha)
    db.session.add(usuario)
    db.session.commit()
    return jsonify({"mensagem": "Usuário criado com sucesso."}), 201

@bp_auth.post("/login")
def login():
    dados = request.get_json(silent=True) or {}
    email = (dados.get("email") or "").strip().lower()
    senha = dados.get("senha") or ""

    usuario = Usuario.query.filter_by(email=email).first()
    if not usuario or not usuario.verificar_senha(senha):
        return jsonify({"erro": "Credenciais inválidas."}), 401

    token = create_access_token(identity=str(usuario.id), additional_claims={"email": usuario.email})
    return jsonify({"access_token": token})
