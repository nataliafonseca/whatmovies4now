# Imports necessários
import os
from flask import Flask, render_template
import scripts.recomendacao as recomendacao
import scripts.filmes_assistidos as filmes_assistidos


# Criação do app em Flask
app = Flask(__name__)


# Rota inicial ("/")
@app.route("/")
def index():
    return render_template("index.html")


# Rota recomendação ("/recommend")
@app.route('/recommend/<user_id>')
def recommend(user_id):

    filmes_assistidos_usuario = filmes_assistidos.ultimos_vistos(user_id)

    recomendacao_usuario = recomendacao.recomendar_para_usuario(user_id)

    #Tratamento se o usuário não possuir recomendação ou filmes assistidos
    if recomendacao_usuario is None:
        rec1 = None
        rec2 = None
    else:
        rec1 = recomendacao_usuario[0:5]
        rec2 = recomendacao_usuario[5:10]

    if filmes_assistidos_usuario is None:
        assistidos1 = None
        assistidos2 = None
    else:
        assistidos1 = filmes_assistidos_usuario[0:5]
        assistidos2 = filmes_assistidos_usuario[5:10]

    args = {
        'user_id': user_id,
        'filmes_assistidos_usuario': filmes_assistidos_usuario,
        'recomendacao_usuario': recomendacao_usuario,
        'rec1': rec1,
        'rec2': rec2,
        'assistidos1': assistidos1,
        'assistidos2': assistidos2,
    }

    return render_template("recommend.html", args=args)


# Inicializador do projeto com debug
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
