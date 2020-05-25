# Imports necessários
import scripts.util as util
import scripts.imdb_to_db as imdb_to_db


def ultimos_vistos(usuario):
    notas_do_usuario = util.get_notas_por_usuario(usuario)
    filmes_50_ou_mais = [str(i) for i in util.get_filmes_50_votos_ou_mais().index]
    notas_do_usuario = notas_do_usuario.query("movieId in @filmes_50_ou_mais")
    filmes_ja_assistidos = [int(filme) for filme in notas_do_usuario.index]
    filmes_ja_assistidos = [imdb_to_db.busca_por_id(filme) for filme in filmes_ja_assistidos][::-1]
    if len(filmes_ja_assistidos) >= 10:
        filmes_ja_assistidos = filmes_ja_assistidos[0:10]

    return filmes_ja_assistidos

