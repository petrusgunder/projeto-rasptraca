from codigo import app
from flask import render_template, request, redirect, url_for
from banco_de_dados import MostarUsuarios, CadastrarUsuario, ExcluirUsuario

@app.route("/")
def homepage():
    lista_usuarios = MostarUsuarios()
    return render_template("homepage.html", usuarios=lista_usuarios)

@app.route("/cadastrar", methods=["POST"])
def cadastrar():
    nome = request.form.get("nome")
    cargo = request.form.get("cargo")
    email = request.form.get("email")
    codigo_digital = request.form.get("codigo_digital")
    
    if nome and cargo and email and codigo_digital:
        CadastrarUsuario(nome, cargo, email, codigo_digital)
        
    return redirect(url_for("homepage"))

@app.route("/excluir/<int:id_usuario>")
def excluir(id_usuario):
    ExcluirUsuario(id_usuario)
    return redirect(url_for("homepage"))