from scripts.recomendacao import recomendar_para_usuario
from scripts.filmes_assistidos import ultimos_vistos


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


def imprimir_recentes(usuario):
    recentes = ultimos_vistos(str(usuario))
    print("-" * 50)
    print(f"ULTIMOS VISTOS PELO USUÁRIO {usuario}:")
    print("-" * 50)
    for filme in recentes:
        print(f"Título: {filme['title']}"
              f"\nAno: {filme['year']}"
              f"\nNota: {filme['rating']}"
              f"\nPoster: {filme['poster']}")
        print("-" * 50)


def imprimir_recomendacoes(usuario):
    recomendacoes = recomendar_para_usuario(str(usuario))
    print("-" * 50)
    print(f"RECOMENDAÇÕES PARA O USUÁRIO {usuario}:")
    print("-" * 50)
    for filme in recomendacoes:
        print(f"Título: {filme['title']}"
              f"\nAno: {filme['year']}"
              f"\nNota: {filme['rating']}"
              f"\nPoster: {filme['poster']}")
        print("-" * 50)


user = definir_usuario()
imprimir_recentes(user)
imprimir_recomendacoes(user)


input("\nENTER para finalizar...")
