from recomendacao import recomendar_para_usuario


def definir_usuario():
    """
    Pede o usuário a ser recomendado e trata para valores fora do índice.
    """
    print("-" * 50)
    print("SISTEMA DE RECOMENDAÇÃO")
    print("-" * 50)
    entrada = int(input("Informe o número do usuário entre 1 e 610: "))
    if 1 <= entrada <= 610:
        return entrada
    else:
        print("Informação invalida, digite um número de usuário entre 1 e 610")
        return definir_usuario()


usuario = definir_usuario()

print()
print("-" * 50)
print(f"RECOMENDAÇÕES PARA O USUÁRIO {usuario}:")
print("-" * 50)
print()

print(recomendar_para_usuario(str(usuario)))

input("\nENTER para finalizar...")
