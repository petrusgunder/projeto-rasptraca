from codigo import app
from flask import render_template, request, redirect, url_for, session
from banco_de_dados import MostarUsuarios, CadastrarUsuario, ExcluirUsuario
from codigo_de_verificacao import VerificarDigital
from autenticacao import login_required, SENHA_ACESSO
from rpi_luz import AcenderLuz

@app.route("/login", methods=["GET", "POST"])
def login():
    erro = None
    if request.method == "POST":
        senha = request.form.get("senha")
        if senha == SENHA_ACESSO:
            session["logado"] = True
            return redirect(url_for("homepage"))
        erro = "Senha incorreta."
    return render_template("login.html", erro=erro)

@app.route("/logout")
def logout():
    session.pop("logado", None)
    return redirect(url_for("login"))

@app.route("/")
@login_required
def homepage():
    lista_usuarios = MostarUsuarios()
    return render_template("homepage.html", usuarios=lista_usuarios)

@app.route("/cadastrar", methods=["POST"])
@login_required
def cadastrar():
    nome = request.form.get("nome")
    cargo = request.form.get("cargo")
    email = request.form.get("email")
    codigo_digital = request.form.get("codigo_digital")

    if nome and cargo and email and codigo_digital:
        CadastrarUsuario(nome, cargo, email, codigo_digital)

    return redirect(url_for("homepage"))

@app.route("/excluir/<int:id_usuario>")
@login_required
def excluir(id_usuario):
    ExcluirUsuario(id_usuario)
    return redirect(url_for("homepage"))

@app.route("/verificacao", methods=["GET", "POST"])
def verificacao():
    resultado = None
    codigo_digital = None

    if request.method == "POST":
        codigo_digital = request.form.get("codigo_digital")
        resultado = VerificarDigital(codigo_digital)
        if resultado:
            AcenderLuz()  # acende a luz no Raspberry Pi ao invés de só mostrar no navegador

    return render_template(
        "verificacao.html",
        resultado=resultado,
        codigo_digital=codigo_digital
    )
