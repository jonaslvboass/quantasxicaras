from models import estoque_model

def adicionar_estoque(usuario_id, ingrediente_id, quantidade):
    if not usuario_id or not ingrediente_id or quantidade is None:
        return 'Todos os campos são obrigatórios.'
    estoque_model.inserir_estoque(usuario_id, ingrediente_id, quantidade)
    return None

def obter_estoque(usuario_id):
    return estoque_model.buscar_estoque(usuario_id)

def editar_estoque(item_id, usuario_id, quantidade):
    if not item_id or not usuario_id or quantidade is None:
        return 'Todos os campos são obrigatórios.'
    estoque_model.atualizar_estoque(item_id, usuario_id, quantidade)
    return None

def excluir_estoque(item_id, usuario_id):
    if not item_id or not usuario_id:
        return 'Todos os campos são obrigatórios.'
    estoque_model.deletar_estoque(item_id, usuario_id)
    return None

def obter_item_estoque(item_id, usuario_id):
    return estoque_model.buscar_item_estoque(item_id, usuario_id) 