from banco import Usuario
from funcoes import VerificarPlaca

c = Usuario()

ids = c.retornarId()

dado = input("simulação de leitura de dados: ")

VerificarPlaca(dado,ids)

c.fechar_conexao 