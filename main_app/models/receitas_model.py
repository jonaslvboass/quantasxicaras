from models.schema import get_connection

def inserir_receita(nome, modo_preparo, ingredientes, quantidades):
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO receitas (nome, modo_preparo) VALUES (?, ?)', (nome, modo_preparo))
    receita_id = c.lastrowid
    for ing_id, qtd in zip(ingredientes, quantidades):
        c.execute('INSERT INTO receitas_ingredientes (receita_id, ingrediente_id, quantidade) VALUES (?, ?, ?)', (receita_id, ing_id, float(qtd)))
    conn.commit()
    conn.close()
    return receita_id

def buscar_receitas():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''SELECT r.id, r.nome, r.modo_preparo, GROUP_CONCAT(i.nome || ' (' || ri.quantidade || 'g)') as ingredientes
                 FROM receitas r
                 LEFT JOIN receitas_ingredientes ri ON r.id = ri.receita_id
                 LEFT JOIN ingredientes i ON ri.ingrediente_id = i.id
                 GROUP BY r.id''')
    receitas = []
    for row in c.fetchall():
        receitas.append({
            'id': row[0],
            'nome': row[1],
            'modo_preparo': row[2],
            'ingredientes': row[3].split(',') if row[3] else []
        })
    conn.close()
    return receitas

def buscar_receita_por_id(receita_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''SELECT r.id, r.nome, r.modo_preparo, GROUP_CONCAT(i.nome || ' (' || ri.quantidade || 'g)') as ingredientes
                 FROM receitas r
                 LEFT JOIN receitas_ingredientes ri ON r.id = ri.receita_id
                 LEFT JOIN ingredientes i ON ri.ingrediente_id = i.id
                 WHERE r.id = ?
                 GROUP BY r.id''', (receita_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return {
            'id': row[0],
            'nome': row[1],
            'modo_preparo': row[2],
            'ingredientes': row[3].split(',') if row[3] else []
        }
    return None

def recomendar_receitas(usuario_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''SELECT rd.id, rd.nome, rd.modo_preparo, GROUP_CONCAT(i.nome || ' (' || rdi.quantidade || 'g)') as ingredientes_desc
                 FROM receitas rd
                 JOIN receitas_ingredientes rdi ON rd.id = rdi.receita_id
                 JOIN ingredientes i ON rdi.ingrediente_id = i.id
                 WHERE rd.id NOT IN (
                     SELECT r.id
                     FROM receitas r
                     JOIN receitas_ingredientes ri ON r.id = ri.receita_id
                     LEFT JOIN estoque e ON e.ingrediente_id = ri.ingrediente_id
                     WHERE (e.usuario_id = ? AND e.quantidade < ri.quantidade) OR e.usuario_id IS NULL
                 )
                 GROUP BY rd.id''', (usuario_id,))
    receitas = []
    for row in c.fetchall():
        receitas.append({
            'id': row[0],
            'nome': row[1],
            'modo_preparo': row[2],
            'ingredientes': row[3].split(',') if row[3] else []
        })
    conn.close()
    return receitas 