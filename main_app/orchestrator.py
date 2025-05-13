from models import schema

if __name__ == '__main__':
    print('Resetando banco de dados...')
    schema.resetar_banco()
    print('Adicionando ingredientes padrão...')
    schema.adicionar_ingredientes_padrao()
    print('Banco de dados pronto para uso!') 