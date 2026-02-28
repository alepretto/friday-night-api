# Friday Night API — Contexto para Integração Frontend

## Visão Geral

- **Framework**: FastAPI (Python)
- **Autenticação**: Supabase Auth (JWT Bearer Token)
- **Base URL**: `http://localhost:8000`
- **Prefixo global**: `/api/v1`
- **CORS**: `http://localhost:5173` (Vite dev server)
- **Paginação**: `fastapi-pagination` (todos os endpoints de listagem)

---

## Autenticação

Todas as rotas protegidas exigem header:
```
Authorization: Bearer <access_token>
```

O `access_token` é retornado pelo endpoint de login e é um JWT do Supabase.

---

## Formato de Erros

### Erros da aplicação (`FridayNightException`)
```json
{
  "error": "NomeDoErro",
  "message": "Descrição do problema"
}
```

### Erros de autenticação Supabase
```json
{
  "message": "Error de validação",
  "detail": "..."
}
```

### Erros HTTP padrão (401, 403, 404)
```json
{
  "detail": "Mensagem de erro"
}
```

---

## Formato de Paginação

Todos os endpoints `GET` de listagem retornam:
```json
{
  "items": [...],
  "total": 100,
  "page": 1,
  "size": 50,
  "pages": 2
}
```

Query params de paginação: `?page=1&size=50`

---

## Endpoints

### AUTH — `/api/v1/auth`

#### `POST /api/v1/auth/signup` — Cadastro
**Body:**
```json
{
  "email": "user@email.com",
  "password": "senha123",
  "first_name": "João",
  "last_name": "Silva"
}
```
**Response:**
```json
{
  "message": "Usuário criado. Verifique o e-mail se necessário",
  "user": { ...supabase_user_object }
}
```

#### `POST /api/v1/auth/login` — Login
**Body:**
```json
{
  "email": "user@email.com",
  "password": "senha123"
}
```
**Response:**
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "user": { ...supabase_user_object }
}
```

---

### USERS — `/api/v1/users` 🔒

#### `GET /api/v1/users/me` — Dados do usuário logado
**Response:**
```json
{
  "id": "uuid",
  "email": "user@email.com",
  "first_name": "João",
  "last_name": "Silva",
  "username": null,
  "avatar_url": null,
  "language": "pt-br",
  "is_premium": false,
  "is_active": true,
  "role": "user",
  "telegram_id": null,
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### `PATCH /api/v1/users/me` — Atualizar perfil
**Body (todos opcionais):**
```json
{
  "first_name": "João",
  "last_name": "Silva",
  "avatar_url": "https://...",
  "language": "pt-br"
}
```

#### `DELETE /api/v1/users/me` — Deletar conta
**Response:** `204 No Content`

---

### FINANCIAL INSTITUTIONS — `/api/v1/finance/financial-institutions`

> **Não requer autenticação** nas rotas de leitura/criação (dados globais do sistema)

#### `POST /api/v1/finance/financial-institutions`
**Body:**
```json
{
  "name": "Nubank",
  "type": "fintech",
  "icon_url": "https://..."
}
```
**Response:**
```json
{
  "id": "uuid",
  "name": "Nubank",
  "type": "fintech",
  "icon_url": "https://...",
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### `GET /api/v1/finance/financial-institutions` — Listar
**Query params:** `?type=bank` (opcional), `?page=1&size=50`

**Enum `type`:** `bank` | `fintech` | `broker` | `exchange` | `wallet`

---

### CURRENCIES — `/api/v1/finance/currencies`

> Dados globais (moedas/criptomoedas do sistema). `POST` requer autenticação 🔒. `GET` é público.

**Enum `type`:** `fiat` | `cripto`

#### `POST /api/v1/finance/currencies` 🔒
**Body:**
```json
{
  "label": "Real Brasileiro",
  "symbol": "BRL",
  "type": "fiat"
}
```
**Response `201`:**
```json
{
  "id": "uuid",
  "label": "Real Brasileiro",
  "symbol": "BRL",
  "type": "fiat",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

#### `GET /api/v1/finance/currencies/{currency_id}` — Buscar por ID
**Response `200`:** objeto `CurrencyResponse` | **`404`** se não encontrado

#### `GET /api/v1/finance/currencies` — Listar (paginado)
**Query params (todos opcionais):**
- `label=real` — busca case-insensitive por substring no label
- `symbol=BRL` — busca case-insensitive por substring no symbol
- `type=fiat` — filtro exato pelo tipo
- `page=1&size=50`

---

### ACCOUNTS — `/api/v1/finance/accounts` 🔒

#### `POST /api/v1/finance/accounts`
**Body:**
```json
{
  "financial_institution_id": "uuid",
  "status": "activate",
  "type": "bank",
  "subtype": "corrente"
}
```
**Response:**
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "financial_institution_id": "uuid",
  "status": "activate",
  "type": "bank",
  "subtype": "corrente",
  "created_at": "...",
  "updated_at": "..."
}
```

**Enum `status`:** `activate` | `deactivate`

**Enum `type`:** `bank` | `investment` | `cash` | `benefit`

#### `GET /api/v1/finance/accounts` — Listar contas do usuário
**Query params (todos opcionais):**
- `financial_institution_id=uuid`
- `status=activate`
- `type=bank`
- `page=1&size=50`

---

### CATEGORIES — `/api/v1/finance/categories` 🔒

#### `POST /api/v1/finance/categories`
**Body:**
```json
{
  "label": "Alimentação",
  "type": "outcome"
}
```
**Response:**
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "label": "Alimentação",
  "type": "outcome",
  "created_at": "...",
  "updated_at": "..."
}
```

**Enum `type`:** `outcome` | `income`

#### `GET /api/v1/finance/categories/{id_category}` — Buscar por ID

#### `GET /api/v1/finance/categories` — Listar (paginado)

---

### SUBCATEGORIES — `/api/v1/finance/subcategories` 🔒

#### `POST /api/v1/finance/subcategories`
**Body:**
```json
{
  "category_id": "uuid",
  "label": "Restaurante"
}
```
**Response:**
```json
{
  "id": "uuid",
  "created_at": "...",
  "updated_at": "..."
}
```

#### `GET /api/v1/finance/subcategories/{subcategory_id}` — Buscar por ID

#### `GET /api/v1/finance/subcategories/list/{category_id}` — Listar por categoria (paginado)

---

### TAGS — `/api/v1/finance/tags` 🔒

> Tags combinam categoria + subcategoria para classificar transações.

#### `POST /api/v1/finance/tags`
**Body:**
```json
{
  "category_id": "uuid",
  "subcategory_id": "uuid",
  "active": true
}
```
**Response:**
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "category_id": "uuid",
  "subcategory_id": "uuid",
  "active": true,
  "created_at": "...",
  "updated_at": "..."
}
```

#### `GET /api/v1/finance/tags/{tag_id}` — Buscar por ID

#### `GET /api/v1/finance/tags` — Listar (paginado)
**Query params:** `?active=true` (default: `false`)

#### `PATCH /api/v1/finance/tags/{tag_id}/activate` — Ativar tag

#### `PATCH /api/v1/finance/tags/{tag_id}/deactivate` — Desativar tag

---

### PAYMENT METHODS — `/api/v1/finance/payment-methods` 🔒

#### `POST /api/v1/finance/payment-methods`
**Body:**
```json
{
  "label": "Cartão Nubank",
  "active": true
}
```
**Response:**
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "label": "Cartão Nubank",
  "active": true,
  "created_at": "...",
  "updated_at": "..."
}
```

#### `GET /api/v1/finance/payment-methods/{payment_method_id}` — Buscar por ID

#### `GET /api/v1/finance/payment-methods` — Listar (paginado)
**Query params:** `?active=true` (opcional, sem valor = retorna todos)

#### `PATCH /api/v1/finance/payment-methods/{payment_method_id}/activate`

#### `PATCH /api/v1/finance/payment-methods/{payment_method_id}/deactivate`

---

### TRANSACTIONS — `/api/v1/finance/transactions` 🔒

#### `POST /api/v1/finance/transactions`
**Body:**
```json
{
  "account_id": "uuid",
  "tag_id": "uuid",
  "payment_method_id": "uuid",
  "currency_id": "uuid",
  "value": "150.50",
  "description": "Almoço",
  "date_transaction": "2024-01-15T12:00:00Z"
}
```
> `description` e `date_transaction` são opcionais.

**Response:**
```json
{
  "id": "uuid",
  "account_id": "uuid",
  "tag_id": "uuid",
  "payment_method_id": "uuid",
  "currency_id": "uuid",
  "value": "150.50",
  "description": "Almoço",
  "date_transaction": "2024-01-15T12:00:00-03:00",
  "created_at": "...",
  "updated_at": "..."
}
```

---

### HOLDINGS — `/api/v1/finance/holdings` 🔒

> Holdings representam ativos financeiros vinculados a uma transação.

#### `POST /api/v1/finance/holdings`
**Body:**
```json
{
  "transaction_id": "uuid",
  "symbol": "BTC",
  "asset_type": "cripto",
  "quantity": "0.005000",
  "price": "280000.000000"
}
```
**Response:**
```json
{
  "id": "uuid",
  "transaction_id": "uuid",
  "symbol": "BTC",
  "asset_type": "cripto",
  "quantity": "0.005000",
  "price": "280000.000000",
  "created_at": "...",
  "updated_at": "..."
}
```

**Enum `asset_type`:** `cripto` | `stock` | `etf` | `bond`

---

## Fluxo típico de uso

```
1. POST /auth/signup  ou  POST /auth/login
   → Salvar access_token

2. GET /users/me
   → Carregar dados do usuário

3. GET /finance/financial-institutions
   → Listar bancos disponíveis

4. POST /finance/accounts
   → Criar conta vinculada a uma instituição

5. POST /finance/categories  →  POST /finance/subcategories
   →  POST /finance/tags
   → Criar hierarquia de classificação

6. POST /finance/payment-methods
   → Cadastrar formas de pagamento

7. GET /finance/currencies  (ou POST para criar)
   → Obter moeda (ex: BRL)

8. POST /finance/transactions
   → Registrar transação com account, tag, payment_method, currency

9. POST /finance/holdings  (opcional)
   → Vincular ativo à transação (para investimentos)
```

---

## Notas importantes

- **Datas**: Todos os campos de data são retornados no timezone local (conversão automática via `to_local()`)
- **Valores monetários**: Serializados como string com até 28 dígitos e 6 casas decimais (`Decimal`)
- **IDs**: Todos são UUIDs v7 (ordenáveis por tempo)
- **Unicidade**: Categoria (user+label+type), Tag (user+category+subcategory), Conta (user+institution+type+subtype), Currency (label+symbol), Instituição (name+type)
- **Token expirado**: API retorna `401` com `{"detail": "Sessão expirada"}` — redirecionar para login
