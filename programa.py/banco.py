import sqlite3

conn = sqlite3.connect('banco.db')

cursor = conn.cursor()

cursor.executescript('''
-- Apaga na ordem inversa das dependências
    DROP TABLE IF EXISTS Usuario_digital;
    DROP TABLE IF EXISTS Placa;
    DROP TABLE IF EXISTS Usuario;

    CREATE TABLE Usuario(
        id CHAR(9) PRIMARY KEY,
        nome VARCHAR(50),
        cargo VARCHAR(10) CHECK (cargo IN ('professor', 'aluno')),
        email VARCHAR(50) 
    );

    CREATE TABLE Placa (
        id INT PRIMARY KEY,
        codigo INT
    );

    CREATE TABLE Usuario_Placa (
        id_usuario INT NOT NULL,
        id_placa INT NOT NULL,
        CONSTRAINT pk_usuario_placa PRIMARY KEY (id_usuario, id_placa)
    );

    INSERT INTO Usuario VALUES ('a1a1-a1a1', 'João Silva', 'professor', 'joao.silva@email.com');
    INSERT INTO Usuario VALUES ('a2a2-a2a2', 'Maria Oliveira', 'aluno', 'maria.oliveira@email.com');
    
    INSERT INTO Placa VALUES (1, 12345);
    INSERT INTO Placa VALUES (2, 67890);

    INSERT INTO Usuario_Placa VALUES (1, 1);
    INSERT INTO Usuario_Placa VALUES (2, 2);

''')

conn.commit()

class Usuario:
    def mostar_dados(self):

        cursor.execute('SELECT * FROM Usuario')

        usuarios = cursor.fetchall()

        for usuario in usuarios:
            print(f"ID: {usuario[0]} | Nome: {usuario[1]} | Cargo: {usuario[2]}")

        

    def retornarId(self):
        cursor.execute('SELECT id FROM Usuario')
        ids = cursor.fetchall()
        
        lista_ids = []
        for row in ids:
            lista_ids.append(row[0])
        
        return lista_ids

    def fechar_conexao(self):
        conn.close()