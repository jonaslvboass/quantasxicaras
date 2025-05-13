from models import cozinheiros_model

def cadastrar_usuario(nome, senha):
    if not nome or not senha:
        return 'Nome e senha são obrigatórios.'
    if cozinheiros_model.buscar_usuario_por_nome(nome):
        return 'Usuário já existe.'
    cozinheiros_model.inserir_usuario(nome, senha)
    return None

def autenticar_usuario(nome, senha):
    usuario = cozinheiros_model.buscar_usuario_por_nome(nome)
    if usuario and usuario[2] == senha:
        return {'usuario_id': usuario[0], 'nome': usuario[1]}
    return None

def buscar_usuario_por_nome(nome):
    return cozinheiros_model.buscar_usuario_por_nome(nome) 