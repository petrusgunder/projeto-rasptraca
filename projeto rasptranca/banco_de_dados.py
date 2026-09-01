import sqlite3

conexao = sqlite3.connect("banco.db", check_same_thread=False)
cursor = conexao.cursor()

cursor.executescript("""
    CREATE TABLE IF NOT EXISTS Usuario(
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nome VARCHAR(50) NOT NULL,
        cargo VARCHAR(10) NOT NULL,
        email VARCHAR(50) NOT NULL
    );
               
    CREATE TABLE IF NOT EXISTS Digital(
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        codigo VARCHAR(10) NOT NULL
    );
               
    CREATE TABLE IF NOT EXISTS UsuarioDigital(
        id_usuario INTEGER NOT NULL,
        id_digital INTEGER NOT NULL,
        FOREIGN KEY (id_usuario) REFERENCES Usuario(id),
        FOREIGN KEY (id_digital) REFERENCES Digital(id)
    );

    -- Usuarios do Sistema de Agenda (login com email/senha)
    CREATE TABLE IF NOT EXISTS SistemaUsuario (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nome VARCHAR(100) NOT NULL,
        email VARCHAR(100) NOT NULL UNIQUE,
        senha_hash VARCHAR(200) NOT NULL,
        is_admin BOOLEAN NOT NULL DEFAULT 0,
        criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Laboratorios do Sistema de Agenda
    CREATE TABLE IF NOT EXISTS Laboratorio (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nome VARCHAR(50) NOT NULL,
        descricao VARCHAR(200),
        capacidade INTEGER NOT NULL DEFAULT 30
    );

    -- Reservas de Laboratorio
    CREATE TABLE IF NOT EXISTS Reserva (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        id_usuario INTEGER NOT NULL,
        id_laboratorio INTEGER NOT NULL,
        data_reserva DATE NOT NULL,
        periodo INTEGER NOT NULL,
        descricao VARCHAR(200),
        criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (id_usuario) REFERENCES SistemaUsuario(id),
        FOREIGN KEY (id_laboratorio) REFERENCES Laboratorio(id),
        UNIQUE(id_laboratorio, data_reserva, periodo)
    );
""")

# Campo de codigo de barras para o SistemaUsuario (criacao/upgrade seguro)
try:
    cursor.execute("ALTER TABLE SistemaUsuario ADD COLUMN codigo_barras VARCHAR(50)")
    conexao.commit()
except Exception:
    pass  # coluna ja existe (banco ja criado)

# Ids dos periodos (patrao IFSC): 55 min cada
PERIODOS = {
    1: "08:00 - 08:55",
    2: "09:00 - 09:50",
    3: "10:10 - 11:05",
    4: "11:10 - 12:00",
    5: "13:30 - 14:25",
    6: "14:30 - 15:20",
    7: "15:40 - 16:35",
    8: "19:00 - 19:55",
}

def MostarUsuarios():
    cursor.execute("""SELECT * FROM Usuario""")
    usuarios = cursor.fetchall()
    return usuarios  

def MostrarDigitais():
    cursor.execute("""SELECT * FROM Digital""")
    digitals = cursor.fetchall()
    return digitals 


def CadastrarUsuario(nome, cargo, email, codigo_digital):
    cursor.execute("""INSERT INTO Usuario (nome, cargo, email) VALUES(?,?,?)""", (nome, cargo, email))
    id_usuario = cursor.lastrowid
    cursor.execute("""INSERT INTO Digital (codigo) VALUES(?)""", (codigo_digital,))
    id_digital = cursor.lastrowid
    cursor.execute("""INSERT INTO UsuarioDigital VALUES(?,?)""", (id_usuario, id_digital))
    conexao.commit() 

def ExcluirUsuario(id_usuario):
    cursor.execute("""SELECT id_digital FROM UsuarioDigital WHERE id_usuario = ?""", (id_usuario,))
    resultado = cursor.fetchone()
    
    if resultado:
        id_digital = resultado[0]
        
        cursor.execute("""DELETE FROM UsuarioDigital WHERE id_usuario = ?""", (id_usuario,))
        cursor.execute("""DELETE FROM Usuario WHERE id = ?""", (id_usuario,))
        cursor.execute("""DELETE FROM Digital WHERE id = ?""", (id_digital,))
        
        print(f"Usuário {id_usuario} e sua digital foram excluídos com sucesso!")
    else:
        print("Usuário não encontrado.")
    conexao.commit()

def EditarUsuarioAll():
    id_usuario = int(input("Digite o ID do usuário que deseja editar: "))
    
    cursor.execute("""SELECT * FROM Usuario WHERE id = ?""", (id_usuario,))
    usuario = cursor.fetchone()
    
    if usuario:
        nome_atual, cargo_atual, email_atual = usuario[1], usuario[2], usuario[3]
        
        novo_nome = input(f"Digite o novo nome (atual: {nome_atual}): ") or nome_atual
        novo_cargo = input(f"Digite o novo cargo (atual: {cargo_atual}): ") or cargo_atual
        novo_email = input(f"Digite o novo email (atual: {email_atual}): ") or email_atual
        
        cursor.execute("""UPDATE Usuario SET nome = ?, cargo = ?, email = ? WHERE id = ?""",
                       (novo_nome, novo_cargo, novo_email, id_usuario))
        
        print("Usuário atualizado com sucesso!")
    else:
        print("Usuário não encontrado.")

    conexao.commit()

def Digital_existe(codigo_busca):
    # Reaproveita a mesma conexão global, em vez de abrir uma nova a cada chamada
    cursor.execute("SELECT 1 FROM Digital WHERE codigo = ?", (codigo_busca,))
    resultado = cursor.fetchone()
    return resultado is not None


def BuscarUsuarioComDigital(id_usuario):
    """
    Retorna (id, nome, cargo, email, codigo_digital) de um usuário específico,
    juntando as tabelas Usuario, UsuarioDigital e Digital.
    """
    cursor.execute("""
        SELECT Usuario.id, Usuario.nome, Usuario.cargo, Usuario.email, Digital.codigo
        FROM Usuario
        JOIN UsuarioDigital ON Usuario.id = UsuarioDigital.id_usuario
        JOIN Digital ON Digital.id = UsuarioDigital.id_digital
        WHERE Usuario.id = ?
    """, (id_usuario,))
    return cursor.fetchone()


def EditarUsuario(id_usuario, nome, cargo, email, codigo_digital):
    """
    Atualiza nome, cargo, email do usuário e o código da digital associada a ele.
    """
    cursor.execute(
        "UPDATE Usuario SET nome = ?, cargo = ?, email = ? WHERE id = ?",
        (nome, cargo, email, id_usuario)
    )

    cursor.execute("""
        SELECT id_digital FROM UsuarioDigital WHERE id_usuario = ?
    """, (id_usuario,))
    resultado = cursor.fetchone()

    if resultado:
        id_digital = resultado[0]
        cursor.execute(
            "UPDATE Digital SET codigo = ? WHERE id = ?",
            (codigo_digital, id_digital)
        )

    conexao.commit()
