# FastAPI URL Shortener API

API de encurtamento de URLs desenvolvida com **FastAPI**, utilizando **PostgreSQL** como banco de dados, **Redis** para cache e **rate limiting**.

Projeto criado para estudo de arquitetura backend moderna e práticas profissionais de deploy com Docker.

---

## Tecnologias

- **FastAPI** – Framework principal da API
- **PostgreSQL** – Banco de dados relacional
- **SQLAlchemy** – ORM para PostgreSQL
- **Redis** – Cache e Rate Limit
- **SlowAPI** – Limitação de requisições via Redis
- **Pydantic** – Validação de dados
- **Python-dotenv** – Gerenciamento de variáveis de ambiente
- **Uvicorn** – Servidor ASGI
- **Docker / Docker Compose** – Containerização

---

## Funcionalidades

- Criação e listagem de URLs encurtadas
- Cache de URLs com Redis para performance
- Limitação de requisições (Rate Limit) por IP via Redis
- Suporte a Docker e Docker Compose para deploy rápido

---

## Arquitetura

Client
│
▼ Routers (FastAPI)
│
▼ Service Layer (Regras de negócio)
│
▼ Repositories (Acesso aos dados)
│
▼ Models (SQLAlchemy ORM)
│
▼ PostgreSQL + Redis

## Rodando o projeto

Clone o repositório:

```bash
git clone https://github.com/seuuser/fastapi-url-shortener-api
cd fastapi-url-shortener-api

Instale as dependências:

pip install -r requirements.txt

## Rodando com Docker

O projeto já vem configurado com Docker e Docker Compose, incluindo PostgreSQL e Redis:

docker compose up --build

A API só inicia quando o PostgreSQL e o Redis estiverem prontos, graças ao wait-for-it.sh.

## Executando a API

Para rodar sem Docker (apenas para desenvolvimento):

uvicorn app.main:app --reload

Swagger UI: http://127.0.0.1:8000/docs

ReDoc: http://127.0.0.1:8000/redoc

## Estrutura do projeto

app/
├── main.py
├── models/
├── schemas/
├── repositories/
├── services/
├── routers/
├── core/
└── utils/
