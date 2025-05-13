def renderizar_lista_ingredientes(ingredientes):
    html = """
        <h2>Ingredientes Cadastrados</h2>
        <a href='/adicionar_ingrediente' class='button'>Adicionar Novo Item</a><br><br>
        <ul>
    """
    for i in ingredientes:
        html += f"<li>{i[1]} (ml/g: {i[2] if len(i) > 2 else ''})</li>"
    html += """
        </ul>
        <a href='/home'>Voltar</a>
    """
    return html

def renderizar_formulario_adicionar_ingrediente():
    return """
        <h2>Adicionar Ingrediente</h2>
        <form method='POST'>
            <label for='nome'>Nome:</label>
            <input type='text' id='nome' name='nome' required><br><br>
            <label for='ml_por_grama'>ml por grama:</label>
            <input type='number' id='ml_por_grama' name='ml_por_grama' step='0.01' required><br><br>
            <button type='submit'>Adicionar</button>
        </form>
        <a href='/home'>Voltar</a>
    """ 