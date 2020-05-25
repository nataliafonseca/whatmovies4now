# Imports necessários
from flask import Flask, render_template
import scripts.recomendacao as recomendacao
import scripts.util as util


# Criação do app em Flask
app = Flask(__name__)


# Rota inicial ("/")
@app.route("/")
def index():
    return render_template("index.html")


# Rota recomendação ("/recommend")
@app.route("/recommend")
def recommend():
    return render_template("recommend.html")


# Inicializador do projeto com debug
if __name__ == "__main__":
    app.run(debug=True)
