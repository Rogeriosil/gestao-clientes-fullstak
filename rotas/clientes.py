# Importa Blueprint (organização de rotas),
# request (dados da requisição),
# jsonify (retornar JSON)
from flask import Blueprint, request, jsonify

# Decorator que protege a rota exigindo token JWT válido
from flask_jwt_extended import jwt_required

# Importa a instância do banco
from app import db

# Importa o modelo Cliente (tabela do banco)
from modelos import Cliente


# Cria um Blueprint chamado "clientes"
# url_prefix="/clientes" significa que todas as rotas começam com /clientes
bp_clientes = Blueprint("clientes", __name__, url_prefix="/clientes")


# -------------------------------
# CRIAR CLIENTE (POST /clientes)
# -------------------------------
@bp_clientes.post("")
@jwt_required()  # exige que o usuário esteja autenticado
def criar_cliente():

    # Pega os dados enviados no corpo da requisição (JSON)
    dados = request.get_json(silent=True) or {}

    # Limpa e trata os campos
    nome = (dados.get("nome") or "").strip()
    email = (dados.get("email") or "").strip().lower() or None
    telefone = (dados.get("telefone") or "").strip() or None

    # Validação: nome é obrigatório
    if not nome:
        return jsonify({"erro": "Campo 'nome' é obrigatório."}), 400

    # Verifica se já existe cliente com o mesmo email
    if email and Cliente.query.filter_by(email=email).first():
        return jsonify({"erro": "Já existe cliente com este email."}), 409

    # Cria objeto Cliente
    cliente = Cliente(nome=nome, email=email, telefone=telefone)

    # Adiciona ao banco
    db.session.add(cliente)

    # Salva no banco
    db.session.commit()

    # Retorna o cliente criado como JSON
    return jsonify(cliente.para_dict()), 201


# --------------------------------
# LISTAR CLIENTES (GET /clientes)
# --------------------------------
@bp_clientes.get("")
@jwt_required()
def listar_clientes():

    # Busca todos os clientes ordenados do mais novo para o mais antigo
    clientes = Cliente.query.order_by(Cliente.id.desc()).all()

    # Converte cada cliente para dicionário (JSON)
    return jsonify([c.para_dict() for c in clientes])


# -----------------------------------------
# OBTER UM CLIENTE (GET /clientes/<id>) 
# -----------------------------------------
@bp_clientes.get("/<int:cliente_id>")
@jwt_required()
def obter_cliente(cliente_id: int):

    # Busca cliente pelo ID ou retorna erro 404 se não existir
    cliente = Cliente.query.get_or_404(cliente_id)

    return jsonify(cliente.para_dict())


# -----------------------------------------
# ATUALIZAR CLIENTE (PUT /clientes/<id>)
# -----------------------------------------
@bp_clientes.put("/<int:cliente_id>")
@jwt_required()
def atualizar_cliente(cliente_id: int):

    # Busca cliente pelo ID ou retorna 404
    cliente = Cliente.query.get_or_404(cliente_id)

    # Pega os dados enviados
    dados = request.get_json(silent=True) or {}

    # Atualiza apenas se o campo foi enviado
    if "nome" in dados:
        cliente.nome = (dados.get("nome") or "").strip()

    if "email" in dados:
        email = (dados.get("email") or "").strip().lower() or None

        # Verifica se o email já está sendo usado por outro cliente
        if email and Cliente.query.filter(
            Cliente.email == email,
            Cliente.id != cliente.id
        ).first():
            return jsonify({"erro": "Email já está em uso por outro cliente."}), 409

        cliente.email = email

    if "telefone" in dados:
        cliente.telefone = (dados.get("telefone") or "").strip() or None

    # Validação final
    if not cliente.nome:
        return jsonify({"erro": "Campo 'nome' não pode ficar vazio."}), 400

    # Salva alterações no banco
    db.session.commit()

    return jsonify(cliente.para_dict())


# -----------------------------------------
# DELETAR CLIENTE (DELETE /clientes/<id>)
# -----------------------------------------
@bp_clientes.delete("/<int:cliente_id>")
@jwt_required()
def deletar_cliente(cliente_id: int):

    # Busca cliente ou retorna 404
    cliente = Cliente.query.get_or_404(cliente_id)

    # Remove do banco
    db.session.delete(cliente)
    db.session.commit()

    return jsonify({"mensagem": "Cliente removido."})
