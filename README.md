# Friday Night API

API backend construída com **FastAPI**, **SQLModel** e **Supabase Auth** para autenticação de usuários.

## ✨ Visão geral

O projeto expõe endpoints versionados em `/api/v1` para:

- Cadastro (`signup`) e login (`login`) de usuários usando Supabase.
- Consulta do usuário autenticado.
- Atualização de perfil do usuário autenticado.

A aplicação também inclui:

- Configuração via variáveis de ambiente com `pydantic-settings`.
- Banco de dados assíncrono com SQLAlchemy/SQLModel.
- Migrações com Alembic.

## 🧱 Stack principal

- Python 3.12+
- FastAPI
- SQLModel + SQLAlchemy (async)
- PostgreSQL (`asyncpg`)
- Supabase Python SDK
- Alembic

## 📁 Estrutura do projeto

```text
app/
  api/
    deps/           # Dependências de autenticação, DB e serviços
    versions/       # Versionamento de rotas (v1)
    router.py       # Roteador principal (/api)
  core/
    config.py       # Settings e variáveis de ambiente
    database.py     # Engine e session async
    exception.py    # Exceções base da aplicação
  domain/
    user/           # Model, service, repo e rotas de usuário
  use_cases/
    auth/           # Caso de uso de autenticação (signup/login)
  main.py           # Inicialização da aplicação FastAPI
alembic/            # Migrações de banco
```

## ⚙️ Pré-requisitos

- Python `>= 3.12`
- PostgreSQL disponível
- Projeto Supabase configurado
- [uv](https://docs.astral.sh/uv/) (recomendado) ou `pip`

## 🔐 Variáveis de ambiente

Crie um arquivo `.env` na raiz com os campos abaixo:

```env
PROJECT_NAME=Friday Night API

DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/friday_night
DIRECT_URL=postgresql://user:password@localhost:5432/friday_night

SUPABASE_URL=https://<seu-projeto>.supabase.co
SUPABASE_SERVICE_ROLE_KEY=<sua-service-role-key>
SUPABASE_JWT_SECRET=<seu-jwt-secret>

DB_ECHO=false
```

## 🚀 Como executar localmente

### 1) Instalar dependências

Com `uv`:

```bash
uv sync
```

Ou com `pip`:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

### 2) Rodar migrações

```bash
alembic upgrade head
```

### 3) Subir a API

```bash
uv run uvicorn app.main:app --reload
```

A API ficará disponível em `http://127.0.0.1:8000`.

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## 📡 Endpoints principais

Base URL: `/api/v1`

### Auth

- `POST /auth/signup`
  - Cria usuário no Supabase.
  - Body:

```json
{
  "email": "user@example.com",
  "password": "senha_forte",
  "first_name": "Nome",
  "last_name": "Sobrenome"
}
```

- `POST /auth/login`
  - Autentica usuário e retorna token bearer.
  - Body:

```json
{
  "email": "user@example.com",
  "password": "senha_forte"
}
```

### Usuário

> Requer header `Authorization: Bearer <token>`

- `GET /users/me` — retorna usuário autenticado.
- `PATCH /users/me` — atualiza dados do perfil (`first_name`, `last_name`, `avatar_url`, `language`).

## 🧪 Desenvolvimento

Dependências de desenvolvimento já estão declaradas no `pyproject.toml` (pytest, ruff, pyright etc.).

Exemplo para rodar testes quando disponíveis:

```bash
uv run pytest
```

## 📜 Licença

Este projeto está sob a licença definida no arquivo `LICENSE`.
