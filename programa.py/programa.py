from banco import Usuario
from funcoes import VerificarPlaca
from funcoes import Verificar_Quantidade_de_caracteres

c = Usuario()

ids = c.retornarPlaca()

dado = input("simulação de leitura de dados: ")

if Verificar_Quantidade_de_caracteres(dado) == True:
    VerificarPlaca(dado,ids)
else:
    print("placa nao segue os parametros de placa")


c.fechar_conexao 