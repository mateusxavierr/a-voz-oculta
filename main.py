import modulo
import textos

# Configuração de Arquivos
USUARIOS = 'usuarios.json'
DENUNCIAS = 'denuncias.json'

# Carga Inicial de Dados (Criptografados)
database_lista = modulo.inicializar_usuarios(USUARIOS)
denuncias_lista = modulo.inicializar_denuncias(DENUNCIAS)

# Variáveis de Estado
login_sucesso = False
usuario_encontrado = None
usuario_tipo = None 

while True:
    
    # ==========================================
    # 1. MENU PÚBLICO (NÃO LOGADO)
    # ==========================================
    if not login_sucesso:
        textos.menu_inicial()
        escolha = input(textos.escolha())
        print()

        # --- LOGIN / CADASTRO ---
        if escolha == '1':
            textos.perguntar_conta()
            auth = input(textos.escolha())
            print()

            # 1.1 Fazer Login
            if auth == '1':
                user = input("Usuário: ")
                senha = input("Senha: ")
                usuario_encontrado, usuario_tipo = modulo.login_usuario(user, senha, database_lista)
                
                if usuario_encontrado:
                    if usuario_tipo == 'admin':
                        print("\n[ADMIN] Painel acessado.")
                        login_sucesso = True
                    else:
                        status = usuario_encontrado.get("status_verificacao", "pendente")
                        if status == "aprovado":
                            print(f"\n[SUCESSO] Bem-vindo(a), {user}!")
                            login_sucesso = True
                        else:
                            print(f"\n[AVISO] Conta {status}. Contate o suporte.")
                else:
                    print("\n[ERRO] Credenciais inválidas.")

            # 1.2 Criar Conta
            elif auth == '2':
                u, s, sc, comp = modulo.perguntas_nova_conta()
                novo = modulo.verificar_nova_conta(u, database_lista, s, sc, comp)
                if novo:
                    modulo.adicionar_usuario(database_lista, novo, USUARIOS)
                    database_lista = modulo.inicializar_usuarios(USUARIOS) # Recarrega
                else:
                    print("\n[FALHA] Erro na validação.")

        # --- DENÚNCIA ANÔNIMA ---
        elif escolha == '2':
            emp, loc, tit, desc, pub = modulo.perguntas_denuncia()
            nova, prot = modulo.verificar_denuncia(emp, loc, tit, desc, pub, denuncias_lista)
            if nova:
                modulo.adicionar_nova_denuncia(nova, DENUNCIAS)
                denuncias_lista = modulo.inicializar_denuncias(DENUNCIAS)

        # --- CONSULTAR STATUS ---
        elif escolha == '3':
            textos.cabecalho_status()
            prot = input("Protocolo: ")
            d = modulo.buscar_protocolo(denuncias_lista, prot)
            if d: textos.exibir_detalhes_denuncia(d)
            else: print("\n[ERRO] Não encontrado.")

        # --- FEED REDE SOCIAL ---
        elif escolha == '4':
            feed = modulo.obter_feed_social(denuncias_lista)
            textos.exibir_feed_social(feed)
            input("\nENTER para voltar...")

        # --- SAIR ---
        elif escolha == '0':
             print("Saindo...")
             break
        else:
             print("Opção inválida.")

    # ==========================================
    # 2. MENU ADMIN
    # ==========================================
    elif login_sucesso and usuario_tipo == 'admin':
        print("\n--- PAINEL ADMIN ---")
        print("1-Listar Users | 2-Aprovar/Reprovar | 3-Listar Denúncias | 4-Alterar Status | 0-Logout")
        adm = input("Escolha: ")

        if adm == '1':
            modulo.listar_usuarios(database_lista)
        elif adm == '2':
            alvo = input("User: ")
            st = input("Status (aprovado/reprovado): ")
            modulo.aprovar_reprovar_usuario(database_lista, USUARIOS, alvo, st, denuncias_lista, DENUNCIAS)
            # Recarrega DBs para garantir sincronia
            database_lista = modulo.inicializar_usuarios(USUARIOS)
            denuncias_lista = modulo.inicializar_denuncias(DENUNCIAS)
        elif adm == '3':
            modulo.listar_denuncias(denuncias_lista)
        elif adm == '4':
            prot = input("Protocolo: ")
            st = input("Novo Status: ")
            modulo.alterar_status_denuncia(denuncias_lista, DENUNCIAS, prot, st)
            denuncias_lista = modulo.inicializar_denuncias(DENUNCIAS)
        elif adm == '0':
            login_sucesso = False
            usuario_tipo = None

    # ==========================================
    # 3. MENU USUÁRIO COMUM
    # ==========================================
    elif login_sucesso and usuario_tipo == 'user':
        print(f"\n--- Menu: {usuario_encontrado['usuario']} ---")
        print("1-Denunciar (Vinculada) | 2-Consultar Status | 0-Logout")
        usr = input("Escolha: ")

        if usr == '1':
            emp, loc, tit, desc, pub = modulo.perguntas_denuncia()
            nova, prot = modulo.verificar_denuncia(emp, loc, tit, desc, pub, denuncias_lista)
            if nova:
                nova['usuario'] = usuario_encontrado['usuario']
                modulo.adicionar_nova_denuncia(nova, DENUNCIAS)
                denuncias_lista = modulo.inicializar_denuncias(DENUNCIAS)
        elif usr == '2':
            prot = input("Protocolo: ")
            d = modulo.buscar_protocolo(denuncias_lista, prot)
            if d: textos.exibir_detalhes_denuncia(d)
            else: print("\n[ERRO] Não encontrado.")
        elif usr == '0':
            login_sucesso = False
            usuario_tipo = None
