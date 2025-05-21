from flask import Blueprint, request, jsonify, current_app
import jwt
import datetime
from functools import wraps
from services import DBService
from models import Usuario

bp = Blueprint('auth', __name__)
db_service = DBService()

def is_admin_token(token):
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload.get('admin', False) is True
    except Exception:
        return False

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Token necessário.'}), 403
        token = auth_header.split(' ', 1)[1]
        if not is_admin_token(token):
            return jsonify({'error': 'Apenas administradores têm acesso.'}), 403
        return f(*args, **kwargs)
    return decorated

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    nome = data.get('nome')
    senha = data.get('senha')
    admin = bool(data.get('admin', False))
    if not nome or not senha:
        return jsonify({'error': 'Nome e senha são obrigatórios.'}), 400
    if db_service.buscar_usuario_por_nome(nome):
        return jsonify({'error': 'Nome de usuário já existe.'}), 409
    if admin:
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Token de autenticação de administrador necessário.'}), 403
        token = auth_header.split(' ', 1)[1]
        if not is_admin_token(token):
            return jsonify({'error': 'Apenas administradores podem criar outros administradores.'}), 403
    usuario_id = db_service.criar_usuario(nome, senha, admin=admin)
    return jsonify({'message': 'Usuário cadastrado com sucesso!', 'usuario_id': usuario_id, 'admin': admin}), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    nome = data.get('nome')
    senha = data.get('senha')
    usuario = db_service.buscar_usuario_por_nome(nome)
    if not usuario or usuario.senha != senha:
        return jsonify({'error': 'Nome ou senha inválidos.'}), 401
    if not usuario.ativo:
        return jsonify({'error': 'Usuário bloqueado.'}), 403
    now = datetime.datetime.now(datetime.timezone.utc)
    exp = now + datetime.timedelta(hours=12)
    payload = {
        'usuario_id': usuario.id,
        'nome': usuario.nome,
        'admin': usuario.admin,
        'exp': exp,
    }
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    criado_em = now.isoformat()
    expira_em = exp.isoformat()
    db_service.criar_sessao(usuario.id, token, criado_em, expira_em)
    return jsonify({'token': token, 'admin': usuario.admin})

@bp.route('/verify_token', methods=['POST'])
def verify_token():
    data = request.get_json()
    token = data.get('token')
    if not token:
        return jsonify({'error': 'Token não fornecido.'}), 400
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        sessao = db_service.buscar_sessao_por_token(token)
        if not sessao:
            return jsonify({'valid': False, 'error': 'Sessão não encontrada.'}), 401
        return jsonify({'valid': True, 'usuario_id': payload['usuario_id'], 'nome': payload['nome'], 'admin': payload.get('admin', False)})
    except jwt.ExpiredSignatureError:
        return jsonify({'valid': False, 'error': 'Token expirado.'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'valid': False, 'error': 'Token inválido.'}), 401

@bp.route('/usuarios', methods=['GET'])
@admin_required
def listar_todos_usuarios():
    # Modificar para aceitar paginação
    limit = request.args.get('limit', default=10, type=int)
    offset = request.args.get('offset', default=0, type=int)

    usuarios_paginados = db_service.listar_usuarios_paginado(limit, offset)
    total_usuarios = db_service.contar_total_usuarios()

    # Formatar a lista de usuários
    lista_usuarios = [{
        'id': u.id,
        'nome': u.nome,
        'admin': u.admin,
        'ativo': u.ativo
    } for u in usuarios_paginados]

    # Retornar dados paginados e total
    return jsonify({
        'usuarios': lista_usuarios,
        'total': total_usuarios,
        'limit': limit,
        'offset': offset
    })

@bp.route('/usuarios/<int:usuario_id>', methods=['PUT'])
@admin_required
def editar_usuario(usuario_id):
    data = request.get_json()
    nome = data.get('nome')
    senha = data.get('senha')
    admin = data.get('admin')
    ativo = data.get('ativo')
    atualizado = db_service.editar_usuario(usuario_id, nome, senha, admin, ativo)
    if not atualizado:
        return jsonify({'error': 'Usuário não encontrado ou não atualizado.'}), 404
    return jsonify({'message': 'Usuário atualizado com sucesso.'})

@bp.route('/usuarios/<int:usuario_id>', methods=['GET'])
@admin_required
def get_usuario_por_id(usuario_id):
    usuario = db_service.buscar_usuario_por_id(usuario_id)
    if not usuario:
        return jsonify({'error': 'Usuário não encontrado.'}), 404
    # Retorna os dados do usuário (excluindo a senha por segurança)
    return jsonify({
        'id': usuario.id,
        'nome': usuario.nome,
        'admin': usuario.admin,
        'ativo': usuario.ativo
    })

@bp.route('/usuarios/<int:usuario_id>/bloquear', methods=['POST'])
@admin_required
def bloquear_usuario(usuario_id):
    sucesso = db_service.bloquear_usuario(usuario_id)
    if not sucesso:
        return jsonify({'error': 'Usuário não encontrado.'}), 404
    return jsonify({'message': 'Usuário bloqueado com sucesso.'})

@bp.route('/usuarios/<int:usuario_id>/desbloquear', methods=['POST'])
@admin_required
def desbloquear_usuario(usuario_id):
    sucesso = db_service.reativar_usuario(usuario_id)
    if not sucesso:
        return jsonify({'error': 'Usuário não encontrado.'}), 404
    return jsonify({'message': 'Usuário desbloqueado com sucesso.'})

# Novo endpoint para logout
@bp.route('/logout', methods=['POST'])
def logout_user():
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Token de autenticação necessário.'}), 401
    token = auth_header.split(' ', 1)[1]
    db_service.deletar_sessao(token)
    return jsonify({'message': 'Logout realizado com sucesso.'}), 200
