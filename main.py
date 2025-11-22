# importar módulos do próprio projeto
import modulo
import textos

# arquivos JSON
USUARIOS = 'usuarios.json'
DENUNCIAS = 'denuncias.json'

# inicializa banco de dados
database_lista = modulo.inicializar_usuarios(USUARIOS)
denuncias_lista = modulo.inicializar_denuncias(DENUNCIAS)

# estado de login
login_sucesso = False
usuario_encontrado = None
usuario_tipo = None  # 'user' ou 'admin'

while True:
    textos.menu_inicial()
    escolha = input(textos.escolha())
    print()

    # ===== LOGIN =====
    if escolha == '1':
        textos.perguntar_conta()
        escolha_auth = input(textos.escolha())
        print()

        # criar nova conta
        if escolha_auth == '2':
            usuario_digitado, senha_digitada, senha_confirma, caminho_comprovante = modulo.perguntas_nova_conta()
            novo_usuario = modulo.verificar_nova_conta(usuario_digitado, database_lista,
                                                       senha_digitada, senha_confirma, caminho_comprovante)
            if novo_usuario:
                modulo.adicionar_usuario(database_lista, novo_usuario, USUARIOS)
                database_lista = modulo.inicializar_usuarios(USUARIOS)
                print("\n[SUCESSO] Cadastro concluído!")
            else:
                print("\n[AVISO] Cadastro não concluído por erro de validação.")
            continue

        # login
        elif escolha_auth == '1':
            usuario_digitado = input("Usuário: ")
            senha_digitada = input("Senha: ")

            # primeiro verifica se é admin
            usuario_encontrado, usuario_tipo = modulo.login_usuario(usuario_digitado, senha_digitada, database_lista)
            if usuario_encontrado:
                login_sucesso = True
                if usuario_tipo == 'admin':
                    print("[ADMIN] Login bem-sucedido!")
                else:
                    status = usuario_encontrado.get("status_verificacao", "pendente")
                    if status == "aprovado":
                        print(f"\n[SUCESSO] Login efetuado. Bem-vindo(a), {usuario_digitado}!")
                    else:
                        print("\n[AVISO] Conta pendente ou reprovada. Aguarde aprovação do admin.")
                        login_sucesso = False
            else:
                print("\n[ERRO] Usuário ou senha incorretos.")
            continue

    # ===== MENU DO USUÁRIO =====
    if login_sucesso and usuario_tipo == 'user':
        print("\n1 - Denunciar\n2 - Consultar status de denúncia\n3 - Logout")
        escolha_user = input("Escolha: ")
        if escolha_user == '1':
            empresa, local, titulo, descricao = modulo.perguntas_denuncia()
            nova_denuncia, protocolo = modulo.verificar_denuncia(empresa, local, titulo, descricao)
            if nova_denuncia:
                nova_denuncia['usuario'] = usuario_encontrado['usuario']
                modulo.adicionar_nova_denuncia(nova_denuncia, DENUNCIAS)
        elif escolha_user == '2':
            protocolo_digitado = input("Digite o número do protocolo: ")
            denuncia_encontrada = modulo.buscar_protocolo(denuncias_lista, protocolo_digitado)
            if denuncia_encontrada:
                textos.exibir_detalhes_denuncia(denuncia_encontrada)
            else:
                print("\n[ERRO] Protocolo não encontrado.")
        elif escolha_user == '3':
            login_sucesso = False
            usuario_tipo = None
        continue

    # ===== MENU DO ADMIN =====
    if login_sucesso and usuario_tipo == 'admin':
        print("\n1 - Listar usuários\n2 - Aprovar/Reprovar usuário\n3 - Listar denúncias\n4 - Alterar status denúncia\n5 - Logout")
        escolha_admin = input("Escolha: ")
        if escolha_admin == '1':
            modulo.listar_usuarios(database_lista)
        elif escolha_admin == '2':
            u = input("Usuário alvo: ")
            s = input("Novo status (aprovado/reprovado): ")
            modulo.aprovar_reprovar_usuario(database_lista, USUARIOS, u, s)
            database_lista = modulo.inicializar_usuarios(USUARIOS)
        elif escolha_admin == '3':
            modulo.listar_denuncias(denuncias_lista)
        elif escolha_admin == '4':
            p = input("Protocolo: ")
            s = input("Novo status: ")
            modulo.alterar_status_denuncia(denuncias_lista, DENUNCIAS, p, s)
            denuncias_lista = modulo.inicializar_denuncias(DENUNCIAS)
        elif escolha_admin == '5':
            login_sucesso = False
            usuario_tipo = None
        continue

    # ===== MENU INICIAL (não logado) =====
    if not login_sucesso:
        print("1 - Login, 2 - Sair")
        if input("Escolha: ") == '2':
            break
