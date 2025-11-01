import json
import os

USUARIOS = 'usuarios.json'

if not os.path.exists(USUARIOS):
    try:
        with open(USUARIOS, 'w') as f:
            json.dump([], f)
            
    except Exception as e:
        print(f"[ERRO] Não foi possível criar o arquivo: {e}")


while True:
    print('=-=-=-=-=-=-=-=- A VOZ OCULTA =-=-=-=-=-=-=-=-')
    print()
    print('1 - Login')
    print('2 - Denunciar')
    print('3 - Status de denúncias')
    print('4 - Outras denúncias')
    print()

    escolha = input('Digite o número correspondente à sua escolha: ')
    print()

    if escolha == '1':
        print('Você já tem uma conta?')
        print('1 - Sim')
        print('2 - Não')

        escolha_auth = input('Digite o número correspondente à sua escolha: ')
        print()

        if escolha_auth == '1' and login_sucesso == True:
            print('Você já está logado, voltando ao menu...')

        elif escolha_auth == '1' and login_sucesso == False:
            print("\n--- Login ---")
            
            usuario_digitado = input("Usuário: ")
            senha_digitada = input("Senha: ") 
            
            usuario_encontrado = None
            login_sucesso = False
            
            try:
                with open(USUARIOS, 'r', encoding='utf-8') as f:
                    database_lista = json.load(f)

            except FileNotFoundError:
                database_lista = []
                print("[ERRO] Nenhum usuário cadastrado no sistema ainda.")
            
            for dados_usuario in database_lista:
                if dados_usuario.get('usuario') == usuario_digitado:
                    if dados_usuario.get('senha') == senha_digitada:
                        usuario_encontrado = dados_usuario
                        login_sucesso = True
            
            if login_sucesso:
                print('Você está logado.')
            
            else:
                print("\n[ERRO] Usuário ou senha incorretos.")

        elif escolha_auth == '2':
            print("\n--- Cadastro de Nova Conta ---")
            
            usuario_digitado = input("Digite um nome de usuário (fictício): ")
            senha_digitada = input("Digite uma senha: ")
            senha_confirmada = input("Confirme sua senha: ")
            caminho_comprovante = input("Cole o caminho completo do arquivo de comprovante: ")

            usuario_valido = False
            senha_valida = False
            comprovante_valido = False

            try:
                with open(USUARIOS, 'r', encoding='utf-8') as f:
                    database_lista = json.load(f)
            except FileNotFoundError:
                database_lista = []
            
            usuario_ja_existe = False
            if not usuario_digitado:
                print("[ERRO] O nome de usuário não pode ser vazio.")
            else:
                for dados_usuario in database_lista:
                    if dados_usuario.get('usuario') == usuario_digitado: 
                        usuario_ja_existe = True
                        break
                
                if usuario_ja_existe:
                    print(f"[ERRO] O nome de usuário '{usuario_digitado}' já está em uso.")
                else:
                    usuario_valido = True 

            if not senha_digitada:
                print("[ERRO] A senha não pode ser vazia.")
            elif senha_digitada != senha_confirmada:
                print("[ERRO] As senhas não conferem.")
            else:
                senha_valida = True 

            if not os.path.exists(caminho_comprovante):
                print(f"[ERRO] Arquivo não encontrado em: {caminho_comprovante}")
                print("Dica: Copie e cole o caminho completo do arquivo.")
            else:
                comprovante_valido = True 
            
            if usuario_valido and senha_valida and comprovante_valido:
                
                novo_usuario_dados = {
                    "usuario": usuario_digitado,
                    "senha": senha_digitada,
                    "comprovante_path": caminho_comprovante,
                    "status_verificacao": "pendente" 
                }
                
                try:
                    database_lista.append(novo_usuario_dados)
                    
                    with open(USUARIOS, 'w', encoding='utf-8') as f:
                        json.dump(database_lista, f, indent=4)
                    
                    print(f"\n[SUCESSO] Conta '{usuario_digitado}' criada!")

                except Exception as e:
                    print(f"\n[ERRO CRÍTICO] Não foi possível salvar sua conta: {e}")
            
            else:
                print("\n[AVISO] Cadastro não concluído. Tente novamente.")

    elif escolha == '2':
        pass