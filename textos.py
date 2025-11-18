def menu_inicial():
    print('=-=-=-=-=-=-=-=- A VOZ OCULTA =-=-=-=-=-=-=-=-')
    print()
    print('1 - Login')
    print('2 - Denunciar')
    print('3 - Status de denúncias')
    print('4 - Outras denúncias')
    print()

def escolha():
    return 'Digite o número correspondente à sua escolha: '

def perguntar_conta():
    print('Você já tem uma conta?')
    print('1 - Sim')
    print('2 - Não')

def ja_esta_logado():
    print('Você já está logado, voltando ao menu...')

def denuncia():
        print("\n--- Registrar Nova Denúncia Anônima ---")
        print("Suas informações são confidenciais.")
        print("Por favor, preencha os dados da empresa e o motivo.")
        print()

def cabecalho_status():
    print("\n--- Consultar Status da Denúncia ---")

def exibir_detalhes_denuncia(denuncia):
    print("\n" + "="*30)
    print("   DADOS DA DENÚNCIA")
    print("="*30)
    print(f"Protocolo: {denuncia.get('protocolo')}")
    print(f"Empresa:   {denuncia.get('empresa_nome')}")
    print(f"Título:    {denuncia.get('titulo')}")
    print("-" * 30)
    
    status_atual = denuncia.get('status', 'N/A')
    print(f"STATUS ATUAL: {status_atual.upper()}")
    
    # Lógica para explicar o status ao usuário
    print("\nO que isso significa?")
    if status_atual == "Recebida":
        print("-> Sua denúncia foi registrada e está aguardando triagem.")
    elif status_atual == "Em análise":
        print("-> Nossa equipe de compliance está investigando os fatos.")
    elif status_atual == "Encaminhada":
        print("-> A denúncia foi validada e enviada para os órgãos/marcas responsáveis.")
    elif status_atual == "Encerrada":
        print("-> O processo foi concluído.")
    else:
        print("-> Status desconhecido.")
    print("="*30)