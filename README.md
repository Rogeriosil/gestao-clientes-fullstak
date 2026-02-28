# Sistema Full Stack de Gestão de Clientes

Aplicação full stack para gerenciamento de clientes desenvolvida utilizando Flask no backend e interface web construída com HTML, CSS e JavaScript puro no frontend. O sistema permite registro de usuários, autenticação com JWT e operações completas de CRUD de clientes através de uma API REST integrada à interface.

O objetivo do projeto é demonstrar a construção completa de uma aplicação web, incluindo backend, autenticação, banco de dados e consumo da API pelo frontend.

## Tecnologias utilizadas

Python 3, Flask, Flask-SQLAlchemy, Flask-JWT-Extended, SQLite, HTML, CSS e JavaScript (Vanilla JS).

## Estrutura e funcionamento

A aplicação é organizada da seguinte forma:

- **app.py**: ponto de entrada da aplicação. Responsável por criar a instância do Flask, configurar o banco de dados, inicializar o JWT e registrar as rotas da API.
- **modelos.py**: define os modelos do banco de dados utilizando SQLAlchemy, incluindo usuários e clientes.
- **rotas/auth.py**: contém as rotas de registro e login, responsáveis pela autenticação e geração do token JWT.
- **rotas/clientes.py**: implementa o CRUD completo de clientes, protegido por autenticação.
- **web/index.html**: interface principal da aplicação exibida no navegador.
- **web/static/app.js**: responsável por realizar as requisições HTTP para a API, gerenciar o token JWT e atualizar os dados na tela.
- **web/static/estilos.css**: define o layout e aparência da interface.
- **instance/**: diretório utilizado pelo Flask para armazenar arquivos locais, como o banco SQLite.

## Funcionamento geral

O usuário realiza o registro informando email e senha. Após o login, a API retorna um token JWT que é utilizado pelo frontend nas requisições seguintes. As rotas de clientes exigem esse token para permitir acesso, garantindo autenticação nas operações.

Rotas principais da API:

POST /auth/registrar  
POST /auth/login  
GET /clientes  
POST /clientes  
PUT /clientes/<id>  
DELETE /clientes/<id>  

## Como executar o projeto

1. Criar ambiente virtual:
python -m venv .venv

2. Ativar o ambiente (Windows):
.venv\Scripts\Activate.ps1

3. Instalar dependências:
pip install -r requirements.txt

4. Executar a aplicação:
python app.py

Acesse no navegador:
http://127.0.0.1:5000

## Objetivo

Projeto desenvolvido para demonstrar conhecimentos full stack, incluindo desenvolvimento backend com Flask, autenticação JWT, manipulação de banco de dados e integração completa entre frontend e API.
