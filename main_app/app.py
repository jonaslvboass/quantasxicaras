from flask import Flask, request, session, redirect, url_for
import models.schema as schema
import controllers.cozinheiros_controller as cozinheiros_controller
import controllers.receitas_controller as receitas_controller
import controllers.estoque_controller as estoque_controller
import controllers.ingredientes_controller as ingredientes_controller
import controllers.conversor_controller as conversor_controller
import views.home_view as home_view
import views.cozinheiros_view as cozinheiros_view
import views.receitas_view as receitas_view
import views.estoque_view as estoque_view
import views.ingredientes_view as ingredientes_view
import views.conversor_view as conversor_view
from functools import wraps
import pika
import json
import uuid
import controllers.recomendacao_controller as recomendacao_controller
import requests

app = Flask(__name__)
app.secret_key = 'quantasxicaras@Secret'

AUTH_API_URL = 'http://localhost:5001'

def requer_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = session.get('jwt_token')
        if not token:
            return redirect(url_for('login'))
        # Verifica o token na auth_api
        resp = requests.post(f'{AUTH_API_URL}/verify_token', json={'token': token})
        if resp.status_code != 200 or not resp.json().get('valid'):
            session.clear()
            return redirect(url_for('login'))
        # Atualiza dados do usuário na sessão
        payload = resp.json()
        session['usuario_id'] = payload.get('usuario_id')
        session['usuario_nome'] = payload.get('nome')
        session['admin'] = payload.get('admin', False)
        return f(*args, **kwargs)
    return decorated_function

@app.route('/home')
@requer_login
def home():
    if 'usuario_nome' in session:
        return home_view.renderizar_home(session['usuario_nome'])
    
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        admin = request.form.get('admin') == '1'
        admin_token = session.get('jwt_token') if admin else None
        resultado = cozinheiros_controller.cadastrar_usuario(nome, senha, admin, admin_token)
        return resultado or "Cadastro realizado! <a href='/login'>Ir para login</a>"
    else:
        return cozinheiros_view.renderizar_cadastro()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        resultado = cozinheiros_controller.autenticar_usuario(nome, senha)
        if resultado and isinstance(resultado, dict):
            session['usuario_id'] = resultado.get('usuario_id')
            session['usuario_nome'] = resultado.get('nome')
            session['jwt_token'] = resultado.get('token', '')
            session['admin'] = resultado.get('admin', False)
            return redirect(url_for('home'))
        else:
            return "Nome ou senha incorretos. <a href='/login'>Tentar novamente</a>"
    else:
        return cozinheiros_view.renderizar_login()

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# Rotas de receitas
@app.route('/adicionar_receita', methods=['GET', 'POST'])
@requer_login
def adicionar_receita():
    if request.method == 'POST':
        nome = request.form['nome']
        modo_preparo = request.form['modo_preparo']
        ingredientes = request.form.getlist('ingrediente_id[]')
        quantidades = request.form.getlist('quantidade[]')
        autor_id = session.get('usuario_id')
        resultado = receitas_controller.adicionar_receita(nome, modo_preparo, ingredientes, quantidades, autor_id)
        if resultado:
            return f"{resultado} <br><a href='/buscar_receitas'>Voltar</a>"
        return "Receita adicionada! <a href='/buscar_receitas'>Voltar</a>"
    else:
        ingredientes = ingredientes_controller.obter_ingredientes()
        return receitas_view.renderizar_formulario_adicionar_receita(ingredientes)

@app.route('/buscar_receitas')
@requer_login
def buscar_receitas():
    receitas = receitas_controller.obter_receitas()
    return receitas_view.renderizar_lista_receitas(receitas)

@app.route('/recomendar')
@requer_login
def recomendar():
    usuario_id = session.get('usuario_id')
    receitas = recomendacao_controller.obter_recomendacoes(usuario_id)
    return receitas_view.renderizar_recomendacoes(receitas)

# Rotas de estoque
@app.route('/adicionar_estoque', methods=['GET', 'POST'])
@requer_login
def adicionar_estoque():
    if request.method == 'POST':
        usuario_id = session.get('usuario_id')
        ingrediente_id = request.form['ingrediente_id']
        quantidade = float(request.form['quantidade'])
        resultado = estoque_controller.adicionar_estoque(usuario_id, ingrediente_id, quantidade)
        if resultado:
            return f"{resultado} <br><a href='/gerenciar_estoque'>Voltar</a>"
        return "Item adicionado ao estoque! <a href='/gerenciar_estoque'>Voltar</a>"
    else:
        ingredientes = ingredientes_controller.obter_ingredientes()
        return estoque_view.renderizar_formulario_adicionar_estoque(ingredientes)

@app.route('/gerenciar_estoque')
@requer_login
def gerenciar_estoque():
    usuario_id = session.get('usuario_id')
    itens = estoque_controller.obter_estoque(usuario_id)
    return estoque_view.renderizar_lista_estoque(itens)

@app.route('/editar_estoque/<int:item_id>', methods=['GET', 'POST'])
@requer_login
def editar_estoque(item_id):
    usuario_id = session.get('usuario_id')
    if request.method == 'POST':
        quantidade = float(request.form['quantidade'])
        resultado = estoque_controller.editar_estoque(item_id, usuario_id, quantidade)
        return resultado or "Item atualizado!"
    else:
        item = estoque_controller.obter_item_estoque(item_id, usuario_id)
        return estoque_view.renderizar_formulario_editar_estoque(item)

@app.route('/excluir_estoque/<int:item_id>')
@requer_login
def excluir_estoque(item_id):
    usuario_id = session.get('usuario_id')
    resultado = estoque_controller.excluir_estoque(item_id, usuario_id)
    return resultado or "Item excluído!"

# Ingredientes
@app.route('/ingredientes')
@requer_login
def listar_ingredientes():
    ingredientes = ingredientes_controller.obter_ingredientes()
    return ingredientes_view.renderizar_lista_ingredientes(ingredientes)

@app.route('/adicionar_ingrediente', methods=['GET', 'POST'])
@requer_login
def adicionar_ingrediente():
    if request.method == 'POST':
        nome = request.form['nome']
        ml_por_grama = float(request.form['ml_por_grama'])
        resultado = ingredientes_controller.adicionar_ingrediente(nome, ml_por_grama)
        if resultado:
            return f"{resultado} <br><a href='/ingredientes'>Voltar</a>"
        return "Ingrediente adicionado! <a href='/ingredientes'>Voltar</a>"
    else:
        return ingredientes_view.renderizar_formulario_adicionar_ingrediente()

# Exemplo de rota para conversor de medidas
@app.route('/', methods=['GET'])
def converter_medida():
    ingredientes = ingredientes_controller.obter_ingredientes()
    if request.args:
        ingrediente_id = request.args.get('ingrediente_id')
        quantidade = float(request.args.get('quantidade', 1))
        unidade_entrada = request.args.get('unidade_entrada', 'gramas')
        unidade_saida = request.args.get('unidade_saida', 'xicaras')
        resultado = conversor_controller.converter_medida(
            ingrediente_id, quantidade, unidade_entrada, unidade_saida
        )
        return conversor_view.renderizar_conversor(ingredientes, resultado)
    return conversor_view.renderizar_conversor(ingredientes)

if __name__ == '__main__':
    app.run(debug=True) 