# Imports necessários
import numpy as np
import pandas as pd
import scripts.util as util
from scripts.grafo import Grafo


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
    lista_todos_usuarios = [str(userid) for userid in util.get_id_todos_os_usuarios()]
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


def gerar_grafo(qntd_usuarios_analisados=None, distancia_maxima=2):
    """
    Gera um grafo para o usuário analisado e salva em grafo.json

    Keyword arguments:
    qntd_usuarios_analisados -- Número de usuários a serem analisados,
        default: None
    """
    vertices = [str(usuario) for usuario in util.get_id_todos_os_usuarios()[:qntd_usuarios_analisados]]
    arestas = []
    for i, user1 in enumerate(vertices):
        for user2 in vertices:
            if user1 != user2 and distancia_dois_usuarios(user1, user2):
                distancia = distancia_dois_usuarios(user1, user2)[2]
                if distancia <= distancia_maxima:
                    arestas.append(f"{user1}-{user2}")
        print(f"USUARIO {i+1}: OK!")
    grafo = Grafo(False, False, vertices, arestas)
    grafo.salvar_grafo("usuarios")
    return grafo


def mais_proximos(usuario_raiz):
    """
    Retorna três camadas de usuários próximos. A primeira, os usuarios
    que estão diretamente conectados ao usuário raiz. A segunda, os que
    estão conectados a estes. A terceira, os conectados aos usuários da
    segunda.

    Keyword arguments:
    usuario_raiz -- id do usuário raiz
    """
    grafo = Grafo.resgatar_grafo()
    return grafo.busca_largura(usuario_raiz)
