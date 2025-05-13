def renderizar_home(usuario_nome):
    return f"""
        <h1>Bem-vindo ao Quantas Xícaras?</h1>
        <p>Olá, {usuario_nome}!</p>
        <ul>
            <li><a href='/adicionar_receita'>Adicionar Receita</a></li>
            <li><a href='/buscar_receitas'>Buscar Receitas</a></li>
            <li><a href='/gerenciar_estoque'>Gerenciar Estoque</a></li>
            <li><a href='/ingredientes'>Gerenciar Ingredientes</a></li>
            <li><a href='/'>Converter Medidas</a></li>
            <li><a href='/logout'>Sair</a></li>
        </ul>
    """ 