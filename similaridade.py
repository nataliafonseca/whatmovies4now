# Imports necessários
import numpy as np
import util as ut
import pandas as pd


# Funções para o calculo de similaridade
def distancia_entre_pontos(a, b):
    """
    Retorna a distância entre dois pontos passados por parâmetro (a e b)
     através de uma função da biblioteca numpy.

    Keyword arguments:
    a -- ponto A
    b -- ponto B
    """

    return np.linalg.norm(a - b)


def distancia_dois_usuarios(usuario_raiz, usuario_destino, qntd_min_filmes=5):
    """
    Retorna a distância entre dois usuários (similaridade). O retorno
    será uma lista [{id do usuario raiz}, {id do usuario destino},
    {distância}]

    Keyword arguments:
    usuario_raiz -- id do usuário raiz
    usuario_destino -- id do outro usuário a ser comparado
    qntd_min_filmes -- quantidade minima de filmes para entrar na
    comparação, default: 5 filmes
    """

    rating_raiz = ut.get_notas_por_usuario(usuario_raiz)
    rating_outros = ut.get_notas_por_usuario(usuario_destino)
    notas_de_filmes_em_comum = rating_raiz.join(rating_outros, lsuffix="_raiz",
                                                rsuffix="_destino").dropna()
    if len(notas_de_filmes_em_comum) < qntd_min_filmes:
        return None
    distancia_entre_usuarios = distancia_entre_pontos(
        notas_de_filmes_em_comum['rating_raiz'],
        notas_de_filmes_em_comum['rating_destino'])
    return [usuario_raiz, usuario_destino, distancia_entre_usuarios]


def distancia_um_para_todos(usuario_raiz, qntd_usuarios_analisados=None):
    """
    Retorna um DataFrame (tabela) com o usuário raiz, os outros usuários
    e o valor da distância entre eles.

    Keyword arguments:
    usuario_raiz -- id do usuário raiz
    qntd_usuarios_analisados -- Número de usuários a serem analisados,
        default: None

    """

    lista_distancias = []
    lista_todos_usuarios = ut.get_id_todos_os_usuarios()
    if qntd_usuarios_analisados:
        lista_todos_usuarios = lista_todos_usuarios[:qntd_usuarios_analisados]
    for usuario in lista_todos_usuarios:
        distancia = distancia_dois_usuarios(usuario_raiz, usuario)
        lista_distancias.append(distancia)
    lista_distancias = list(filter(None, lista_distancias))
    tabela_similaridade = pd.DataFrame(lista_distancias,
                                       columns=["usuario_raiz",
                                                "usuario_destino",
                                                "distancia"])
    return tabela_similaridade


def mais_proximos(usuario_raiz, qntd_usuarios_mais_proximos=10,
                  qntd_usuarios_analisados=None):
    """
    Retorna os valores em ordem de similaridade do usuário raiz com
    todos os outros usuários, excluindo o próprio usuário raiz.
    (Algoritmo de KNN - k-nearest neighbors algorithm)

    Keyword arguments:
    usuario_raiz -- id do usuário raiz
    qntd_usuarios_analisados -- Número de usuários a serem analisados,
        default: None
    qntd_usuarios_mais_proximos -- Quantidade de usuários próximos a
        serem retornados, default: 10
    """

    tabela_similaridade = distancia_um_para_todos(usuario_raiz,
                                                  qntd_usuarios_analisados)
    maior_similaridade = tabela_similaridade.sort_values("distancia")
    maior_similaridade = maior_similaridade.set_index("usuario_destino")
    maior_similaridade = maior_similaridade.drop(usuario_raiz, errors="ignore")
    maior_similaridade = maior_similaridade.head(qntd_usuarios_mais_proximos)
    return maior_similaridade


def gerarGrafo(usuario_raiz):
    grafo = ut.lerGrafo()
    all_users = ut.get_id_todos_os_usuarios()

    distancia_entre_usuarios = distancia_um_para_todos(usuario_raiz)
    lista_distancia = list(distancia_entre_usuarios["distancia"])

    for x in range(1, len(all_users)+1):
        grafo[str(f"{x}")] = []

    grafo[str(f"{usuario_raiz}")] = lista_distancia
    return grafo

