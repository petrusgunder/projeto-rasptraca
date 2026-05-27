import sqlite3

def conectar():
    return sqlite3.connect("banco.db")

def criar_tabela():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Usuario(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            nome VARCHAR(50) NOT NULL,
            cargo VARCHAR(10) NOT NULL,
            email VARCHAR(50) NOT NULL
        )
                   
        CREATE TABLE IF NOT EXISTS Digital(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            codigo VARCHAR(50) NOT NULL
        )
                   
    """)
    conexao.commit()
    conexao.close()

def mostrar_usuarios():
    """Busca e retorna todos os usuários do banco."""
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM Usuario")
    usuarios = cursor.fetchall()
    conexao.close()
    return usuarios 

def buscar_usuario_por_id(id_usuario):
    """Busca um único usuário pelo ID (útil para validações)."""
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM Usuario WHERE id = ?", (id_usuario,))
    usuario = cursor.fetchone()
    conexao.close()
    return usuario

def adicionar_usuario(nome, cargo, email):
    """Insere um novo usuário no banco."""
    conexao = conectar()
    cursor = conexao.cursor()
    sql = "INSERT INTO Usuario (nome, cargo, email) VALUES (?, ?, ?)"
    cursor.execute(sql, (nome, cargo, email))
    conexao.commit()
    conexao.close()

def editar_usuario(id_usuario, novo_nome, novo_cargo, novo_email):
    """Atualiza os dados de um usuário existente."""
    conexao = conectar()
    cursor = conexao.cursor()
    sql = "UPDATE Usuario SET nome = ?, cargo = ?, email = ? WHERE id = ?"
    cursor.execute(sql, (novo_nome, novo_cargo, novo_email, id_usuario))
    conexao.commit()
    conexao.close()

def excluir_usuario(id_usuario):
    """Remove um usuário do banco pelo ID."""
    conexao = conectar()
    cursor = conexao.cursor()
    sql = "DELETE FROM Usuario WHERE id = ?"
    cursor.execute(sql, (id_usuario,))
    conexao.commit()
    conexao.close()

#-------------------------------------------------------------------------------------------

def mostrar_Digital():
    """Busca e retorna todos os usuários do banco."""
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM Digital")
    usuarios = cursor.fetchall()
    conexao.close()
    return usuarios 

def buscar_usuario_por_id(id_usuario):
    """Busca um único usuário pelo ID (útil para validações)."""
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM Usuario WHERE id = ?", (id_usuario,))
    usuario = cursor.fetchone()
    conexao.close()
    return usuario

def adicionar_usuario(nome, cargo, email):
    """Insere um novo usuário no banco."""
    conexao = conectar()
    cursor = conexao.cursor()
    sql = "INSERT INTO Usuario (nome, cargo, email) VALUES (?, ?, ?)"
    cursor.execute(sql, (nome, cargo, email))
    conexao.commit()
    conexao.close()

def editar_usuario(id_usuario, novo_nome, novo_cargo, novo_email):
    """Atualiza os dados de um usuário existente."""
    conexao = conectar()
    cursor = conexao.cursor()
    sql = "UPDATE Usuario SET nome = ?, cargo = ?, email = ? WHERE id = ?"
    cursor.execute(sql, (novo_nome, novo_cargo, novo_email, id_usuario))
    conexao.commit()
    conexao.close()

def excluir_usuario(id_usuario):
    """Remove um usuário do banco pelo ID."""
    conexao = conectar()
    cursor = conexao.cursor()
    sql = "DELETE FROM Usuario WHERE id = ?"
    cursor.execute(sql, (id_usuario,))
    conexao.commit()
    conexao.close()