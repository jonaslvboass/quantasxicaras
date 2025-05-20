# Auth API

Esta é uma API de autenticação simples para cadastro, login e verificação de tokens JWT.

## Endpoints

### Autenticação

- `POST /register` — Cadastro de usuário
  - Body: `{ "nome": "usuario", "senha": "senha", "admin": false }`
    (Se `admin=true`, exige token de admin no header)
  - Header `{ "Authorization": "Bearer <jwt>"}`
- `POST /login` — Login de usuário
  - Body: `{ "nome": "usuario", "senha": "senha" }`
  - Retorna: `{ "token": "<jwt>" }`
- `POST /verify_token` — Verifica validade do token JWT
  - Body: `{ "token": "<jwt>" }`

### Gestão de Usuários (requer admin)

- `GET /usuarios` — Lista todos os usuários

  - Retorna: `[ { "nome": "usuario", "senha": "senha", "admin": false }, ... ] `
  - Header `{ "Authorization": "Bearer <jwt>"}`

- `PUT /usuarios/<id>` — Atualiza nome, senha, status ativo e tipo de acesso (admin)

  - Body: `{ "nome": "usuario", "senha": "senha", "admin": false, "ativo": "true" }`
  - Header `{ "Authorization": "Bearer <jwt>"}`

- `POST /usuarios/<id>/bloquear` — Bloqueia (soft delete) o usuário

  - Header `{ "Authorization": "Bearer <jwt>"}`

- `POST /usuarios/<id>/desbloquear` — Reativa usuário bloqueado
  - Header `{ "Authorization": "Bearer <jwt>"}`

## Como rodar

1. Acesse a pasta da aplicação:
   ```bash
   cd auth_api
   ```
2. Instale as dependências:
   ```bash
   pip install Flask PyJWT
   ```
3. Execute a API:
   ```bash
   python app.py
   ```

A API estará disponível em `http://localhost:5001`.

## Banco de dados

- Utiliza SQLite (`auth_api/auth_users.db`).

## Resetar o banco de dados

Para resetar o banco de dados (apagar e recriar as tabelas):

```bash
cd auth_api
python orchestrator.py
```
