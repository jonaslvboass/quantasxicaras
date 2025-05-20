def renderizar_cadastro():
    return """
        <h2>Cadastro de Cozinheiro(a)</h2>
        <form method='POST'>
            <label for='nome'>Nome:</label>
            <input type='text' id='nome' name='nome' required><br><br>
            <label for='senha'>Senha:</label>
            <input type='password' id='senha' name='senha' required><br><br>
            <label for='admin'>Administrador?</label>
            <input type='checkbox' id='admin' name='admin' value='1'><br><br>
            <button type='submit'>Cadastrar</button>
        </form>
        <a href='/home'>Voltar</a>
    """

def renderizar_login():
    return """
        <h1>Bem-vindo ao Quantas Xícaras?</h1>
        <p>Por favor, faça login ou <a href='/cadastro'>cadastre-se</a>.</p>
        <h2>Login</h2>
        <form method='POST'>
            <label for='nome'>Nome:</label>
            <input type='text' id='nome' name='nome' required><br><br>
            <label for='senha'>Senha:</label>
            <input type='password' id='senha' name='senha' required><br><br>
            <button type='submit'>Logar</button>
        </form>
        <a href='/home'>Voltar</a>
    """ 