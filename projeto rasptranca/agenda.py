"""
CRUD dos Laboratorios e Reservas do Sistema de Agenda.
Utiliza a mesma conexao global definida em banco_de_dados.py.
"""
from banco_de_dados import conexao, cursor, PERIODOS


def CriarLabsPadrao():
    """Cria laboratorios de exemplo caso nao exista nenhum."""
    cursor.execute("SELECT COUNT(*) FROM Laboratorio")
    if cursor.fetchone()[0] == 0:
        labs = [
            ("Lab Info 1", "Laboratorio de informatica principal", 30),
            ("Lab Info 2", "Laboratorio de informatica secundario", 25),
            ("Lab Redes", "Laboratorio de redes e hardware", 20),
        ]
        for nome, descricao, capacidade in labs:
            cursor.execute(
                "INSERT INTO Laboratorio (nome, descricao, capacidade) VALUES (?,?,?)",
                (nome, descricao, capacidade),
            )
        conexao.commit()


# ---------- LABORATORIOS ----------

def ListarLaboratorios():
    cursor.execute("SELECT id, nome, descricao, capacidade FROM Laboratorio ORDER BY nome")
    return cursor.fetchall()


def BuscarLaboratorio(id_lab):
    cursor.execute(
        "SELECT id, nome, descricao, capacidade FROM Laboratorio WHERE id = ?", (id_lab,)
    )
    return cursor.fetchone()


def CadastrarLaboratorio(nome, descricao, capacidade):
    cursor.execute(
        "INSERT INTO Laboratorio (nome, descricao, capacidade) VALUES (?,?,?)",
        (nome, descricao, capacidade or 30),
    )
    conexao.commit()


def EditarLaboratorio(id_lab, nome, descricao, capacidade):
    cursor.execute(
        "UPDATE Laboratorio SET nome = ?, descricao = ?, capacidade = ? WHERE id = ?",
        (nome, descricao, capacidade, id_lab),
    )
    conexao.commit()


def ExcluirLaboratorio(id_lab):
    # Remove reservas do lab antes de apagar
    cursor.execute("DELETE FROM Reserva WHERE id_laboratorio = ?", (id_lab,))
    cursor.execute("DELETE FROM Laboratorio WHERE id = ?", (id_lab,))
    conexao.commit()


# ---------- RESERVAS ----------

def ReservarLaboratorio(id_usuario, id_lab, data, periodo, descricao=""):
    """Tenta criar uma reserva. Retorna (True, msg) ou (False, msg)."""
    try:
        cursor.execute(
            "INSERT INTO Reserva (id_usuario, id_laboratorio, data_reserva, periodo, descricao)"
            " VALUES (?,?,?,?,?)",
            (id_usuario, id_lab, data, periodo, descricao),
        )
        conexao.commit()
        return True, "Laboratorio reservado!"
    except Exception as e:
        # UNIQUE(...) impede reserva duplicada no mesmo lab/data/periodo
        return False, "Este periodo ja esta reservado neste laboratorio."


def ReservasDeLaboratorioNaData(id_lab, data):
    """Retorna set dos periodos ja ocupados de um lab numa data."""
    cursor.execute(
        "SELECT periodo FROM Reserva WHERE id_laboratorio = ? AND data_reserva = ?",
        (id_lab, data),
    )
    return {linha[0] for linha in cursor.fetchall()}


def ListarReservasDoUsuario(id_usuario):
    cursor.execute("""
        SELECT Reserva.id, Reserva.data_reserva, Reserva.periodo, Reserva.descricao,
               Laboratorio.nome
        FROM Reserva
        JOIN Laboratorio ON Laboratorio.id = Reserva.id_laboratorio
        WHERE Reserva.id_usuario = ?
        ORDER BY Reserva.data_reserva, Reserva.periodo
    """, (id_usuario,))
    return cursor.fetchall()


def ListarTodasReservas():
    cursor.execute("""
        SELECT Reserva.id, Reserva.data_reserva, Reserva.periodo, Reserva.descricao,
               Laboratorio.nome, SistemaUsuario.nome
        FROM Reserva
        JOIN Laboratorio ON Laboratorio.id = Reserva.id_laboratorio
        JOIN SistemaUsuario ON SistemaUsuario.id = Reserva.id_usuario
        ORDER BY Reserva.data_reserva, Reserva.periodo
    """)
    return cursor.fetchall()


def DisponibilidadeNaData(data):
    """Retorna um dict {id_lab: {periodo: ocupado_bool}} para todos os labs numa data.
    Útil para montar a planilha visual de disponibilidade (pública)."""
    labs = ListarLaboratorios()
    cursor.execute(
        "SELECT id_laboratorio, periodo FROM Reserva WHERE data_reserva = ?", (data,)
    )
    ocupados = {}
    for id_lab, periodo in cursor.fetchall():
        ocupados.setdefault(id_lab, set()).add(periodo)

    grade = {}
    for lab in labs:
        id_lab = lab[0]
        grade[id_lab] = {
            periodo: (id_lab in ocupados and periodo in ocupados[id_lab])
            for periodo in PERIODOS
        }
    return grade


def ExcluirReserva(id_reserva, id_usuario=None, eh_admin=False):
    """Exclui uma reserva. Usuario comum so cancela a propria."""
    if eh_admin:
        cursor.execute("DELETE FROM Reserva WHERE id = ?", (id_reserva,))
    else:
        cursor.execute(
            "DELETE FROM Reserva WHERE id = ? AND id_usuario = ?",
            (id_reserva, id_usuario),
        )
    conexao.commit()


def Periodos():
    """Retorna o dict de periodos (id -> horario)."""
    return PERIODOS
