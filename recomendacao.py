# Imports necessários
import similaridade as sim
import util as ut

#Funções para a recomendação
def recomendacao(usuario_raiz, qntd_usuario, qntd_recomendacao = None):
    """Retorna os filmes recomendados para o usuário informado.

    Keyword arguments:
    usuario_raiz -- id do usuário raiz
    qntd_usuario -- Número de usuários a serem analisados, default: 60 (10% da base de dados)
    qntd_recomendacao -- Quantidade de filmes a serem recomendados ao usuário raiz, default: 10 filmes

    """

    rating_raiz = ut.getRatingByUser(usuario_raiz)
    movies_raiz = rating_raiz.index

    usuarios_mais_similares = sim.maiorSimilaridade(usuario_raiz, qntd_usuario, qntd_recomendacao)
    usuarios_outros_similares = usuarios_mais_similares.index

    rating = ut.getAllRatings().set_index("movieId").loc[ut.getMovies50Rates().index]
    rating = rating.reset_index()

    rating_outros_simalares = rating.set_index("userId").loc[usuarios_outros_similares]
    media_ratings_outros_similares = rating_outros_simalares.groupby("movieId").mean()[["rating"]]
    qntd_visualizacoes = rating_outros_simalares.groupby("movieId").count()[["rating"]]

    filtro = qntd_usuario / 2
    media_ratings_outros_similares = media_ratings_outros_similares.join(qntd_visualizacoes, lsuffix="_mean", rsuffix="_visualizacoes")
    recommend = media_ratings_outros_similares.query("rating_visualizacoes >= %.2f" % filtro)
    recommend = recommend.sort_values("rating_mean", ascending=False)
    recommend = recommend.drop(movies_raiz, errors="ignore")
    recommend = recommend.join(ut.getMovies50Rates())
    return recommend

print(recomendacao(1, 50))


