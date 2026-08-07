from flask import Flask
from banco_de_dados import conexao

app = Flask(__name__)
app.secret_key = "troque-essa-chave-por-algo-secreto"  # necessário para a sessão/login funcionar

from routes import *


if __name__ == "__main__":
    app.run(debug=True)
