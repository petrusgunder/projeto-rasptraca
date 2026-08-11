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
