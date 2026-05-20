import banco 

while True:
    print("====== PAINEL DO ADMINISTRADOR ======")
    print("[1] Visualizar Usuários")
    print("[2] Adicionar Usuário")
    print("[3] Editar Usuário")
    print("[4] Excluir Usuário")
    print("[0] Sair do Sistema")
    print("=====================================")
    
    opcao = input("Escolha uma opção: ")
    
    if opcao == "1":
        usuarios = banco.mostrar_usuarios()
        print("\n=== LISTA DE USUÁRIOS ===")
        if not usuarios:
            print("Nenhum usuário cadastrado.")
        else:
            for id, nome, cargo, email in usuarios:
                print(f"ID: {id} | Nome: {nome} | Cargo: {cargo} | Email: {email}")
        print("=========================\n")
        
    elif opcao == "2":
        print("\n--- ADICIONAR NOVO USUÁRIO ---")
        nome = input("Digite o nome: ")
        cargo = input("Digite o cargo: ")
        email = input("Digite o e-mail: ")
        
        banco.adicionar_usuario(nome, cargo, email)
        print(f"Usuário '{nome}' adicionado com sucesso!\n")
        
    elif opcao == "3":
        print("\n--- EDITAR USUÁRIO ---")
        id_usuario = input("Digite o ID do usuário que deseja editar: ")
        
        if not banco.buscar_usuario_por_id(id_usuario):
            print("Erro: Usuário não encontrado!\n")
            continue

        novo_nome = input("Digite o NOVO nome: ")
        novo_cargo = input("Digite o NOVO cargo: ")
        novo_email = input("Digite o NOVO e-mail: ")
        
        banco.editar_usuario(id_usuario, novo_nome, novo_cargo, novo_email)
        print(f"Usuário ID {id_usuario} atualizado com sucesso!\n")
        
    elif opcao == "4":
        print("\n--- EXCLUIR USUÁRIO ---")
        id_usuario = input("Digite o ID do usuário que deseja excluir: ")
        
        if not banco.buscar_usuario_por_id(id_usuario):
            print("Erro: Usuário não encontrado!\n")
            continue
            
        confirmacao = input(f"Tem certeza que deseja excluir o ID {id_usuario}? (S/N): ").upper()
        
        if confirmacao == 'S':
            banco.excluir_usuario(id_usuario)
            print(f"Usuário ID {id_usuario} excluído com sucesso!\n")
        else:
            print("Operação cancelada.\n")
            
    elif opcao == "0":
        print("\nSaindo do sistema... Até logo!")
        break
    else:
        print("\nOpção inválida! Tente novamente.\n")