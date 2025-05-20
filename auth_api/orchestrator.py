from services import DBService
import os

DB_PATH = 'auth_users.db'

def reset_db():
    # Garante que o diretório existe
    os.makedirs(os.path.dirname(DB_PATH) or '.', exist_ok=True)
    # Cria o arquivo do banco se não existir
    if not os.path.exists(DB_PATH):
        open(DB_PATH, 'a').close()
    db_service = DBService(DB_PATH)
    conn = db_service.get_conn()
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS sessoes_ativas')
    c.execute('DROP TABLE IF EXISTS usuarios')
    c.execute('''CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT UNIQUE NOT NULL,
        senha TEXT NOT NULL,
        admin INTEGER NOT NULL DEFAULT 0,
        ativo INTEGER NOT NULL DEFAULT 1
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS sessoes_ativas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER NOT NULL,
        token TEXT NOT NULL,
        criado_em TEXT NOT NULL,
        expira_em TEXT NOT NULL,
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
    )''')
    conn.commit()
    conn.close()
    print('Banco de dados resetado com sucesso.')

if __name__ == '__main__':
    reset_db() 