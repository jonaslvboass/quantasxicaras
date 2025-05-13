import models.ingredientes_model as ingredientes_model

def converter_medida(ingrediente_id, quantidade, unidade_entrada, unidade_saida):
    ingrediente = ingredientes_model.buscar_ingrediente_por_id(ingrediente_id)
    if not ingrediente:
        return 'Ingrediente não encontrado.'
    nome, ml_por_grama = ingrediente[1], ingrediente[2]
    conversoes = {
        'gramas': 1,
        'xicaras': 240,  # 1 xícara = 240ml
        'colheres_sopa': 15,  # 1 colher de sopa = 15ml
        'colheres_cha': 5  # 1 colher de chá = 5ml
    }
    if unidade_entrada not in conversoes or unidade_saida not in conversoes:
        return 'Unidade desconhecida.'
    # Converter unidade de entrada para gramas
    if unidade_entrada == 'gramas':
        gramas = quantidade
    else:
        ml_total = quantidade * conversoes[unidade_entrada]
        gramas = ml_total / ml_por_grama
    # Converter gramas para unidade de saída
    if unidade_saida == 'gramas':
        resultado = gramas
    else:
        ml_total = gramas * ml_por_grama
        resultado = ml_total / conversoes[unidade_saida]
    return f"{quantidade} {unidade_entrada} de {nome} = {resultado:.2f} {unidade_saida}" 