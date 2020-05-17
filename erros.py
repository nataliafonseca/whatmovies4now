#Função de tratamento de erro do menu
def tratarMenu(msg):
    """Retorna o menu tratado para valores fora do indice esperado

    Keyword arguments:
    msg -- mensagem a ser passada

    """

    try:
        opcao = int(input(msg))
        if opcao > 1 and opcao <= 610:
            return opcao
        else:
            print("Informação invalida, digite um número de usuário entre 1 e 610")
            return tratarMenu(msg)
    except:
        print("Informação invalida, digite um número de usuário entre 1 e 610")
        return tratarMenu(msg)