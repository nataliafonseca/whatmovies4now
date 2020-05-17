# Imports necessários
import pandas as pd

# Preparando o Dataset
idx = pd.IndexSlice
movies = pd.read_csv("dados/movies.csv", index_col=['movieId'])
ratings = pd.read_csv("dados/ratings.csv")

# Métodos Auxiliares
def getRatingByUser(usuario):
    """Retorna todos os ratings que o usuário (passado por parametro) deu para os filme.

    Keyword arguments:
    usuario -- id do usuário

    """

    rating_by_user = ratings.query("userId==%d" % usuario)
    rating_by_user = rating_by_user[["movieId", "rating"]].set_index("movieId")
    return rating_by_user

def getAllUsersId():
  """Retorna todos os id de todos os usários.

  """

  all_rating = ratings["userId"].unique()
  return all_rating

