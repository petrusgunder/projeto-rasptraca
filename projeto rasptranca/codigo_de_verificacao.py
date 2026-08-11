from banco_de_dados import Digital_existe


def VerificarDigital(codigo_digital):
    """
    Recebe o código de uma digital e retorna True se ela existir
    no banco de dados, ou False caso contrário.
    Equivalente à lógica de 'CodigoDeVerificação', mas sem input()/print(),
    já que aqui quem chama é uma rota Flask (routes.py).
    """
    if not codigo_digital:
        return False
    return Digital_existe(codigo_digital)
