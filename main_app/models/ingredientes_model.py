from models.schema import get_connection

def buscar_ingredientes():
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT id, nome, ml_por_grama FROM ingredientes ORDER BY nome')
    ingredientes = c.fetchall()
    conn.close()
    return ingredientes

def buscar_ingrediente_por_id(ingrediente_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT id, nome, ml_por_grama FROM ingredientes WHERE id = ?', (ingrediente_id,))
    ingrediente = c.fetchone()
    conn.close()
    return ingrediente

def inserir_ingrediente(nome, ml_por_grama):
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO ingredientes (nome, ml_por_grama) VALUES (?, ?)', (nome, ml_por_grama))
    conn.commit()
    conn.close() 