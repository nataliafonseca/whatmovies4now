"""
Código disponibilizado pelo professor Adolfo Pinto
"""

# Import necessários para esta seção
import pandas as pd

idx = pd.IndexSlice

# Preparando o Dataset
links = pd.read_csv("dados/links.csv", index_col=['movieId'])
movies = pd.read_csv("dados/movies.csv", sep=",", index_col=['movieId'])
ratings = pd.read_csv("dados/ratings.csv", index_col=['userId', 'movieId'])
tags = pd.read_csv("dados/tags.csv", index_col=['userId', 'movieId'])


# Métodos Auxiliares
def get_movies_by_user(id_user, rating_cut=0, list_=False):
    """Retorna a lista de filmes avaliados por um usuário

    Keyword arguments:
    id_user -- id do usuário
    rating_cut -- retorna só itens avaliados com rating maior que rating_cut
    (default: 0)
    list_ -- se True retorna somente os ids dos filmes, se False retorna os
    ids com o valor do rating (default: False)

    """

    return_dict = {}
    dict_ = ratings.loc[idx[id_user, :], 'rating'].T.to_dict()

    for d in dict_:
        if rating_cut != 0:
            if dict_[d] >= rating_cut:
                return_dict[d[1]] = dict_[d]
        else:
            return_dict[d[1]] = dict_[d]

    if list_:
        return list(return_dict.keys())

    return return_dict


def get_users_by_movie(id_movie, rating_cut=0, list_=False):
    """Retorna a lista de usuários que avaliaram determinado filme

    Keyword arguments:
    id_movie -- id do filme
    rating_cut -- retorna só usuários que avaliaram o filme com rating maior
    que rating_cut (default: 0)
    list_ -- se True retorna somente os ids dos usuários, se False retorna
    os ids com o valor do rating

    """

    return_dict = {}
    dict_ = ratings.loc[idx[:, id_movie], 'rating'].T.to_dict()
    for d in dict_:
        if rating_cut != 0:
            if dict_[d] >= rating_cut:
                return_dict[d[0]] = dict_[d]
        else:
            return_dict[d[0]] = dict_[d]

    if list_:
        return list(return_dict.keys())

    return return_dict


def get_rating_by_user_movie(id_user, id_movie):
    """Retorna o rating que o usuário (id_user) deu para um filme (
    id_movie). Se não exister, retorna 0.0.

    Keyword arguments:
    id_user -- id do usuário
    id_movie -- id do filme

    """

    rating = 0.0

    try:
        rating = ratings.loc[idx[id_user, id_movie], 'rating']
    except KeyError as e:
        rating = 0.0

    return rating


def get_all_users():
    """Retorna o id de todos os usuários.

    """

    return list(set([x[0] for x in ratings.index.values]))


def get_movie_title(id_movie):
    """Retorna o título de um filme.

    Keyword arguments:
    id_movie -- id do filme

    """

    info = movies.loc[idx[id_movie], :]
    return info['title']


# Mesmo com esses métodos algumas operações podem ter um certo custo
# computacional já que serão chamadas várias vezes. Por exemplo, quando
# vamos calcular a similaridade de um usuário com todos da base, isso tem um
# certo custo. Por conta disso, algumas informações serão geradas antes e
# armazenadas em variáveis na memória. Tais informações serão geradas nas
# células a seguir. Essas variáveis só serão utilizadas nos métodos em que
# são utilizadas muitas vezes.

'''
    Neste trecho vamos armazenar em memória as informações de filmes 
    avaliados pelos usuários. Isso evitar 
    fazermos muitos acesso a estrutura do DataFrame. 
'''

all_users = get_all_users()

movies_user_true = {}
movies_user_false = {}

for user in all_users:
    movies_user_true[user] = get_movies_by_user(user, list_=True)
    movies_user_false[user] = get_movies_by_user(user, list_=False)
