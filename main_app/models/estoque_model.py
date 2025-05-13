from models.schema import get_connection

def inserir_estoque(usuario_id, ingrediente_id, quantidade):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT id, quantidade FROM estoque WHERE usuario_id = ? AND ingrediente_id = ?', (usuario_id, ingrediente_id))
    item_existente = c.fetchone()
    if item_existente:
        nova_quantidade = item_existente[1] + quantidade
        c.execute('UPDATE estoque SET quantidade = ? WHERE id = ?', (nova_quantidade, item_existente[0]))
    else:
        c.execute('INSERT INTO estoque (usuario_id, ingrediente_id, quantidade) VALUES (?, ?, ?)', (usuario_id, ingrediente_id, quantidade))
    conn.commit()
    conn.close()

def buscar_estoque(usuario_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''SELECT e.id, i.nome, e.quantidade
                 FROM estoque e
                 JOIN ingredientes i ON e.ingrediente_id = i.id
                 WHERE e.usuario_id = ?
                 ORDER BY i.nome''', (usuario_id,))
    itens = []
    for row in c.fetchall():
        itens.append({'id': row[0], 'nome': row[1], 'quantidade': row[2]})
    conn.close()
    return itens

def buscar_item_estoque(item_id, usuario_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''SELECT e.id, e.quantidade, i.nome
                 FROM estoque e
                 JOIN ingredientes i ON e.ingrediente_id = i.id
                 WHERE e.id = ? AND e.usuario_id = ?''', (item_id, usuario_id))
    row = c.fetchone()
    conn.close()
    if row:
        return {'id': row[0], 'quantidade': row[1], 'nome': row[2]}
    return None

def atualizar_estoque(item_id, usuario_id, quantidade):
    conn = get_connection()
    c = conn.cursor()
    c.execute('UPDATE estoque SET quantidade = ? WHERE id = ? AND usuario_id = ?', (quantidade, item_id, usuario_id))
    conn.commit()
    conn.close()

def deletar_estoque(item_id, usuario_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('DELETE FROM estoque WHERE id = ? AND usuario_id = ?', (item_id, usuario_id))
    conn.commit()
    conn.close() 