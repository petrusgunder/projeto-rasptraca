from banco_de_dados import (
    MostarUsuarios, 
    MostrarDigitais, 
    CadastrarUsuario, 
    ExcluirUsuario, 
    EditarUsuarioAll, 
    conexao
)

def exibir_menu():
    while True:
        print("\n" + "="*30)
        print("       SISTEMA DE BIOMETRIA      ")
        print("="*30)
        print("1. Listar Usuários")
        print("2. Listar Digitais")
        print("3. Cadastrar Novo Usuário + Digital")
        print("4. Editar Usuário")
        print("5. Excluir Usuário e Digital")
        print("0. Sair")
        print("="*30)
        
        opcao = input("Escolha uma opção: ")
        print("-" * 30)
        
        if opcao == "1":
            MostarUsuarios()
            
        elif opcao == "2":
            MostrarDigitais()
            
        elif opcao == "3":
            print("--- CADASTRO DE USUÁRIO ---")
            nome = input("Nome: ")
            cargo = input("Cargo: ")
            email = input("Email: ")
            digital = input("Código da Digital: ")
            
            if nome and cargo and email and digital:
                CadastrarUsuario(nome, cargo, email, digital)
            else:
                print("Erro: Todos os campos são obrigatórios!")
                
        elif opcao == "4":
            EditarUsuarioAll()
            
        elif opcao == "5":
            print("--- EXCLUSÃO DE USUÁRIO ---")
            try:
                id_user = int(input("Digite o ID do usuário que deseja remover: "))
                ExcluirUsuario(id_user)
            except ValueError:
                print("Erro: Por favor, insira um número de ID válido.")
                
        elif opcao == "0":
            print("Encerrando o sistema... Até mais!")
            break
            
        else:
            print("Opção inválida! Tente novamente.")
        
        input("\nPressione Enter para voltar ao menu...")

if __name__ == "__main__":
    exibir_menu()
    conexao.close()