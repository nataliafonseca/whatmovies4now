import util
from tinydb import TinyDB, Query
from imdb import IMDb


def generate_db():
    db = TinyDB('db.json')

    movieids = [str(i) for i in util.get_filmes_50_votos_ou_mais().index]
    notas = [str(i) for i in util.get_filmes_50_votos_ou_mais()['rating']]
    titulos = [str(i[:-7]) for i in util.get_filmes_50_votos_ou_mais()['title']]
    anos = [str(i[-5:-1]) for i in util.get_filmes_50_votos_ou_mais()['title']]

    imdbcon = IMDb()
    for i, movieid in enumerate(movieids):
        movie = imdbcon.get_movie(movieid)
        dicio = {'id': movieid,
                 'title': f"{movie.get('title', titulos[i])}",
                 'year': f"{movie.get('year', anos[i])}",
                 'rating': f"{movie.get('rating', notas[i])}",
                 'poster': f"{movie.get('cover url', None)}"}
        print(db.insert(dicio))

# Buscar na DB
# db = TinyDB('db.json')
# movie = Query()
# mv = db.search(movie.id == '356')
# print(mv[0])
