import requests

AUTH_API_URL = 'http://localhost:5001'

def cadastrar_usuario(nome, senha, admin=False, admin_token=None):
    if not nome or not senha:
        return 'Nome e senha são obrigatórios.'
    payload = {'nome': nome, 'senha': senha}
    if admin:
        payload['admin'] = True
    headers = {}
    if admin and admin_token:
        headers['Authorization'] = f'Bearer {admin_token}'
    resp = requests.post(f'{AUTH_API_URL}/register', json=payload, headers=headers)
    if resp.status_code == 201:
        return None
    else:
        return resp.json().get('error', 'Erro ao cadastrar usuário.')

def autenticar_usuario(nome, senha):
    resp = requests.post(f'{AUTH_API_URL}/login', json={'nome': nome, 'senha': senha})
    if resp.status_code == 200:
        data = resp.json()
        return {
            'usuario_id': data.get('usuario_id'),
            'nome': nome,
            'token': data.get('token', ''),
            'admin': data.get('admin', False)
        }
    return None 