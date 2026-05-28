from flask import Flask
from banco_de_dados import conexao

app = Flask(__name__)

from routes import *


if __name__ == "__main__":
    app.run(debug=True)