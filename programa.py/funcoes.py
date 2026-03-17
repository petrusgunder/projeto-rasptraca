def VerificarPlaca (placa_a_ser_avaliada, placas_do_banco):
    for i in placas_do_banco:
        if placa_a_ser_avaliada in placas_do_banco:
            print("placa consta no banco de dados")
            break
        else:
            print("placa nao conta no bnaco de dados ")
            break

def Verificar_Quantidade_de_caracteres(entrada):
    if len(entrada) != 7:
        return False
    else:
        return True