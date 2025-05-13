import sqlite3
import os

DB_PATH = 'quantas_xicaras.db'

def get_connection():
    return sqlite3.connect(DB_PATH)

def resetar_banco():
    # Remove o banco antigo, se existir
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = get_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE usuarios (
        id INTEGER PRIMARY KEY, 
        nome TEXT, 
        senha TEXT
    )''')
    c.execute('''CREATE TABLE ingredientes (
        id INTEGER PRIMARY KEY,
        nome TEXT UNIQUE,
        ml_por_grama FLOAT
    )''')
    c.execute('''CREATE TABLE receitas (
        id INTEGER PRIMARY KEY, 
        nome TEXT, 
        modo_preparo TEXT
    )''')
    c.execute('''CREATE TABLE receitas_ingredientes (
        receita_id INTEGER,
        ingrediente_id INTEGER,
        quantidade FLOAT,
        FOREIGN KEY (receita_id) REFERENCES receitas(id),
        FOREIGN KEY (ingrediente_id) REFERENCES ingredientes(id),
        PRIMARY KEY (receita_id, ingrediente_id)
    )''')
    c.execute('''CREATE TABLE estoque (
        id INTEGER PRIMARY KEY, 
        usuario_id INTEGER,
        ingrediente_id INTEGER,
        quantidade FLOAT,
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
        FOREIGN KEY (ingrediente_id) REFERENCES ingredientes(id)
    )''')
    conn.commit()
    conn.close()

def adicionar_ingredientes_padrao():
    ingredientes_padrao = [
        ('Farinha de Trigo', 0.6),
        ('Açúcar', 0.85),
        ('Leite', 1.03),
        ('Óleo', 0.92),
        ('Manteiga', 0.91),
        ('Chocolate em Pó', 0.5),
        ('Fermento em Pó', 0.45)
    ]
    conn = get_connection()
    c = conn.cursor()
    c.executemany('''INSERT OR IGNORE INTO ingredientes (nome, ml_por_grama) VALUES (?, ?)''', ingredientes_padrao)
    conn.commit()
    conn.close() 