from models.schema import get_connection

def inserir_usuario(nome, senha):
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO usuarios (nome, senha) VALUES (?, ?)', (nome, senha))
    conn.commit()
    conn.close()

def buscar_usuario_por_nome(nome):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT id, nome, senha FROM usuarios WHERE nome = ?', (nome,))
    usuario = c.fetchone()
    conn.close()
    return usuario 