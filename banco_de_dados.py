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
""")

def MostarUsuarios():
    cursor.execute("""SELECT * FROM Usuario""")
    usuarios = cursor.fetchall()
    return usuarios  # Alterado de print para return

def MostrarDigitais():
    cursor.execute("""SELECT * FROM Digital""")
    digitals = cursor.fetchall()
    return digitals  # Alterado de print para return


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