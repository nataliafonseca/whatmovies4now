import scripts.util as util
from tinydb import TinyDB, Query
from imdb import IMDb


def generate_db(db_name='db'):
    db = TinyDB(f'{db_name}.json')

    movies = util.get_filmes_50_votos_ou_mais()
    movieids = [str(i) for i in movies.index]
    notas = [str(round((float(i)*2), 2)) for i in movies['rating']]
    titulos = [str(i[:-7]) for i in movies['title']]
    anos = [str(i[-5:-1]) for i in movies['title']]

    imdbcon = IMDb()
    for i, movieid in enumerate(movieids):
        movie = imdbcon.get_movie(movieid)
        dicio = {'id': movieid,
                 'title': f"{movie.get('title', titulos[i])}",
                 'year': f"{movie.get('year', anos[i])}",
                 'rating': f"{movie.get('rating', notas[i])}",
                 'poster': f"{movie.get('cover url', 'https://i.imgur.com/IUozMIm.png')}"}
        print(db.insert(dicio))


def busca_por_id(movieid):
    db = TinyDB('db.json')
    movie = Query()
    mv = db.search(movie.id == f"{movieid}")[0]
    return mv
