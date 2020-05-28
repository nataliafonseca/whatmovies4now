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
    """
    Imprime os filmes recentes assistidos pelo usuário
    """
    recentes = ultimos_vistos(str(usuario))
    print("-" * 50)
    print(f"ULTIMOS VISTOS PELO USUÁRIO {usuario}:")
    print("-" * 50)
    if recentes:
        for filme in recentes:
            print(f"Título: {filme['title']}"
                  f"\nAno: {filme['year']}"
                  f"\nNota: {filme['rating']}"
                  f"\nPoster: {filme['poster']}")
            print("-" * 50)
    else:
        print("O usuário ainda não assistiu nenhum filme.")


def imprimir_recomendacoes(usuario):
    """
    Imprime a recomendação de filmes para o pelo usuário
    """
    recomendacoes = recomendar_para_usuario(str(usuario))
    print("-" * 50)
    print(f"RECOMENDAÇÕES PARA O USUÁRIO {usuario}:")
    print("-" * 50)
    if recomendacoes:
        for filme in recomendacoes:
            print(f"Título: {filme['title']}"
                  f"\nAno: {filme['year']}"
                  f"\nNota: {filme['rating']}"
                  f"\nPoster: {filme['poster']}")
            print("-" * 50)
    else:
        print("O usuário ainda não possui recomendações.")


user = definir_usuario()
imprimir_recentes(user)
imprimir_recomendacoes(user)


input("\nENTER para finalizar...")
