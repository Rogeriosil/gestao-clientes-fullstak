# Importa funções de segurança para trabalhar com senha
# generate_password_hash → transforma senha em hash seguro
# check_password_hash → verifica se a senha digitada corresponde ao hash salvo
from werkzeug.security import generate_password_hash, check_password_hash

# Importa a instância do banco criada no app.py
# Esse db já está conectado ao Flask e ao banco configurado
from app import db


# ==============================
# MODELO DE USUÁRIO (LOGIN)
# ==============================
class Usuario(db.Model):

    # Nome da tabela no banco de dados
    __tablename__ = "usuarios"

    # ID único do usuário (chave primária)
    id = db.Column(db.Integer, primary_key=True)

    # Email do usuário
    # unique=True → não permite emails repetidos
    # nullable=False → campo obrigatório
    # index=True → melhora performance de busca
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)

    # Aqui NÃO salvamos a senha real!
    # Salvamos apenas o HASH da senha (segurança)
    senha_hash = db.Column(db.String(255), nullable=False)

    # Define a senha do usuário convertendo para hash
    def definir_senha(self, senha: str) -> None:
        # Gera hash seguro da senha e salva no banco
        self.senha_hash = generate_password_hash(senha)

    # Verifica se a senha digitada está correta
    def verificar_senha(self, senha: str) -> bool:
        # Compara senha digitada com o hash salvo
        return check_password_hash(self.senha_hash, senha)


# ==============================
# MODELO DE CLIENTE (CRUD)
# ==============================
class Cliente(db.Model):

    # Nome da tabela no banco
    __tablename__ = "clientes"

    # ID único do cliente
    id = db.Column(db.Integer, primary_key=True)

    # Nome do cliente (obrigatório)
    nome = db.Column(db.String(120), nullable=False)

    # Email do cliente
    # Pode ser vazio (nullable=True)
    # Não pode repetir (unique=True)
    email = db.Column(db.String(255), unique=True, nullable=True, index=True)

    # Telefone opcional
    telefone = db.Column(db.String(40), nullable=True)

    # Data de criação automática no banco
    # server_default=db.func.now() → banco preenche automaticamente
    criado_em = db.Column(db.DateTime, server_default=db.func.now())

    # Converte objeto Cliente para dicionário
    # Usado para retornar JSON na API
    def para_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "telefone": self.telefone,

            # Converte datetime para string ISO (necessário para JSON)
            "criado_em": None if self.criado_em is None else self.criado_em.isoformat(),
        }
