import sqlite3
from models import Usuario, SessaoAtiva

DB_PATH = 'auth_users.db'

class DBService:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self._ensure_tables()

    def get_conn(self):
        return sqlite3.connect(self.db_path)

    def _ensure_tables(self):
        conn = self.get_conn()
        c = conn.cursor()
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

    # Usuários
    def criar_usuario(self, nome, senha, admin=False):
        conn = self.get_conn()
        c = conn.cursor()
        c.execute('INSERT INTO usuarios (nome, senha, admin) VALUES (?, ?, ?)', (nome, senha, int(admin)))
        conn.commit()
        usuario_id = c.lastrowid
        conn.close()
        return usuario_id

    def buscar_usuario_por_nome(self, nome):
        conn = self.get_conn()
        c = conn.cursor()
        c.execute('SELECT id, nome, senha, admin, ativo FROM usuarios WHERE nome = ?', (nome,))
        row = c.fetchone()
        conn.close()
        return Usuario.from_row(row)

    def buscar_usuario_por_id(self, usuario_id):
        conn = self.get_conn()
        c = conn.cursor()
        c.execute('SELECT id, nome, senha, admin, ativo FROM usuarios WHERE id = ?', (usuario_id,))
        row = c.fetchone()
        conn.close()
        return Usuario.from_row(row)

    def listar_usuarios_ativos(self):
        conn = self.get_conn()
        c = conn.cursor()
        c.execute('SELECT id, nome, senha, admin, ativo FROM usuarios WHERE ativo = 1')
        rows = c.fetchall()
        conn.close()
        return [Usuario.from_row(row) for row in rows]

    def listar_todos_usuarios(self):
        conn = self.get_conn()
        c = conn.cursor()
        c.execute('SELECT id, nome, senha, admin, ativo FROM usuarios')
        rows = c.fetchall()
        conn.close()
        return [Usuario.from_row(row) for row in rows]

    def editar_usuario(self, usuario_id, nome=None, senha=None, admin=None, ativo=None):
        conn = self.get_conn()
        c = conn.cursor()
        updates = []
        values = []
        if nome is not None:
            updates.append('nome = ?')
            values.append(nome)
        if senha is not None:
            updates.append('senha = ?')
            values.append(senha)
        if admin is not None:
            updates.append('admin = ?')
            values.append(int(admin))
        if ativo is not None:
            updates.append('ativo = ?')
            values.append(int(ativo))
        if not updates:
            conn.close()
            return False
        values.append(usuario_id)
        query = f'UPDATE usuarios SET {", ".join(updates)} WHERE id = ?'
        c.execute(query, values)
        conn.commit()
        sucesso = c.rowcount > 0
        conn.close()
        return sucesso

    def bloquear_usuario(self, usuario_id):
        return self.editar_usuario(usuario_id, ativo=0)

    def reativar_usuario(self, usuario_id):
        return self.editar_usuario(usuario_id, ativo=1)

    # Sessões
    def criar_sessao(self, usuario_id, token, criado_em, expira_em):
        conn = self.get_conn()
        c = conn.cursor()
        c.execute('INSERT INTO sessoes_ativas (usuario_id, token, criado_em, expira_em) VALUES (?, ?, ?, ?)',
                  (usuario_id, token, criado_em, expira_em))
        conn.commit()
        sessao_id = c.lastrowid
        conn.close()
        return sessao_id

    def buscar_sessao_por_token(self, token):
        conn = self.get_conn()
        c = conn.cursor()
        c.execute('SELECT id, usuario_id, token, criado_em, expira_em FROM sessoes_ativas WHERE token = ?', (token,))
        row = c.fetchone()
        conn.close()
        return SessaoAtiva.from_row(row)

    def deletar_sessao(self, token):
        conn = self.get_conn()
        c = conn.cursor()
        c.execute('DELETE FROM sessoes_ativas WHERE token = ?', (token,))
        conn.commit()
        conn.close()
