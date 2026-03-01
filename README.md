# Friday Night API

Backend do **Friday Night** — assistente pessoal de finanças, construído com **FastAPI**, **SQLModel** e **Supabase Auth**.

## Stack

- Python 3.12+
- FastAPI
- SQLModel + SQLAlchemy (async) + asyncpg
- PostgreSQL (schema `finance`)
- Supabase Auth (JWT)
- Alembic
- uv

## Estrutura do projeto

```text
app/
  api/
    deps/           # DI: get_db, get_current_user, get_*_service
    versions/v1/    # Registro de rotas (finance.py agrega todos os routers financeiros)
    router.py       # Monta prefixo /api
  core/
    config.py       # pydantic-settings (DATABASE_URL, SUPABASE_*, DB_ECHO)
    database.py     # Engine e session async
    exception.py    # FridayNightException base
  modules/
    auth/           # signup/login via Supabase SDK
    user/           # perfil do usuário (CRUD)
    finance/
      accounts/             # contas bancárias/investimento/carteira
      cards/                # cartões vinculados a contas bancárias
      categories/           # categorias de transação (outcome/income)
      subcategories/        # subcategorias
      tags/                 # tag = categoria + subcategoria
      currencies/           # moedas fiat e crypto
      financial_institutions/  # bancos e corretoras
      payment_methods/      # formas de pagamento
      transactions/         # lançamentos financeiros
      holdings/             # ativos de investimento vinculados a transações
alembic/            # migrações de banco de dados
tests/              # testes com pytest
```

Cada sub-módulo de `finance/` segue o padrão de 5 arquivos:

```text
model.py       → tabela SQLModel
schemas.py     → schemas Pydantic (Create / Response)
repo.py        → acesso ao banco (repository pattern)
service.py     → lógica de negócio
router.py      → endpoints FastAPI
exceptions.py  → exceções do módulo
```

## Pré-requisitos

- Python >= 3.12
- PostgreSQL disponível
- Projeto Supabase configurado
- [uv](https://docs.astral.sh/uv/)

## Variáveis de ambiente

Crie um arquivo `.env` na raiz:

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/friday_night
DIRECT_URL=postgresql://user:password@localhost:5432/friday_night

SUPABASE_URL=https://<seu-projeto>.supabase.co
SUPABASE_SERVICE_ROLE_KEY=<sua-service-role-key>
SUPABASE_JWT_SECRET=<seu-jwt-secret>

DB_ECHO=false

# Opcional — default: ["http://localhost:5173"]
CORS_ORIGINS=["http://localhost:5173","http://localhost:3000"]
```

## Como executar

### Desenvolvimento local

```bash
uv sync                                       # instalar dependências
alembic upgrade head                          # rodar migrações
uv run uvicorn app.main:app --reload          # subir API
```

API disponível em `http://localhost:8000`.
Swagger UI: `http://localhost:8000/docs` — ReDoc: `http://localhost:8000/redoc`

### Docker

```bash
docker build -t friday-night-api .
docker run --env-file .env -p 8000:8000 friday-night-api
```

Ou via docker-compose na raiz do monorepo:

```bash
docker compose up api
```

Para rodar as migrações no container:

```bash
docker compose exec api uv run alembic upgrade head
```

## Comandos úteis

```bash
uv run pytest                                 # todos os testes
uv run pytest tests/test_accounts.py          # arquivo específico
uv run pytest tests/test_accounts.py::test_fn # teste específico
ruff check .                                  # lint
ruff format .                                 # format
pyright .                                     # type check
alembic revision --autogenerate -m "msg"      # gerar migração
alembic upgrade head                          # aplicar migrações
```

## Endpoints — `/api/v1`

Rotas protegidas exigem `Authorization: Bearer <access_token>`.

### Auth

| Método | Rota         | Descrição                    |
| ------ | ------------ | ---------------------------- |
| POST   | /auth/signup | Cadastrar usuário            |
| POST   | /auth/login  | Login — retorna access_token |

### Usuários 🔒

| Método | Rota      | Descrição        |
| ------ | --------- | ---------------- |
| GET    | /users/me | Dados do usuário |
| PATCH  | /users/me | Atualizar perfil |
| DELETE | /users/me | Deletar conta    |

### Instituições Financeiras

| Método | Rota                                 | Descrição                  |
| ------ | ------------------------------------ | -------------------------- |
| POST   | /finance/financial-institutions      | Criar instituição          |
| GET    | /finance/financial-institutions      | Listar (filtro por `type`) |
| GET    | /finance/financial-institutions/{id} | Buscar por ID              |

### Contas 🔒

| Método | Rota                            | Descrição     |
| ------ | ------------------------------- | ------------- |
| POST   | /finance/accounts               | Criar conta   |
| GET    | /finance/accounts               | Listar contas |
| GET    | /finance/accounts/{id}          | Buscar por ID |
| PATCH  | /finance/accounts/{id}/archive  | Arquivar      |
| PATCH  | /finance/accounts/{id}/activate | Ativar        |

### Cartões 🔒

| Método | Rota                | Descrição                        |
| ------ | ------------------- | -------------------------------- |
| POST   | /finance/cards      | Criar cartão                     |
| GET    | /finance/cards      | Listar por conta (`?account_id`) |
| GET    | /finance/cards/{id} | Buscar por ID                    |
| DELETE | /finance/cards/{id} | Deletar cartão                   |

Campos: `label`, `flag` (visa/mastercard), `close_day`, `due_day`, `limit`.

### Categorias 🔒

| Método | Rota                     | Descrição       |
| ------ | ------------------------ | --------------- |
| POST   | /finance/categories      | Criar categoria |
| GET    | /finance/categories      | Listar          |
| GET    | /finance/categories/{id} | Buscar por ID   |

### Subcategorias 🔒

| Método | Rota                                      | Descrição            |
| ------ | ----------------------------------------- | -------------------- |
| POST   | /finance/subcategories                    | Criar subcategoria   |
| GET    | /finance/subcategories/{id}               | Buscar por ID        |
| GET    | /finance/subcategories/list/{category_id} | Listar por categoria |

### Tags 🔒

| Método | Rota                          | Descrição               |
| ------ | ----------------------------- | ----------------------- |
| POST   | /finance/tags                 | Criar tag               |
| GET    | /finance/tags                 | Listar (`?active=true`) |
| GET    | /finance/tags/{id}            | Buscar por ID           |
| PATCH  | /finance/tags/{id}/activate   | Ativar                  |
| PATCH  | /finance/tags/{id}/deactivate | Desativar               |

### Métodos de Pagamento 🔒

| Método | Rota                                     | Descrição     |
| ------ | ---------------------------------------- | ------------- |
| POST   | /finance/payment-methods                 | Criar         |
| GET    | /finance/payment-methods                 | Listar        |
| GET    | /finance/payment-methods/{id}            | Buscar por ID |
| PATCH  | /finance/payment-methods/{id}/activate   | Ativar        |
| PATCH  | /finance/payment-methods/{id}/deactivate | Desativar     |

### Moedas 🔒

| Método | Rota                | Descrição                    |
| ------ | ------------------- | ---------------------------- |
| POST   | /finance/currencies | Criar moeda                  |
| GET    | /finance/currencies | Listar (`type`: fiat/cripto) |

### Transações 🔒

| Método | Rota                  | Descrição        |
| ------ | --------------------- | ---------------- |
| POST   | /finance/transactions | Criar transação  |
| GET    | /finance/transactions | Listar por conta |

### Holdings 🔒

| Método | Rota              | Descrição     |
| ------ | ----------------- | ------------- |
| POST   | /finance/holdings | Criar holding |

## Convenções

- **IDs**: UUID v7 (time-ordered)
- **Paginação**: `fastapi-pagination` → `{ items, total, page, size, pages }` em todos os GETs de listagem
- **Valores monetários**: `Decimal` serializado como string (até 28 dígitos, 6 casas decimais)
- **Datas**: retornadas no timezone local via `to_local()`
- **Erros de aplicação**: `{ "error": "NomeDoErro", "message": "..." }`
- **Erros de auth**: `{ "message": "...", "detail": "..." }`
- **Token expirado**: 401 com `{ "detail": "Sessão expirada" }`

## Licença

Este projeto está sob a licença definida no arquivo `LICENSE`.
