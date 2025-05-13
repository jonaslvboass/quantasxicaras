# Quantas Xícaras? (MVC)

Este é o sistema Quantas Xícaras? organizado no padrão MVC com Flask.

## Estrutura

- `app.py`: aplicação principal Flask
- `models/`: modelos de dados separados por contexto
- `controllers/`: controladores de cada contexto
- `views/`: views HTML de cada contexto
- `models/schema.py`: conexão e (re)criação do banco de dados
- `orchestrator.py`: script para resetar o banco
- `requirements.txt`: dependências do projeto

## Como rodar a aplicação

0. Navege para a raiz da aplicação

   ```bash
   cd main_app
   ```

1. **Instale as dependências:**

   ```bash
   pip install -r requirements.txt
   ```

2. **(Opcional) Resete o banco de dados:**
   Sempre que quiser começar do zero, execute:

   ```bash
   python orchestrator.py
   ```

   Isso irá apagar o banco antigo, criar as tabelas e popular os ingredientes padrão.

3. **Inicie a aplicação:**

   ```bash
   python app.py
   ```

4. **Acesse no navegador:**
   - [http://localhost:5000](http://localhost:5000)

## Observações

- O banco de dados é um arquivo SQLite chamado `quantas_xicaras.db` na raiz do projeto.
- O sistema de autenticação pode depender de um serviço externo (verifique a configuração de `AUTH_API_URL` em `app.py`).
- O reset do banco APAGA todos os dados anteriores.

---

Desenvolvido para fins didáticos e de organização de código.
