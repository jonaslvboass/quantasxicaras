from models import ingredientes_model

def obter_ingredientes():
    return ingredientes_model.buscar_ingredientes()

def obter_ingrediente_por_id(ingrediente_id):
    return ingredientes_model.buscar_ingrediente_por_id(ingrediente_id)

def adicionar_ingrediente(nome, ml_por_grama):
    if not nome or ml_por_grama is None:
        return 'Nome e ml_por_grama são obrigatórios.'
    ingredientes_model.inserir_ingrediente(nome, ml_por_grama)
    return None 