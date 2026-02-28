from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class Usuario(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    senha_hash = db.Column(db.String(255), nullable=False)

    def definir_senha(self, senha: str) -> None:
        self.senha_hash = generate_password_hash(senha)

    def verificar_senha(self, senha: str) -> bool:
        return check_password_hash(self.senha_hash, senha)

class Cliente(db.Model):
    __tablename__ = "clientes"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=True, index=True)
    telefone = db.Column(db.String(40), nullable=True)
    criado_em = db.Column(db.DateTime, server_default=db.func.now())

    def para_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "telefone": self.telefone,
            "criado_em": None if self.criado_em is None else self.criado_em.isoformat(),
        }
