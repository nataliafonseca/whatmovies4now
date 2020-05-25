# Imports necessários
import pandas as pd

# Preparando o Dataset
idx = pd.IndexSlice
movies = pd.read_csv("dados/movies.csv", index_col=['movieId'])
ratings = pd.read_csv("dados/ratings.csv")
quantidade_de_avaliacoes = ratings["movieId"].value_counts()
movies['ratingsCount'] = quantidade_de_avaliacoes
notas_medias = ratings.groupby("movieId").mean()["rating"]
movies['rating'] = notas_medias


# Métodos Auxiliares
def get_notas_por_usuario(usuario):
    """
    Retorna todos os ratings que o usuário (passado por parametro) deu
    para os filme.

    Keyword arguments:
    usuario -- id do usuário
    """

    notas_por_usuario = ratings.query(f"userId=={usuario}")
    notas_por_usuario = notas_por_usuario[
        ["movieId", "rating", "userId"]].set_index("movieId")
    return notas_por_usuario


def get_id_todos_os_usuarios():
    """
    Retorna os id de todos os usários.
    """

    id_todos_os_usuarios = ratings["userId"].unique()
    return id_todos_os_usuarios


def get_todas_as_notas():
    """
    Retorna todos os notas de todos os usários para todos os filmes.
    """
    todas_as_notas = ratings
    return todas_as_notas


def get_todos_os_filmes():
    """
    Retorna todos os filmes.
    """

    todos_os_filmes = movies[["title", "ratingsCount"]]
    return todos_os_filmes


def get_filmes_50_votos_ou_mais():
    """
    Retorna somente os filmes com 50 ou mais votos.
    """

    all_movies = movies.sort_values("ratingsCount", ascending=False)
    movies_50_rates = all_movies.query("ratingsCount >= 50")
    return movies_50_rates
