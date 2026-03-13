import sqlite3

conn = sqlite3.connect('banco.db')

cursor = conn.cursor()

cursor.executescript('''
-- Apaga na ordem inversa das dependências
    DROP TABLE IF EXISTS Usuario_digital;
    DROP TABLE IF EXISTS Digital;
    DROP TABLE IF EXISTS Usuario;

    CREATE TABLE Usuario(
        id INT PRIMARY KEY,
        nome VARCHAR(50),
        cargo VARCHAR(10) CHECK (cargo IN ('professor', 'aluno')),
        email VARCHAR(50) 
    );

    CREATE TABLE Digital (
        id INT PRIMARY KEY,
        codigo INT
    );

    CREATE TABLE Usuario_digital (
        id_usuario INT NOT NULL,
        id_digital INT NOT NULL,
        CONSTRAINT pk_usuario_digital PRIMARY KEY (id_usuario, id_digital)
    );

    INSERT INTO Usuario VALUES (1, 'João Silva', 'professor', 'joao.silva@email.com');
    INSERT INTO Usuario VALUES (2, 'Maria Oliveira', 'aluno', 'maria.oliveira@email.com');
    
    INSERT INTO Digital VALUES (1, 12345);
    INSERT INTO Digital VALUES (2, 67890);

    INSERT INTO Usuario_digital VALUES (1, 1);
    INSERT INTO Usuario_digital VALUES (2, 2);

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