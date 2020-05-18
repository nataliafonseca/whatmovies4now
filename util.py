# Imports necessários
import pandas as pd

# Preparando o Dataset
idx = pd.IndexSlice
movies = pd.read_csv("dados/movies.csv", index_col=['movieId'])
ratings = pd.read_csv("dados/ratings.csv")
all_ratings = ratings["movieId"].value_counts()
movies['allRatings'] = all_ratings

# Métodos Auxiliares
def getRatingByUser(usuario):
    """Retorna todos os ratings que o usuário (passado por parametro) deu para os filme.

    Keyword arguments:
    usuario -- id do usuário

    """

    rating_by_user = ratings.query("userId==%d" % usuario)
    rating_by_user = rating_by_user[["movieId", "rating", "userId"]].set_index("movieId")
    return rating_by_user


def getAllUsersId():
  """Retorna todos os id de todos os usários.

  """

  all_user_id = ratings["userId"].unique()
  return all_user_id


def getAllRatings():
    """Retorna todos os ratings de todos os usários.

    """

    all_rating = ratings
    return all_rating


def getAllMovies():
    """Retorna todos os filmes.

    """

    all_movies = movies[["title", "allRatings"]]
    return all_movies


def getMovies50Rates():
    """Retorna somente os filmes com 50 ou mais votos.

    """
    all_movies = movies.sort_values("allRatings", ascending=False)
    movies_50_rates = all_movies.query("allRatings >= 50")
    return movies_50_rates
