from flask import Flask
from banco_de_dados import conexao
from usuarios import CriarAdminPadrao
from agenda import CriarLabsPadrao

app = Flask(__name__)
app.secret_key = "troque-essa-chave-por-algo-secreto"  # necessário para a sessão/login funcionar

# Cria administrador padrao e laboratorios iniciais (apenas se ainda nao existirem)
CriarAdminPadrao()
CriarLabsPadrao()

from routes import *


if __name__ == "__main__":
    app.run(debug=True)
