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


def calculoSimilaridade(usuario_raiz, outros_usuarios, qntd_min_filmes = 5, similaridadeMax = 999999):
    """Retorna uma lista com a distância entre dois usuários (similaridade).

    Keyword arguments:
    usuario_raiz -- id do usuário raiz
    outros_usuarios -- id do outro usuário a ser comparado com o usuário raiz
    qntd_filmes -- quantidade minima de filmes para entrar na comparação
    similaridadeMax -- se o critério de quantidade de filmes minima não for atendida, será atribuido o valor 999999 a similaridade

    """

    rating_raiz = ut.getRatingByUser(usuario_raiz)
    rating_outros = ut.getRatingByUser(outros_usuarios)
    notas_de_filmes_em_comum = rating_raiz.join(rating_outros, lsuffix="_raiz", rsuffix="_outro").dropna()
    if (len(notas_de_filmes_em_comum) < qntd_min_filmes):
        return [usuario_raiz, outros_usuarios, similaridadeMax]
    distancia_entre_usuarios = distanciaEntrePontos(notas_de_filmes_em_comum['rating_raiz'], notas_de_filmes_em_comum['rating_outro'])
    return [usuario_raiz, outros_usuarios, distancia_entre_usuarios]


def calculoSimilaridadeTotal(usuario_raiz):
    """Retorna um DataFrame (tabela) com o usuário raiz, os outros usuários similares e o valor da similaridade entre eles.

    Keyword arguments:
    usuario_raiz -- id do usuário raiz

    """

    lista_similaridade = []
    for userId in ut.getAllUsersId():
        similaridade = calculoSimilaridade(usuario_raiz, userId)
        lista_similaridade.append(similaridade)
    tabela_similaridade = pd.DataFrame(lista_similaridade, columns=["usuario_raiz", "usuario_outro", "similaridade"])
    return tabela_similaridade


def menorSimilaridade(usuario_raiz):
    """Retorna os valores em ordem de similaridade do usuário raiz com todos os outros usuários, excluindo o usuário raiz.

    Keyword arguments:
    usuario_raiz -- id do usuário raiz

    """

    tabela_similaridade = calculoSimilaridadeTotal(usuario_raiz)
    menor_similaridade = tabela_similaridade.sort_values("similaridade")
    menor_similaridade = menor_similaridade.set_index("usuario_outro").drop(usuario_raiz)
    return menor_similaridade

