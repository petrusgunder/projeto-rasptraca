from codigo import app
from datetime import date
from flask import render_template, request, redirect, url_for, session, flash
from autenticacao import login_usuario_required, admin_required
from rpi_luz import AcenderLuz
from usuarios import (
    CadastrarUsuarioSistema, AutenticarUsuario, BuscarUsuarioSistema,
    ListarUsuariosSistema, EditarUsuarioSistema, ExcluirUsuarioSistema,
    VerificarCodigoBarras,
)
from agenda import (
    ListarLaboratorios, CadastrarLaboratorio, EditarLaboratorio, ExcluirLaboratorio,
    ReservarLaboratorio, ReservasDeLaboratorioNaData,
    ListarReservasFuturasDoUsuario, ListarReservasPassadasDoUsuario,
    ReservasDoUsuarioNaData, ListarTodasReservas, ExcluirReserva, Periodos,
    DisponibilidadeNaData,
)


# Disponibiliza o usuario logado, os periodos e a data de hoje para todos os templates
@app.context_processor
def contexto_global():
    return {
        "periodos": Periodos(),
        "hoje": date.today().isoformat(),
        "usuario_sessao": session.get("usuario_nome"),
        "usuario_eh_admin": session.get("usuario_admin", False),
    }


# =====================================================================
#  HOME (PUBLICA) - planilha de disponibilidade + reserva inline
# =====================================================================

@app.route("/")
def home():
    labs = ListarLaboratorios()
    hoje = date.today().isoformat()
    data = request.args.get("data", "") or hoje
    if data < hoje:
        data = hoje  # a grade nunca mostra datas passadas (ficam so no historico)
    grade = DisponibilidadeNaData(data)
    minhas = {}
    if session.get("usuario_id"):
        minhas = ReservasDoUsuarioNaData(session["usuario_id"], data)
    return render_template("home.html", labs=labs, data=data, grade=grade, minhas_reservas=minhas)


@app.route("/reservar", methods=["POST"])
@login_usuario_required
def reservar():
    """Endpoint unico de reserva (usado pela home e pela agenda)."""
    id_lab = request.form.get("laboratorio", type=int)
    data = request.form.get("data")
    periodo = request.form.get("periodo", type=int)
    descricao = request.form.get("descricao", "")
    ok, msg = ReservarLaboratorio(session["usuario_id"], id_lab, data, periodo, descricao)
    flash(msg, "sucesso" if ok else "erro")
    return redirect(url_for("home", data=data))


# =====================================================================
#  LOGIN / LOGOUT
# =====================================================================

@app.route("/login", methods=["GET", "POST"])
def login():
    erro = None
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")
        usuario = AutenticarUsuario(email, senha)
        if usuario:
            session["usuario_id"] = usuario[0]
            session["usuario_nome"] = usuario[1]
            session["usuario_admin"] = bool(usuario[4])
            # vai para o painel ADM se for admin, senao para a home (reserva)
            destino = url_for("admin_dashboard") if usuario[4] else url_for("home")
            return redirect(destino)
        erro = "Email ou senha incorretos."
    return render_template("login.html", erro=erro)


@app.route("/logout")
def logout():
    session.pop("usuario_id", None)
    session.pop("usuario_nome", None)
    session.pop("usuario_admin", None)
    return redirect(url_for("home"))


# =====================================================================
#  CONFIG (MINHA CONTA) - hub do usuario: perfil, reservas, historico
# =====================================================================

@app.route("/config")
@login_usuario_required
def config():
    reservas = ListarReservasFuturasDoUsuario(session["usuario_id"])
    usuario = BuscarUsuarioSistema(session["usuario_id"])
    return render_template("config.html", reservas=reservas, usuario=usuario)


# =====================================================================
#  AGENDA - ver periodos ocupados (reserva feita pela home via /reservar)
# =====================================================================

@app.route("/agenda", methods=["GET"])
@login_usuario_required
def agenda():
    labs = ListarLaboratorios()
    hoje = date.today().isoformat()
    lab_selecionado = request.args.get("laboratorio", type=int)
    data_selecionada = request.args.get("data", "") or hoje
    if data_selecionada < hoje:
        data_selecionada = hoje

    ocupados = set()
    if lab_selecionado is None and labs:
        lab_selecionado = labs[0][0]
    if lab_selecionado and data_selecionada:
        ocupados = ReservasDeLaboratorioNaData(lab_selecionado, data_selecionada)

    return render_template(
        "agenda.html",
        labs=labs,
        lab_selecionado=lab_selecionado,
        data_selecionada=data_selecionada,
        ocupados=ocupados,
    )


@app.route("/minhas_reservas")
@login_usuario_required
def minhas_reservas():
    reservas = ListarReservasFuturasDoUsuario(session["usuario_id"])
    return render_template("minhas_reservas.html", reservas=reservas)


@app.route("/cancelar_reserva/<int:id_reserva>")
@login_usuario_required
def cancelar_reserva(id_reserva):
    ExcluirReserva(id_reserva, session["usuario_id"], eh_admin=session.get("usuario_admin", False))
    destino = request.referrer or ""
    if not destino.startswith("/") or "cancelar_reserva" in destino:
        destino = url_for("config")
    return redirect(destino)


# =====================================================================
#  HISTORICO - reservas passadas (somente leitura)
# =====================================================================

@app.route("/historico")
@login_usuario_required
def historico():
    reservas = ListarReservasPassadasDoUsuario(session["usuario_id"])
    return render_template("historico.html", reservas=reservas)


# =====================================================================
#  VERIFICACAO POR CODIGO DE BARRAS (estacao de hardware - publica)
# =====================================================================

@app.route("/verificar_codigo", methods=["GET", "POST"])
def verificar_codigo():
    resultado = None
    codigo = None
    if request.method == "POST":
        codigo = request.form.get("codigo")
        resultado = VerificarCodigoBarras(codigo)
        AcenderLuz(resultado)  # verde se valido, vermelho se nao

    # mostra o nome do usuario, se encontrado
    nome_usuario = None
    if resultado:
        for u in ListarUsuariosSistema():
            if u[4] and u[4].strip() == (codigo or "").strip():
                nome_usuario = u[1]
                break

    return render_template(
        "verificacao_codigo.html",
        resultado=resultado,
        codigo=codigo,
        nome_usuario=nome_usuario,
    )


# =====================================================================
#  PAINEL ADMINISTRADOR
# =====================================================================

@app.route("/admin")
@admin_required
def admin_dashboard():
    qtd_usuarios = len(ListarUsuariosSistema())
    qtd_labs = len(ListarLaboratorios())
    qtd_reservas = len(ListarTodasReservas())
    return render_template(
        "admin_dashboard.html",
        qtd_usuarios=qtd_usuarios,
        qtd_labs=qtd_labs,
        qtd_reservas=qtd_reservas,
    )


@app.route("/admin/usuarios", methods=["GET", "POST"])
@admin_required
def admin_usuarios():
    mensagem = None
    if request.method == "POST":
        acao = request.form.get("acao")
        if acao == "cadastrar":
            nome = request.form.get("nome")
            email = request.form.get("email")
            senha = request.form.get("senha")
            is_admin = 1 if request.form.get("is_admin") else 0
            codigo_barras = request.form.get("codigo_barras")
            ok, msg = CadastrarUsuarioSistema(nome, email, senha, is_admin, codigo_barras)
            mensagem = msg
        elif acao == "editar":
            id_usuario = request.form.get("id_usuario", type=int)
            nome = request.form.get("nome")
            email = request.form.get("email")
            is_admin = 1 if request.form.get("is_admin") else 0
            codigo_barras = request.form.get("codigo_barras")
            EditarUsuarioSistema(id_usuario, nome, email, is_admin, codigo_barras)
            mensagem = "Usuario atualizado."
        elif acao == "excluir":
            id_usuario = request.form.get("id_usuario", type=int)
            ExcluirUsuarioSistema(id_usuario)
            mensagem = "Usuario excluido."

    usuarios = ListarUsuariosSistema()
    return render_template("admin_usuarios.html", usuarios=usuarios, mensagem=mensagem)


@app.route("/admin/laboratorios", methods=["GET", "POST"])
@admin_required
def admin_laboratorios():
    mensagem = None
    if request.method == "POST":
        acao = request.form.get("acao")
        if acao == "cadastrar":
            nome = request.form.get("nome")
            descricao = request.form.get("descricao")
            capacidade = request.form.get("capacidade", type=int)
            CadastrarLaboratorio(nome, descricao, capacidade or 30)
            mensagem = "Laboratorio cadastrado."
        elif acao == "editar":
            id_lab = request.form.get("id_lab", type=int)
            nome = request.form.get("nome")
            descricao = request.form.get("descricao")
            capacidade = request.form.get("capacidade", type=int)
            EditarLaboratorio(id_lab, nome, descricao, capacidade or 30)
            mensagem = "Laboratorio atualizado."
        elif acao == "excluir":
            id_lab = request.form.get("id_lab", type=int)
            ExcluirLaboratorio(id_lab)
            mensagem = "Laboratorio excluido."

    labs = ListarLaboratorios()
    return render_template("admin_laboratorios.html", labs=labs, mensagem=mensagem)


@app.route("/admin/reservas")
@admin_required
def admin_reservas():
    reservas = ListarTodasReservas()
    return render_template("admin_reservas.html", reservas=reservas)
