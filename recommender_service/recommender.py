import sqlite3

DB_PATH = '../main_app/quantas_xicaras.db'

def recommend_for_user(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        SELECT r.id, r.nome, r.modo_preparo, GROUP_CONCAT(i.nome || ' (' || ri.quantidade || 'g)') as ingredientes_desc
        FROM receitas r
        JOIN receitas_ingredientes ri ON r.id = ri.receita_id
        JOIN ingredientes i ON ri.ingrediente_id = i.id
        WHERE NOT EXISTS (
            SELECT 1
            FROM receitas_ingredientes ri2
            LEFT JOIN estoque e ON e.ingrediente_id = ri2.ingrediente_id AND e.usuario_id = ?
            WHERE ri2.receita_id = r.id
              AND (e.quantidade IS NULL OR e.quantidade < ri2.quantidade)
        )
        GROUP BY r.id
    ''', (user_id,))
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