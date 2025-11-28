# --- MENUS E CABEÇALHOS ---

def menu_inicial():
    print('=-=-=-=-=-=-=-=- A VOZ OCULTA =-=-=-=-=-=-=-=-')
    print()
    print('1 - Login')
    print('2 - Denunciar')
    print('3 - Status de denúncias')
    print('4 - Feed "Outras Denúncias" (Rede Social) 📢')
    print('0 - Sair')
    print()

def cabecalho_status():
    print("\n--- Consultar Status da Denúncia ---")

def denuncia():
    print("\n--- Registrar Nova Denúncia Anônima ---")
    print("Suas informações são confidenciais.")
    print("Por favor, preencha os dados da empresa e o motivo.")
    print()

# --- INPUTS E INTERAÇÕES ---

def escolha():
    return 'Digite o número correspondente à sua escolha: '

def perguntar_conta():
    print('Você já tem uma conta?')
    print('1 - Sim')
    print('2 - Não')

def ja_esta_logado():
    print('Você já está logado, voltando ao menu...')

# --- EXIBIÇÃO DE DADOS ---

def exibir_detalhes_denuncia(denuncia):
    """Formata e exibe uma denúncia individual."""
    print("\n" + "="*30)
    print("   DADOS DA DENÚNCIA")
    print("="*30)
    print(f"Protocolo: {denuncia.get('protocolo')}")
    print(f"Empresa:   {denuncia.get('empresa_nome')}")
    print(f"Título:    {denuncia.get('titulo')}")
    print("-" * 30)
    
    status_atual = denuncia.get('status', 'N/A')
    print(f"STATUS ATUAL: {status_atual.upper()}")
    
    print("\nO que isso significa?")
    if status_atual == "Recebida":
        print("-> Sua denúncia foi registrada e está aguardando triagem.")
    elif status_atual == "Em análise":
        print("-> Nossa equipe de compliance está investigando os fatos.")
    elif status_atual == "Encaminhada":
        print("-> A denúncia foi validada e enviada para os órgãos competentes.")
    elif status_atual == "Encerrada":
        print("-> O processo foi concluído.")
    else:
        print("-> Status desconhecido.")
    print("="*30)

def exibir_feed_social(lista_feed):
    """Exibe o feed público de denúncias encerradas."""
    print("\n" + "█"*40)
    print("      📢 FEED: OUTRAS DENÚNCIAS")
    print("      (Casos encerrados e verificados)")
    print("█"*40)
    
    if not lista_feed:
        print("\n[vazio] Ainda não há denúncias públicas encerradas.")
    else:
        for d in lista_feed:
            print(f"\n[{d.get('empresa_nome').upper()}] - {d.get('empresa_local')}")
            print(f"Abuso: {d.get('titulo')}")
            print(f"Relato: \"{d.get('descricao')}\"")
            print(f"--- Denunciado por: {d.get('usuario')} ---")
            print("-" * 40)
