from functools import wraps
from flask import session, redirect, url_for

# Troque essa senha pela que você quiser usar no projeto
SENHA_ACESSO = "1234"

def login_required(funcao):
    @wraps(funcao)
    def decorada(*args, **kwargs):
        if not session.get("logado"):
            return redirect(url_for("login"))
        return funcao(*args, **kwargs)
    return decorada


def login_usuario_required(funcao):
    """Exige que o usuario esteja logado no Sistema de Agenda."""
    @wraps(funcao)
    def decorada(*args, **kwargs):
        if not session.get("usuario_id"):
            return redirect(url_for("login"))
        return funcao(*args, **kwargs)
    return decorada


def admin_required(funcao):
    """Exige que o usuario logado seja administrador."""
    @wraps(funcao)
    def decorada(*args, **kwargs):
        if not session.get("usuario_id"):
            return redirect(url_for("login"))
        if not session.get("usuario_admin"):
            return redirect(url_for("home"))
        return funcao(*args, **kwargs)
    return decorada
