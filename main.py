# importar módulos do próprio projeto
import modulo
import textos

# cria variáveis essenciais para o funcionamento do código
USUARIOS = 'usuarios.json'
DENUNCIAS = 'denuncias.json'
login_sucesso = False 
usuario_encontrado = None 
database_lista = None

# inicializa o json de usuários e denúncias, caso não existam eles são criados
database_lista = modulo.inicializar_usuarios(USUARIOS)
denuncias_lista = modulo.inicializar_denuncias(DENUNCIAS)

# loop principal, onde todo o código vai rodar
while True:
    textos.menu_inicial() # printa o menu principal
    escolha = input(textos.escolha()) # input para o usuário escolher uma opção
    print()

    # usuário escolheu "1 - Login"
    if escolha == '1':
        textos.perguntar_conta() # pergunta se o usuário tem uma conta

        escolha_auth = input(textos.escolha()) # input para o usuário escolher uma opção
        print()

        # caso escolha que já tem uma conta e esteja logado
        if escolha_auth == '1' and login_sucesso == True:
            textos.ja_esta_logado() # avisa que usuário já está logado
            # volta para o começo do loop, menu principal

        # caso escolha que já tem uma conta e não esteja logado
        elif escolha_auth == '1' and login_sucesso == False:
            # login, pede para digitar usuário e senha para entrar na conta
            print("\n--- Login ---")
            usuario_digitado = input("Usuário: ")
            senha_digitada = input("Senha: ") 
            
            # procura na db se os dados conferem, e coloca true ou false no sucesso do login
            usuario_encontrado, login_sucesso = modulo.procurar_login(database_lista, usuario_digitado, senha_digitada)
            
            # caso o login seja bem sucedido
            if login_sucesso:
                status = usuario_encontrado.get('status_verificacao', 'pendente')

                # esse bloco verifica se o usuário teve o comprovante de vínculo aprovado
                # aprovado
                if status == 'aprovado':
                    print(f"\n[SUCESSO] Login efetuado. Bem-vindo(a), {usuario_digitado}!")
                    # loga na conta

                # pendente
                elif status == 'pendente':
                    print("\n[AVISO] Esta conta ainda está 'pendente' de análise.")
                    print("Você poderá logar assim que ela for aprovada.")
                    login_sucesso = False # não entra na conta

                # repovado
                else:
                    print("\n[ERRO] O cadastro desta conta foi 'reprovado' pela moderação.")
                    login_sucesso = False # não entra na conta

            # caso o login não tenha sucesso
            else:
                print("\n[ERRO] Usuário ou senha incorretos.")

        # caso escolha que não tem conta, criar nova
        elif escolha_auth == '2':
            # perguntas para criar nova conta, respostas salvas em variáveis
            usuario_digitado, senha_digitada, senha_confirmada, caminho_comprovante = modulo.perguntas_nova_conta() 

            # criação de variáveis essenciais
            usuario_valido = False
            senha_valida = False
            comprovante_valido = False

            # inicializar db de usuários, caso ainda não tenha sido
            modulo.inicializar_usuarios(USUARIOS)
            
            # variável para criação de usuário
            usuario_ja_existe = False
            
            # variáveis pro código não quebrar
            usuario_ja_existe = False
            usuario_valido = False
            senha_valida = False
            comprovante_valido = False

            # juntar todos os dados do usuário, caso válidos
            novo_usuario_dados = modulo.verificar_nova_conta(usuario_digitado, database_lista, senha_digitada, senha_confirmada, caminho_comprovante)

            # verifica se os dados existem
            if novo_usuario_dados:
                # se sim, adiciona à database
                modulo.adicionar_usuario(database_lista, novo_usuario_dados, usuario_digitado)
                # e adiciona na memória do programa
                database_lista = modulo.inicializar_usuarios(USUARIOS)

            else:
                # se não, avisa que deu erro
                print("\n[AVISO] Cadastro não concluído por erro de validação.")
        
        # caso o cadastro não dê certo
        else:
            print("\n[AVISO] Cadastro não concluído. Tente novamente.")

    # usuário escolheu "2 - Denunciar"
    elif escolha == '2':
        textos.denuncia() # printa o texto sobre denunciar
        
        # faz o questionário de denúncia e salva as respostas em variáveis
        empresa_nome, empresa_local, titulo_denuncia, descricao_denuncia = modulo.perguntas_denuncia()

        # verifica se a denúncia é válida e se for salva em uma variável e também o protocolo
        nova_denuncia_dados, protocolo = modulo.verificar_denuncia(empresa_nome, empresa_local, titulo_denuncia, descricao_denuncia)
        if nova_denuncia_dados:
            # salva a denúncia na database caso válido
            modulo.adicionar_nova_denuncia(nova_denuncia_dados, protocolo)
        else:
            print("\n[AVISO] Cadastro não concluído por erro de validação.")

    # em construção...
    else:
        print('3 e 4 em construção...')