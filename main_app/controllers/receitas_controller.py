from models import receitas_model

def adicionar_receita(nome, modo_preparo, ingredientes, quantidades, autor_id):
    if not nome or not modo_preparo or not ingredientes or not quantidades or not autor_id:
        return 'Todos os campos são obrigatórios.'
    receitas_model.inserir_receita(nome, modo_preparo, ingredientes, quantidades, autor_id)
    return None

def obter_receitas():
    return receitas_model.buscar_receitas()

def obter_receita_por_id(receita_id):
    return receitas_model.buscar_receita_por_id(receita_id)

def recomendar_receitas(usuario_id):
    return receitas_model.recomendar_receitas(usuario_id) 