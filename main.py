import json
import os
import random

USUARIOS = 'usuarios.json'
DENUNCIAS = 'denuncias.json'
login_sucesso = False 
usuario_encontrado = None 

if not os.path.exists(USUARIOS):
    try:
        with open(USUARIOS, 'w') as f:
            json.dump([], f)
            
    except Exception as e:
        print(f"[ERRO] Não foi possível criar o arquivo {USUARIOS}: {e}")


if not os.path.exists(DENUNCIAS):
    try:
        with open(DENUNCIAS, 'w') as f:
            json.dump([], f)
            
    except Exception as e:
        print(f"[ERRO] Não foi possível criar o arquivo {DENUNCIAS}: {e}")


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
                status = usuario_encontrado.get('status_verificacao', 'pendente')

                if status == 'aprovado':
                    print(f"\n[SUCESSO] Login efetuado. Bem-vindo(a), {usuario_digitado}!")

                elif status == 'pendente':
                    print("\n[AVISO] Esta conta ainda está 'pendente' de análise.")
                    print("Você poderá logar assim que ela for aprovada.")
                    login_sucesso = False 

                else:
                    print("\n[ERRO] O cadastro desta conta foi 'reprovado' pela moderação.")
                    login_sucesso = False

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
        print("\n--- Registrar Nova Denúncia Anônima ---")
        print("Suas informações são confidenciais.")
        print("Por favor, preencha os dados da empresa e o motivo.")
        print()
        
        empresa_nome = input("Qual o nome da empresa a ser denunciada? ")
        empresa_local = input("Qual a localização da empresa (Cidade/Estado)? ")
        titulo_denuncia = input("Qual o título/tipo de abuso (ex: Assédio, Horas extras não pagas)? ")
        
        print("\nDescreva detalhadamente o que aconteceu:")
        print("(Para terminar, pressione ENTER em uma linha vazia)")
        
        descricao_linhas = []
        while True:
            linha = input()
            if linha == "":
                break
            descricao_linhas.append(linha)
        
        descricao_denuncia = "\n".join(descricao_linhas)

        if not empresa_nome or not titulo_denuncia or not descricao_denuncia:
            print("\n[ERRO] Nome da empresa, Título e Descrição são obrigatórios.")
            print("Denúncia não registrada. Tente novamente.")
        else:
            protocolo = str(random.randint(100000, 999999))

            nova_denuncia_dados = {
                "protocolo": protocolo,
                "empresa_nome": empresa_nome,
                "empresa_local": empresa_local,
                "titulo": titulo_denuncia,
                "descricao": descricao_denuncia,
                "status": "Recebida"
            }

            try:
                with open(DENUNCIAS, 'r', encoding='utf-8') as f:
                    lista_denuncias = json.load(f)
                
                lista_denuncias.append(nova_denuncia_dados)

                with open(DENUNCIAS, 'w', encoding='utf-8') as f:
                    json.dump(lista_denuncias, f, indent=4)
                
                print("\n" + "="*40)
                print("[SUCESSO] Denúncia registrada.")
                print(f"  SEU NÚMERO DE PROTOCOLO É: {protocolo}")
                print("\n  ATENÇÃO: GUARDE ESTE NÚMERO!")
                print("  Você usará ele para checar o 'Status da Denúncia'.")
                print("="*40)

            except Exception as e:
                print(f"\n[ERRO CRÍTICO] Não foi possível salvar sua denúncia: {e}")

    else:
        continue