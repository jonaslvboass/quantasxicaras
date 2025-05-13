def renderizar_conversor(ingredientes, resultado=None):
    html = """
        <h1>Bem-vindo ao Quantas Xícaras?</h1>
        <h2>Conversor de Medidas</h2>
        <form method='GET'>
            <label for='ingrediente_id'>Ingrediente:</label>
            <select id='ingrediente_id' name='ingrediente_id' required>
                <option value=''>Selecione um ingrediente</option>
    """
    for i in ingredientes:
        html += f"<option value='{i[0]}'>{i[1]}</option>"
    html += """
            </select><br><br>
            <label for='quantidade'>Quantidade:</label>
            <input type='number' id='quantidade' name='quantidade' step='0.01' required><br><br>
            <label for='unidade_entrada'>Unidade de entrada:</label>
            <select id='unidade_entrada' name='unidade_entrada' required>
                <option value='gramas'>Gramas</option>
                <option value='xicaras'>Xícaras</option>
                <option value='colheres_sopa'>Colheres de Sopa</option>
                <option value='colheres_cha'>Colheres de Chá</option>
            </select><br><br>
            <label for='unidade_saida'>Unidade de saída:</label>
            <select id='unidade_saida' name='unidade_saida' required>
                <option value='gramas'>Gramas</option>
                <option value='xicaras'>Xícaras</option>
                <option value='colheres_sopa'>Colheres de Sopa</option>
                <option value='colheres_cha'>Colheres de Chá</option>
            </select><br><br>
            <button type='submit'>Converter</button>
        </form>
    """
    if resultado:
        html += f"<h3>Resultado: {resultado}</h3>"
    html += "<a href='/home'>Voltar</a>"
    return html 