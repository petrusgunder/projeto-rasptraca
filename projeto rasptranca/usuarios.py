"""
CRUD dos usuarios do Sistema de Agenda.
Conta com cadastro, login (senha com hash), listagem e busca.
Utiliza a mesma conexao global definida em banco_de_dados.py.
"""
from werkzeug.security import generate_password_hash, check_password_hash
from banco_de_dados import conexao, cursor

# Credenciais do administrador padrao (criado automaticamente no primeiro uso)
ADMIN_EMAIL = "admin@admin.com"
ADMIN_SENHA = "admin127"


def CriarAdminPadrao():
    """Cria o usuario administrador padrao caso ainda nao exista."""
    cursor.execute("SELECT 1 FROM SistemaUsuario WHERE email = ?", (ADMIN_EMAIL,))
    if not cursor.fetchone():
        hash_senha = generate_password_hash(ADMIN_SENHA)
        cursor.execute(
            "INSERT INTO SistemaUsuario (nome, email, senha_hash, is_admin) VALUES (?,?,?,1)",
            ("Administrador", ADMIN_EMAIL, hash_senha),
        )
        conexao.commit()


def CadastrarUsuarioSistema(nome, email, senha, is_admin=0, codigo_barras=None):
    """Cadastra um novo usuario. Retorna (True, msg) ou (False, msg)."""
    if not nome or not email or not senha:
        return False, "Preencha nome, email e senha."
    if "@" not in email or "." not in email:
        return False, "Email invalido."

    # Verifica se o email ja esta em uso
    cursor.execute("SELECT 1 FROM SistemaUsuario WHERE email = ?", (email,))
    if cursor.fetchone():
        return False, "Ja existe um usuario com este email."

    hash_senha = generate_password_hash(senha)
    try:
        cursor.execute(
            "INSERT INTO SistemaUsuario (nome, email, senha_hash, is_admin, codigo_barras)"
            " VALUES (?,?,?,?,?)",
            (nome, email, hash_senha, is_admin, codigo_barras),
        )
        conexao.commit()
        return True, "Usuario cadastrado com sucesso!"
    except Exception as e:
        return False, f"Erro ao cadastrar: {e}"


def AutenticarUsuario(email, senha):
    """Retorna o usuario (tuple) se email+senha conferem, senao retorna None."""
    cursor.execute(
        "SELECT id, nome, email, senha_hash, is_admin FROM SistemaUsuario WHERE email = ?",
        (email,),
    )
    usuario = cursor.fetchone()
    if usuario and check_password_hash(usuario[3], senha):
        return usuario  # (id, nome, email, senha_hash, is_admin)
    return None


def BuscarUsuarioSistema(id_usuario):
    cursor.execute(
        "SELECT id, nome, email, is_admin, codigo_barras FROM SistemaUsuario WHERE id = ?",
        (id_usuario,),
    )
    return cursor.fetchone()


def ListarUsuariosSistema():
    cursor.execute(
        "SELECT id, nome, email, is_admin, codigo_barras FROM SistemaUsuario ORDER BY id"
    )
    return cursor.fetchall()


def EditarUsuarioSistema(id_usuario, nome, email, is_admin, codigo_barras=None):
    cursor.execute(
        "UPDATE SistemaUsuario SET nome = ?, email = ?, is_admin = ?, codigo_barras = ? WHERE id = ?",
        (nome, email, is_admin, codigo_barras, id_usuario),
    )
    conexao.commit()


def ExcluirUsuarioSistema(id_usuario):
    # Remove reservas do usuario antes de apagar (evita erro de FK)
    cursor.execute("DELETE FROM Reserva WHERE id_usuario = ?", (id_usuario,))
    cursor.execute("DELETE FROM SistemaUsuario WHERE id = ?", (id_usuario,))
    conexao.commit()


def AlterarSenha(id_usuario, nova_senha):
    hash_senha = generate_password_hash(nova_senha)
    cursor.execute(
        "UPDATE SistemaUsuario SET senha_hash = ? WHERE id = ?", (hash_senha, id_usuario)
    )
    conexao.commit()


def VerificarCodigoBarras(codigo):
    """Verifica se o codigo de barras pertence a algum usuario cadastrado.
    Retorna True se existir, False caso contrario. (Substitui a verificação por digital)"""
    if not codigo:
        return False
    cursor.execute(
        "SELECT 1 FROM SistemaUsuario WHERE codigo_barras = ?", (codigo.strip(),)
    )
    return cursor.fetchone() is not None
