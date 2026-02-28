from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from modelos import Cliente

bp_clientes = Blueprint("clientes", __name__, url_prefix="/clientes")

@bp_clientes.post("")
@jwt_required()
def criar_cliente():
    dados = request.get_json(silent=True) or {}
    nome = (dados.get("nome") or "").strip()
    email = (dados.get("email") or "").strip().lower() or None
    telefone = (dados.get("telefone") or "").strip() or None

    if not nome:
        return jsonify({"erro": "Campo 'nome' é obrigatório."}), 400

    if email and Cliente.query.filter_by(email=email).first():
        return jsonify({"erro": "Já existe cliente com este email."}), 409

    cliente = Cliente(nome=nome, email=email, telefone=telefone)
    db.session.add(cliente)
    db.session.commit()
    return jsonify(cliente.para_dict()), 201

@bp_clientes.get("")
@jwt_required()
def listar_clientes():
    clientes = Cliente.query.order_by(Cliente.id.desc()).all()
    return jsonify([c.para_dict() for c in clientes])

@bp_clientes.get("/<int:cliente_id>")
@jwt_required()
def obter_cliente(cliente_id: int):
    cliente = Cliente.query.get_or_404(cliente_id)
    return jsonify(cliente.para_dict())

@bp_clientes.put("/<int:cliente_id>")
@jwt_required()
def atualizar_cliente(cliente_id: int):
    cliente = Cliente.query.get_or_404(cliente_id)
    dados = request.get_json(silent=True) or {}

    if "nome" in dados:
        cliente.nome = (dados.get("nome") or "").strip()
    if "email" in dados:
        email = (dados.get("email") or "").strip().lower() or None
        if email and Cliente.query.filter(Cliente.email == email, Cliente.id != cliente.id).first():
            return jsonify({"erro": "Email já está em uso por outro cliente."}), 409
        cliente.email = email
    if "telefone" in dados:
        cliente.telefone = (dados.get("telefone") or "").strip() or None

    if not cliente.nome:
        return jsonify({"erro": "Campo 'nome' não pode ficar vazio."}), 400

    db.session.commit()
    return jsonify(cliente.para_dict())

@bp_clientes.delete("/<int:cliente_id>")
@jwt_required()
def deletar_cliente(cliente_id: int):
    cliente = Cliente.query.get_or_404(cliente_id)
    db.session.delete(cliente)
    db.session.commit()
    return jsonify({"mensagem": "Cliente removido."})
