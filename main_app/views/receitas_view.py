def renderizar_formulario_adicionar_receita(ingredientes):
    return f"""
        <h2>Cadastro de Receita</h2>
        <form method='POST'>
            <label for='nome'>Nome:</label>
            <input type='text' id='nome' name='nome' required><br><br>
            <div id='ingredientes'>
                <h3>Ingredientes:</h3>
                <div class='ingrediente-item'>
                    <select name='ingrediente_id[]' required>
                        <option value=''>Selecione um ingrediente</option>
                        {''.join(f'<option value="{i[0]}">{i[1]}</option>' for i in ingredientes)}
                    </select>
                    <input type='number' name='quantidade[]' step='0.01' placeholder='Quantidade (g)' required>
                </div>
            </div>
            <button type='button' onclick='addIngrediente()'>+ Adicionar Ingrediente</button><br><br>
            <label for='modo_preparo'>Modo de Preparo:</label><br>
            <textarea id='modo_preparo' name='modo_preparo' rows='4' cols='50' required></textarea><br><br>
            <button type='submit'>Cadastrar</button>
        </form>
        <script>
            function addIngrediente() {{
                const div = document.createElement('div');
                div.className = 'ingrediente-item';
                div.innerHTML = `
                    <select name='ingrediente_id[]' required>
                        <option value=''>Selecione um ingrediente</option>
                        {''.join(f'<option value=\"{i[0]}\">{i[1]}</option>' for i in ingredientes)}
                    </select>
                    <input type='number' name='quantidade[]' step='0.01' placeholder='Quantidade (g)' required>
                `;
                document.getElementById('ingredientes').appendChild(div);
            }}
        </script>
        <a href='/home'>Voltar</a>
    """

def renderizar_lista_receitas(receitas):
    html = """
        <h2>Receitas Disponíveis</h2>
        <div style='margin: 20px;'>
    """
    for r in receitas:
        html += f"""
            <div style='margin-bottom: 30px; border: 1px solid #ccc; padding: 15px; border-radius: 5px;'>
                <h3>{r['nome']}</h3>
                <div>
                    <strong>Ingredientes:</strong>
                    <ul>
                        {''.join(f'<li>{ing}</li>' for ing in r['ingredientes'])}
                    </ul>
                </div>
                <div>
                    <strong>Modo de Preparo:</strong>
                    <p style='white-space: pre-line;'>{r['modo_preparo']}</p>
                </div>
            </div>
        """
    html += """
        </div>
        <a href='/home'>Voltar</a>
    """
    return html

def renderizar_recomendacoes(receitas):
    html = """
        <h2>Receitas Recomendadas</h2>
        <div style='margin: 20px;'>
    """
    if not receitas:
        html += "<p>Você não pode fazer nenhuma receita cadastrada.</p>"
    else:
        for r in receitas:
            html += f"""
                <div class='receita possivel'>
                    <h3>{r['nome']}</h3>
                    <p><strong>Ingredientes necessários:</strong></p>
                    <ul>
                        {''.join(f'<li>{ing}</li>' for ing in r['ingredientes'])}
                    </ul>
                    <p><strong>Modo de Preparo:</strong></p>
                    <p style='white-space: pre-line;'>{r['modo_preparo']}</p>
                </div>
            """
    html += """
        </div>
        <a href='/home'>Voltar</a>
    """
    return html 