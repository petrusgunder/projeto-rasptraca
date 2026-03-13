from banco import Usuario

c = Usuario()
c.mostar_dados()

ids = c.retornarId()

dado = int(input("digite a digital: "))

for i in ids:
    if dado in ids:
        print("ta ficha")
        break
    else:
        print("ta midia")
        break


c.fechar_conexao