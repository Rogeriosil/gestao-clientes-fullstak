# Projeto 1 — API de Gestão de Clientes (Backend + Front-end)

Sistema completo com **API REST** + **Front-end Web** (sem precisar instalar Node).
O front consome a API via `fetch`, faz login, cria/lista/edita/deleta clientes.

## ✅ Stack
- Python 3.10+
- Flask
- Flask-SQLAlchemy
- JWT (Flask-JWT-Extended)
- SQLite (padrão) — opcional MySQL via `DATABASE_URL`
- Front-end: HTML + JS (vanilla) servido pelo próprio Flask

## 📌 Funcionalidades
### Autenticação
- `POST /auth/registrar`
- `POST /auth/login`

### Clientes (JWT obrigatório)
- `POST /clientes`
- `GET /clientes`
- `GET /clientes/<id>`
- `PUT /clientes/<id>`
- `DELETE /clientes/<id>`

### Front-end (Web)
- `GET /` abre a tela
- Login
- Lista clientes
- Criar cliente
- Editar cliente
- Excluir cliente

## ▶️ Como rodar (Windows / Linux / Mac)
```bash
cd "Projeto_1_API_Gestao_Clientes_Fullstack"
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/Mac: source .venv/bin/activate
pip install -r requirements.txt
python -m flask --app app run --debug
```
Abra no navegador:
- http://127.0.0.1:5000

## 🔐 Usuário de teste
Você pode registrar na tela (Front-end) ou por cURL:

Registrar:
```bash
curl -X POST http://127.0.0.1:5000/auth/registrar -H "Content-Type: application/json" -d "{"email":"admin@teste.com","senha":"123456"}"
```
Login:
```bash
curl -X POST http://127.0.0.1:5000/auth/login -H "Content-Type: application/json" -d "{"email":"admin@teste.com","senha":"123456"}"
```

## ⚙️ Variáveis de ambiente
Copie `.env.example` para `.env` (opcional).
