from flask import Flask, request, session, redirect, url_for
import sqlite3
import random

app = Flask(__name__)
app.secret_key = 'quantasxicaras@Secret'

db = 'quantas_xicaras.db'

# Criando banco de dados
conn = sqlite3.connect(db)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY, 
    nome TEXT, 
    senha TEXT
)''')

c.execute('''CREATE TABLE IF NOT EXISTS ingredientes (
    id INTEGER PRIMARY KEY,
    nome TEXT UNIQUE,
    ml_por_grama FLOAT
)''')

c.execute('''CREATE TABLE IF NOT EXISTS receitas (
    id INTEGER PRIMARY KEY, 
    nome TEXT, 
    modo_preparo TEXT
)''')

c.execute('''CREATE TABLE IF NOT EXISTS receitas_ingredientes (
    receita_id INTEGER,
    ingrediente_id INTEGER,
    quantidade FLOAT,
    FOREIGN KEY (receita_id) REFERENCES receitas(id),
    FOREIGN KEY (ingrediente_id) REFERENCES ingredientes(id),
    PRIMARY KEY (receita_id, ingrediente_id)
)''')

c.execute('''CREATE TABLE IF NOT EXISTS estoque (
    id INTEGER PRIMARY KEY, 
    usuario_id INTEGER,
    ingrediente_id INTEGER,
    quantidade FLOAT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (ingrediente_id) REFERENCES ingredientes(id)
)''')

# Adicionando alguns ingredientes padrão
ingredientes_padrao = [
    ('Farinha de Trigo', 0.6),
    ('Açúcar', 0.85),
    ('Leite', 1.03),
    ('Óleo', 0.92),
    ('Manteiga', 0.91),
    ('Chocolate em Pó', 0.5),
    ('Fermento em Pó', 0.45)
]

c.executemany('''INSERT OR IGNORE INTO ingredientes (nome, ml_por_grama) VALUES (?, ?)''', 
              ingredientes_padrao)

conn.commit()
conn.close()

@app.route('/home')
def home():
    if 'usuario_nome' in session:
        return f"""
            <h1>Bem-vindo ao Quantas Xícaras?</h1>
            <p>Olá, {session['usuario_nome']}!</p>
            <ul>
                <li><a href="/adicionar_receita">Adicionar Receita</a></li>
                <li><a href="/buscar_receitas">Buscar Receitas</a></li>
                <li><a href="/gerenciar_estoque">Gerenciar Estoque</a></li>
                <li><a href="/">Converter Medidas</a></li>
                <li><a href="/logout">Sair</a></li>
            </ul>
        """
    else:
        return f"""
            <h1>Bem-vindo ao Quantas Xícaras?</h1>
            <p>Por favor, faça <a href="/login">login</a> ou <a href="/cadastro">cadastre-se</a>.</p>
            <a href="/">Voltar ao conversor de medidas</a>
        """

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute("INSERT INTO usuarios (nome, senha) VALUES (?, ?)", (nome, senha))
        conn.commit()
        conn.close()
        return "Cadastro realizado!"
    else:
        return f"""
            <h2>Cadastro de Cozinheiro(a)</h2>
            <form method="POST">
                <label for="nome">Nome:</label>
                <input type="text" id="nome" name="nome" required><br><br>
                
                <label for="senha">Senha:</label>
                <input type="password" id="senha" name="senha" required><br><br>
                
                <button type="submit">Cadastrar</button>
            </form>
            <a href="/home">Voltar</a>
        """

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute("SELECT id, nome FROM usuarios WHERE nome = ? AND senha = ?", (nome, senha))
        usuario = c.fetchone()
        conn.close()
        
        if usuario:
            session['usuario_id'] = usuario[0]
            session['usuario_nome'] = usuario[1]
            return redirect(url_for('home'))
        else:
            return "Nome ou senha incorretos."
    else:
        return f"""
            <h1>Bem-vindo ao Quantas Xícaras?</h1>
            <p>Por favor, faça login ou <a href="/cadastro">cadastre-se</a>.</p>

            <h2>Login</h2>
            <form method="POST">
                <label for="nome">Nome:</label>
                <input type="text" id="nome" name="nome" required><br><br>
                
                <label for="senha">Senha:</label>
                <input type="password" id="senha" name="senha" required><br><br>
                
                <button type="submit">Logar</button>
            </form>
            <a href="/home">Voltar</a>
        """

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# Função auxiliar para verificar se usuário está logado
def requer_login(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/adicionar_receita', methods=['GET', 'POST'])
@requer_login
def adicionar_receita():
    if request.method == 'POST':
        nome = request.form['nome']
        modo_preparo = request.form['modo_preparo']
        
        conn = sqlite3.connect(db)
        c = conn.cursor()
        
        # Inserir a receita
        c.execute("INSERT INTO receitas (nome, modo_preparo) VALUES (?, ?)", 
                 (nome, modo_preparo))
        receita_id = c.lastrowid
        
        # Processar ingredientes
        ingredientes = request.form.getlist('ingrediente_id[]')
        quantidades = request.form.getlist('quantidade[]')
        
        for ing_id, qtd in zip(ingredientes, quantidades):
            c.execute("""
                INSERT INTO receitas_ingredientes (receita_id, ingrediente_id, quantidade)
                VALUES (?, ?, ?)
            """, (receita_id, ing_id, float(qtd)))
        
        conn.commit()
        conn.close()
        return "Receita adicionada!"
    else:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute("SELECT id, nome FROM ingredientes ORDER BY nome")
        ingredientes = c.fetchall()
        conn.close()
        
        return f"""
            <h2>Cadastro de Receita</h2>
            <form method="POST">
                <label for="nome">Nome:</label>
                <input type="text" id="nome" name="nome" required><br><br>
                
                <div id="ingredientes">
                    <h3>Ingredientes:</h3>
                    <div class="ingrediente-item">
                        <select name="ingrediente_id[]" required>
                            <option value="">Selecione um ingrediente</option>
                            {''.join(f'<option value="{i[0]}">{i[1]}</option>' for i in ingredientes)}
                        </select>
                        <input type="number" name="quantidade[]" step="0.01" placeholder="Quantidade (g)" required>
                    </div>
                </div>
                <button type="button" onclick="addIngrediente()">+ Adicionar Ingrediente</button><br><br>

                <label for="modo_preparo">Modo de Preparo:</label><br>
                <textarea id="modo_preparo" name="modo_preparo" rows="4" cols="50" required></textarea><br><br>
                
                <button type="submit">Cadastrar</button>
            </form>
            
            <script>
                function addIngrediente() {{
                    const div = document.createElement('div');
                    div.className = 'ingrediente-item';
                    div.innerHTML = `
                        <select name="ingrediente_id[]" required>
                            <option value="">Selecione um ingrediente</option>
                            {''.join(f'<option value="{i[0]}">{i[1]}</option>' for i in ingredientes)}
                        </select>
                        <input type="number" name="quantidade[]" step="0.01" placeholder="Quantidade (g)" required>
                    `;
                    document.getElementById('ingredientes').appendChild(div);
                }}
            </script>
            <a href="/home">Voltar</a>
        """

@app.route('/buscar_receitas')
@requer_login
def buscar_receitas():
    conn = sqlite3.connect(db)
    c = conn.cursor()
    
    # Buscar todas as receitas com seus ingredientes
    c.execute("""
        SELECT 
            r.id,
            r.nome,
            r.modo_preparo,
            GROUP_CONCAT(i.nome || ' (' || ri.quantidade || 'g)') as ingredientes
        FROM receitas r
        LEFT JOIN receitas_ingredientes ri ON r.id = ri.receita_id
        LEFT JOIN ingredientes i ON ri.ingrediente_id = i.id
        GROUP BY r.id
    """)
    receitas = c.fetchall()
    conn.close()
    
    html = """
        <h2>Receitas Disponíveis</h2>
        <div style="margin: 20px;">
    """
    
    for r in receitas:
        html += f"""
            <div style="margin-bottom: 30px; border: 1px solid #ccc; padding: 15px; border-radius: 5px;">
                <h3>{r[1]}</h3>
                <div>
                    <strong>Ingredientes:</strong>
                    <ul>
                        {' '.join(f'<li>{ing}</li>' for ing in (r[3].split(',') if r[3] else []))}
                    </ul>
                </div>
                <div>
                    <strong>Modo de Preparo:</strong>
                    <p style="white-space: pre-line;">{r[2]}</p>
                </div>
            </div>
        """
    
    html += """
        </div>
        <a href="/home">Voltar</a>
    """
    return html

@app.route('/recomendar')
@requer_login
def recomendar():
    usuario_id = session['usuario_id']
    
    conn = sqlite3.connect(db)
    c = conn.cursor()

    c.execute("""
        SELECT 
            rd.id,
            rd.nome,
            rd.modo_preparo,
            GROUP_CONCAT(i.nome || ' (' || rdi.quantidade || 'g)') as ingredientes_desc
        FROM receitas rd
        JOIN receitas_ingredientes rdi ON rd.id = rdi.receita_id
        JOIN ingredientes i ON rdi.ingrediente_id = i.id
        WHERE rd.id NOT IN (              
            SELECT r.id
            FROM receitas r
            JOIN receitas_ingredientes ri ON r.id = ri.receita_id
            LEFT JOIN estoque e ON e.ingrediente_id = ri.ingrediente_id
            WHERE (e.usuario_id = ? AND e.quantidade < ri.quantidade) 
            OR e.usuario_id IS NULL
        )
    """, (usuario_id, ))
    receitas = c.fetchall()
    conn.close()
    
    html = """
        <h2>Receitas Recomendadas</h2>
        <style>
            .receita {
                margin: 20px 0;
                padding: 15px;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
            .receita.possivel {
                border-left: 5px solid #4CAF50;
            }
            .receita.impossivel {
                border-left: 5px solid #f44336;
            }
            .ingrediente {
                margin: 5px 0;
            }
            .disponivel {
                color: #4CAF50;
            }
            .indisponivel {
                color: #f44336;
            }
        </style>
    """
    if not receitas or not receitas[0][1]:
        html += "<p>Você não pode fazer nenhuma receita cadastrada.</p>"
    else:   
        for r in receitas:
            html += f"""
                <div class="receita possivel">
                    <h3>{r[1]} </h3>
                    <p><strong>Ingredientes necessários:</strong></p>
                    <ul>
                    {' '.join(f'<li>{ing}</li>' for ing in (r[3].split(',') if r[3] else []))}
                    </ul>
                    <p><strong>Modo de Preparo:</strong></p>
                    <p style="white-space: pre-line;">{r[2]}</p>
                </div>
            """
    
    
    
    html += """
        <br>
        <a href="/home">Voltar ao Menu</a>
    """
    
    return html

@app.route('/', methods=['GET'])
def converter_medida():
    if request.method == 'GET':
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute("SELECT id, nome FROM ingredientes ORDER BY nome")
        ingredientes = c.fetchall()
        conn.close()
        
        # Se não houver parâmetros, mostrar o formulário
        if not request.args:
            return f"""
            <div style="width: 100vw; height: 90vh; display: flex; flex-direction: column; justify-content: center; align-items: center;">
                <h1>Quantas Xícaras?</h1>
                <form method="GET">
                    <label for="ingrediente_id">Ingrediente:</label>
                    <select id="ingrediente_id" name="ingrediente_id" required>
                        <option value="">Selecione um ingrediente</option>
                        {''.join(f'<option value="{i[0]}">{i[1]}</option>' for i in ingredientes)}
                    </select><br><br>
                    
                    <label for="quantidade">Quantidade:</label>
                    <input type="number" id="quantidade" name="quantidade" step="0.01" required><br><br>
                    
                    <label for="unidade">Unidade:</label>
                    <select id="unidade" name="unidade" required>
                        <option value="gramas">Gramas</option>
                        <option value="xicaras">Xícaras</option>
                        <option value="colheres_sopa">Colheres de Sopa</option>
                        <option value="colheres_cha">Colheres de Chá</option>
                    </select><br><br>
                    
                    <button type="submit">Converter</button>
                </form>
                <a href="/home">Sistema de Receitas</a>
            </div>
            """
        
        # Se houver parâmetros, fazer a conversão
        ingrediente_id = request.args.get('ingrediente_id')
        quantidade = float(request.args.get('quantidade', 1))
        unidade = request.args.get('unidade', 'gramas')
        
        # Buscar o fator de conversão do ingrediente
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute("SELECT nome, ml_por_grama FROM ingredientes WHERE id = ?", (ingrediente_id,))
        ingrediente = c.fetchone()
        conn.close()
        
        if not ingrediente:
            return "Ingrediente não encontrado"
        
        nome_ingrediente, ml_por_grama = ingrediente
        
        # Fatores de conversão para volume
        conversoes = {
            'gramas': 1,
            'xicaras': 240,  # 1 xícara = 240ml
            'colheres_sopa': 15,  # 1 colher de sopa = 15ml
            'colheres_cha': 5  # 1 colher de chá = 5ml
        }
        
        if unidade not in conversoes:
            return "Unidade desconhecida"
        
        # Cálculos de conversão
        if unidade == 'gramas':
            # Convertendo de gramas para todas as unidades
            ml_total = quantidade * ml_por_grama
            resultado = {
                'xicaras': ml_total / conversoes['xicaras'],
                'colheres_sopa': ml_total / conversoes['colheres_sopa'],
                'colheres_cha': ml_total / conversoes['colheres_cha']
            }
        else:
            # Convertendo de volume para gramas e depois para outros volumes
            ml_total = quantidade * conversoes[unidade]
            gramas = ml_total / ml_por_grama
            resultado = {
                'gramas': gramas,
                'xicaras': ml_total / conversoes['xicaras'],
                'colheres_sopa': ml_total / conversoes['colheres_sopa'],
                'colheres_cha': ml_total / conversoes['colheres_cha']
            }
            
        # Formatando o resultado
        html = f"""
            <h2>Resultado da Conversão</h2>
            <h3>{quantidade} {unidade} de {nome_ingrediente} equivale a:</h3>
            <ul>
        """
        
        for un, valor in resultado.items():
            if un != unidade:  # Não mostrar a unidade de origem
                html += f"<li>{valor:.2f} {un}</li>"
        
        html += """
            </ul>
            <br>
            <a href="/converter_medida">Nova Conversão</a> | 
            <a href="/home">Voltar</a>
        """
        
        return html

@app.route('/adicionar_estoque', methods=['GET', 'POST'])
@requer_login
def adicionar_estoque():
    if request.method == 'POST':
        usuario_id = session['usuario_id']  # Usando ID do usuário logado
        ingrediente_id = request.form['ingrediente_id']
        quantidade = float(request.form['quantidade'])
        
        conn = sqlite3.connect(db)
        c = conn.cursor()
        
        # Verificar se o ingrediente já existe no estoque do usuário
        c.execute("""
            SELECT id, quantidade FROM estoque 
            WHERE usuario_id = ? AND ingrediente_id = ?
        """, (usuario_id, ingrediente_id))
        item_existente = c.fetchone()
        
        if item_existente:
            # Atualizar quantidade existente
            nova_quantidade = item_existente[1] + quantidade
            c.execute("""
                UPDATE estoque 
                SET quantidade = ? 
                WHERE id = ?
            """, (nova_quantidade, item_existente[0]))
            mensagem = "Quantidade atualizada no estoque!"
        else:
            # Inserir novo item
            c.execute("""
                INSERT INTO estoque (usuario_id, ingrediente_id, quantidade) 
                VALUES (?, ?, ?)
            """, (usuario_id, ingrediente_id, quantidade))
            mensagem = "Item adicionado ao estoque!"
        
        conn.commit()
        conn.close()
        return f"{mensagem} <a href='/gerenciar_estoque'>Voltar ao estoque</a>"
    else:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute("SELECT id, nome FROM ingredientes ORDER BY nome")
        ingredientes = c.fetchall()
        conn.close()
        
        return f"""
            <h2>Adicionar Item ao Estoque</h2>
            <form method="POST">
                <label for="ingrediente_id">Ingrediente:</label>
                <select id="ingrediente_id" name="ingrediente_id" required>
                    <option value="">Selecione um ingrediente</option>
                    {''.join(f'<option value="{i[0]}">{i[1]}</option>' for i in ingredientes)}
                </select><br><br>
                
                <label for="quantidade">Quantidade (g):</label>
                <input type="number" id="quantidade" name="quantidade" step="0.01" required><br><br>
                
                <button type="submit">Adicionar</button>
            </form>
            <a href="/gerenciar_estoque">Voltar</a>
        """

@app.route('/gerenciar_estoque')
@requer_login
def gerenciar_estoque():
    usuario_id = session['usuario_id']  # Usando ID do usuário logado
    
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("""
        SELECT e.id, i.nome, e.quantidade, i.ml_por_grama
        FROM estoque e
        JOIN ingredientes i ON e.ingrediente_id = i.id
        WHERE e.usuario_id = ?
        ORDER BY i.nome
    """, (usuario_id,))
    itens = c.fetchall()
    conn.close()
    
    html = """
        <h2>Meu Estoque</h2>
        <a href="/adicionar_estoque" class="button">Adicionar Novo Item</a><br><br>
        <style>
            .button {
                display: inline-block;
                padding: 8px 16px;
                background-color: #4CAF50;
                color: white;
                text-decoration: none;
                border-radius: 4px;
                margin-bottom: 10px;
            }
            .button:hover {
                background-color: #45a049;
            }
            table {
                width: 100%;
                border-collapse: collapse;
            }
            th, td {
                padding: 8px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }
            th {
                background-color: #f2f2f2;
            }
            tr:hover {
                background-color: #f5f5f5;
            }
            .actions a {
                margin-right: 10px;
                color: #0066cc;
                text-decoration: none;
            }
            .actions a:hover {
                text-decoration: underline;
            }
        </style>
    """
    
    if itens:
        html += """
            <table>
                <tr>
                    <th>Ingrediente</th>
                    <th>Quantidade (g)</th>
                    <th>Volume (ml)</th>
                    <th>Ações</th>
                </tr>
        """
        
        for item in itens:
            volume_ml = item[2] * item[3]  # quantidade * ml_por_grama
            html += f"""
                <tr>
                    <td>{item[1]}</td>
                    <td>{item[2]:.2f}</td>
                    <td>{volume_ml:.2f}</td>
                    <td class="actions">
                        <a href="/editar_estoque/{item[0]}">Editar</a>
                        <a href="/excluir_estoque/{item[0]}" onclick="return confirm('Tem certeza que deseja excluir este item?')">Excluir</a>
                    </td>
                </tr>
            """
        
        html += "</table>"
    else:
        html += "<p>Nenhum item no estoque. Comece adicionando ingredientes!</p>"
    
    html += "<br><a href='/' class='button'>Voltar ao Menu</a>"
    return html

@app.route('/editar_estoque/<int:item_id>', methods=['GET', 'POST'])
@requer_login
def editar_estoque(item_id):
    usuario_id = session['usuario_id']
    
    if request.method == 'POST':
        quantidade = float(request.form['quantidade'])
        
        conn = sqlite3.connect(db)
        c = conn.cursor()
        # Verificar se o item pertence ao usuário
        c.execute("SELECT id FROM estoque WHERE id = ? AND usuario_id = ?", 
                 (item_id, usuario_id))
        if not c.fetchone():
            conn.close()
            return "Item não encontrado ou sem permissão para editar."
            
        c.execute("UPDATE estoque SET quantidade = ? WHERE id = ?", 
                 (quantidade, item_id))
        conn.commit()
        conn.close()
        return "Item atualizado! <a href='/gerenciar_estoque'>Voltar ao estoque</a>"
    else:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        
        # Buscar item com informações do ingrediente
        c.execute("""
            SELECT e.id, e.quantidade, i.nome, i.id as ingrediente_id
            FROM estoque e
            JOIN ingredientes i ON e.ingrediente_id = i.id
            WHERE e.id = ? AND e.usuario_id = ?
        """, (item_id, usuario_id))
        item = c.fetchone()
        
        if not item:
            conn.close()
            return "Item não encontrado ou sem permissão para editar."
        
        return f"""
            <h2>Editar Item do Estoque</h2>
            <form method="POST">
                <p><strong>Ingrediente:</strong> {item[2]}</p>
                
                <label for="quantidade">Quantidade (g):</label>
                <input type="number" id="quantidade" name="quantidade" 
                       step="0.01" value="{item[1]:.2f}" required><br><br>
                
                <button type="submit">Atualizar</button>
            </form>
            <a href="/gerenciar_estoque">Voltar</a>
        """

@app.route('/excluir_estoque/<int:item_id>')
@requer_login
def excluir_estoque(item_id):
    usuario_id = session['usuario_id']
    
    conn = sqlite3.connect(db)
    c = conn.cursor()
    
    # Verificar se o item pertence ao usuário
    c.execute("SELECT id FROM estoque WHERE id = ? AND usuario_id = ?", 
             (item_id, usuario_id))
    if not c.fetchone():
        conn.close()
        return "Item não encontrado ou sem permissão para excluir."
        
    c.execute("DELETE FROM estoque WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()
    return "Item excluído! <a href='/gerenciar_estoque'>Voltar ao estoque</a>"

if __name__ == '__main__':
    app.run(debug=True)
