import sqlite3

DB_PATH = '../main_app/quantas_xicaras.db'

def recommend_for_user(user_id):
    conn = sqlite3.connect(DB_PATH)
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
                 GROUP BY rd.id''', (user_id,))
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