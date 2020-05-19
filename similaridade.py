# Imports necessários
import numpy as np
import pandas as pd
import util
from grafo import Grafo
from jsonpickle import encode


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

    rating_raiz = util.get_notas_por_usuario(usuario_raiz)
    rating_outros = util.get_notas_por_usuario(usuario_destino)
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
    lista_todos_usuarios = util.get_id_todos_os_usuarios()
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


def distancia_um_para_posteriores(usuario_raiz, qntd_usuarios_analisados=None):
    """
    Adaptação do método distancia_um_para_todos para calcular somente
    a distancia para os usuarios com id de valor superior, para evitar
    repetições de arestas na geração do grafo.

    Keyword arguments:
    usuario_raiz -- id do usuário raiz
    qntd_usuarios_analisados -- Número de usuários a serem analisados,
        default: None
    """
    lista_distancias = []
    lista_todos_usuarios = [str(usuario) for usuario in util.get_id_todos_os_usuarios()]

    if qntd_usuarios_analisados:
        lista_todos_usuarios = lista_todos_usuarios[:qntd_usuarios_analisados]
    for usuario_destino in lista_todos_usuarios:
        if usuario_destino > usuario_raiz:
            distancia = distancia_dois_usuarios(usuario_raiz, usuario_destino)
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


def gerar_grafo(qntd_usuarios_analisados=None):
    vertices = [str(vertice) for vertice in util.get_id_todos_os_usuarios()]
    if qntd_usuarios_analisados:
        vertices = vertices[:qntd_usuarios_analisados]
    arestas = []
    for idx, usuario in enumerate(vertices):
        tabela_similaridade = distancia_um_para_posteriores(usuario, qntd_usuarios_analisados=qntd_usuarios_analisados)
        tabela_similaridade = tabela_similaridade[tabela_similaridade.usuario_destino != usuario]
        for index, row in tabela_similaridade.iterrows():
            arestas.append(f"{int(row['usuario_raiz'])}-{int(row['usuario_destino'])}-{row['distancia']}")
        print(f"\nUSUARIO {idx+1} OK!")

    grafo = Grafo(False, True, vertices, arestas)

    with open("grafo.json", "w") as grafos_json:
        grafos_json.write(encode(grafo) + "\n")
