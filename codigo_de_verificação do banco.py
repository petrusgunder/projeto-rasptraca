from banco_de_dados import Digital_existe


c = 1

while(c != 0):
    print("1) validar digital\n2) sair")
    aux = input("digite o que quer fazer: ")

    if (aux == "2"):
        c=0
    else:
        if (aux == "1"):
            aux = input("digite o codigo da digital: ")
            sn = Digital_existe(aux)
            if (sn == True):
                print('ta')
                c=0
            else:
                print('nao ta')
                c=0
        else:
            print("dado invalido")