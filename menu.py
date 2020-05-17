# Imports necessários
import erros as e

#Função para criação do menu principal
def menuPrincipal():
    """Retorna o ID do usuário a ser recomendado.

    """

    print("="*50)
    print(f"              Sistema de recomendação")
    print("="*50)
    print("")
    msg = "Informe o número do usuário entre 1 e 610: "
    usuario = e.tratarMenu(msg)
    return usuario