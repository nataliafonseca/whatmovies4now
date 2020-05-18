# Imports necessários
import numpy as np
import util as ut
import pandas as pd

#Funções para o calculo de similaridade
def distanciaEntrePontos(a,b):
    """Retorna a distância entre dois pontos passados por parâmetro (a e b) através de uma função da biblioteca numpy.

    Keyword arguments:
    a -- ponto A
    b -- ponto b

    """

    return np.linalg.norm(a-b)


def calculoSimilaridade(usuario_raiz, outros_usuarios, qntd_min_filmes = 5):
    """Retorna uma lista com a distância entre dois usuários (similaridade).

    Keyword arguments:
    usuario_raiz -- id do usuário raiz
    outros_usuarios -- id do outro usuário a ser comparado com o usuário raiz
    qntd_min_filmes -- quantidade minima de filmes para entrar na comparação, default: 5 filmes

    """

    rating_raiz = ut.getRatingByUser(usuario_raiz)
    rating_outros = ut.getRatingByUser(outros_usuarios)
    notas_de_filmes_em_comum = rating_raiz.join(rating_outros, lsuffix="_raiz", rsuffix="_outro").dropna()
    if (len(notas_de_filmes_em_comum) < qntd_min_filmes):
        return None
    distancia_entre_usuarios = distanciaEntrePontos(notas_de_filmes_em_comum['rating_raiz'], notas_de_filmes_em_comum['rating_outro'])
    return [usuario_raiz, outros_usuarios, distancia_entre_usuarios]


def calculoSimilaridadeTotal(usuario_raiz, usuarios_analisados = None):
    """Retorna um DataFrame (tabela) com o usuário raiz, os outros usuários similares e o valor da similaridade entre eles.

    Keyword arguments:
    usuario_raiz -- id do usuário raiz
    usuarios_analisados -- Número de usuários a serem analisados, default: None

    """

    lista_similaridade = []
    lista_todos_usuarios = ut.getAllUsersId()
    if usuarios_analisados:
        lista_todos_usuarios = lista_todos_usuarios[:lista_todos_usuarios]
    for userId in lista_todos_usuarios:
        similaridade = calculoSimilaridade(usuario_raiz, userId)
        lista_similaridade.append(similaridade)
    lista_similaridade = list(filter(None, lista_similaridade))
    tabela_similaridade = pd.DataFrame(lista_similaridade, columns=["usuario_raiz", "usuario_outro", "similaridade"])
    return tabela_similaridade


def maiorSimilaridade(usuario_raiz, qntd_usuarios = 10, usuarios_analisados = None):
    """Retorna os valores em ordem de similaridade do usuário raiz com todos os outros usuários, excluindo o usuário raiz. (Algoritmo de KNN - k-nearest neighbors algorithm)

    Keyword arguments:
    usuario_raiz -- id do usuário raiz
    usuarios_analisados -- Número de usuários a serem analisados, default: None
    qntd_usuarios -- Quantidade de usuários, default: 10 filmes

    """

    tabela_similaridade = calculoSimilaridadeTotal(usuario_raiz, usuarios_analisados)
    maior_similaridade = tabela_similaridade.sort_values("similaridade")
    maior_similaridade = maior_similaridade.set_index("usuario_outro").drop(usuario_raiz, errors="ignore")
    maior_similaridade.head(qntd_usuarios)
    return maior_similaridade

