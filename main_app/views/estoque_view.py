def renderizar_formulario_adicionar_estoque(ingredientes):
    return f"""
        <h2>Adicionar Item ao Estoque</h2>
        <form method='POST'>
            <label for='ingrediente_id'>Ingrediente:</label>
            <select id='ingrediente_id' name='ingrediente_id' required>
                <option value=''>Selecione um ingrediente</option>
                {''.join(f'<option value="{i[0]}">{i[1]}</option>' for i in ingredientes)}
            </select><br><br>
            <label for='quantidade'>Quantidade (g):</label>
            <input type='number' id='quantidade' name='quantidade' step='0.01' required><br><br>
            <button type='submit'>Adicionar</button>
        </form>
        <a href='/gerenciar_estoque'>Voltar</a>
    """

def renderizar_lista_estoque(itens):
    html = """
        <h2>Meu Estoque</h2>
        <a href='/adicionar_estoque' class='button'>Adicionar Novo Item</a><br><br>
        <style>
            .button { display: inline-block; padding: 8px 16px; background-color: #4CAF50; color: white; text-decoration: none; border-radius: 4px; margin-bottom: 10px; }
            .button:hover { background-color: #45a049; }
            table { width: 100%; border-collapse: collapse; }
            th, td { padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }
            th { background-color: #f2f2f2; }
            tr:hover { background-color: #f5f5f5; }
            .actions a { margin-right: 10px; color: #0066cc; text-decoration: none; }
            .actions a:hover { text-decoration: underline; }
        </style>
    """
    if itens:
        html += """
            <table>
                <tr>
                    <th>Ingrediente</th>
                    <th>Quantidade (g)</th>
                    <th>Ações</th>
                </tr>
        """
        for item in itens:
            html += f"""
                <tr>
                    <td>{item['nome']}</td>
                    <td>{item['quantidade']:.2f}</td>
                    <td class='actions'>
                        <a href='/editar_estoque/{item['id']}'>Editar</a>
                        <a href='/excluir_estoque/{item['id']}' onclick="return confirm('Tem certeza que deseja excluir este item?')">Excluir</a>
                    </td>
                </tr>
            """
        html += "</table>"
    else:
        html += "<p>Nenhum item no estoque. Comece adicionando ingredientes!</p>"
    html += "<br><a href='/home' class='button'>Voltar ao Menu</a>"
    return html

def renderizar_formulario_editar_estoque(item):
    return f"""
        <h2>Editar Item do Estoque</h2>
        <form method='POST'>
            <p><strong>Ingrediente:</strong> {item['nome']}</p>
            <label for='quantidade'>Quantidade (g):</label>
            <input type='number' id='quantidade' name='quantidade' step='0.01' value='{item['quantidade']:.2f}' required><br><br>
            <button type='submit'>Atualizar</button>
        </form>
        <a href='/gerenciar_estoque'>Voltar</a>
    """ 