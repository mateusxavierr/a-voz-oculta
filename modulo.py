import json
import os
import random

USUARIOS = 'usuarios.json'  # Nome do arquivo que armazena os dados dos usuários
DENUNCIAS = 'denuncias.json'  # Nome do arquivo que armazena as denúncias feitas


def inicializar_usuarios(USUARIOS):
    # Função para garantir que o arquivo de usuários exista e carregar seus dados
    if not os.path.exists(USUARIOS):
        # Se o arquivo não existir, cria um arquivo vazio com uma lista vazia dentro
        try:
            with open(USUARIOS, 'w', encoding='utf-8') as f:
                json.dump([], f)
            return []  # Retorna lista vazia pois o arquivo acabou de ser criado
        except Exception as e:
            # Caso ocorra algum erro ao criar o arquivo, exibe uma mensagem e retorna lista vazia
            print(f"[ERRO] Não foi possível criar o arquivo {USUARIOS}: {e}")
            return []
    else:
        # Se o arquivo existir, tenta carregar os dados dos usuários
        try:
            with open(USUARIOS, 'r', encoding='utf-8') as f:
                return json.load(f)  # Retorna os usuários existentes no arquivo
        except Exception as e:
            # Caso ocorra erro na leitura do arquivo, exibe mensagem e retorna lista vazia
            print(f"[ERRO] Não foi possível carregar o arquivo {USUARIOS}: {e}")
            return []

def inicializar_denuncias(DENUNCIAS):
    # Função para garantir que o arquivo de denúncias exista e carregar seus dados
    if not os.path.exists(DENUNCIAS):
        # Se o arquivo não existir, cria um arquivo vazio com uma lista vazia dentro
        try:
            with open(DENUNCIAS, 'w', encoding='utf-8') as f:
                json.dump([], f)
            return []  # Retorna lista vazia pois o arquivo acabou de ser criado
        except Exception as e:
            # Caso ocorra algum erro ao criar o arquivo, exibe uma mensagem e retorna lista vazia
            print(f"[ERRO] Não foi possível criar o arquivo {DENUNCIAS}: {e}")
            return []
    else:
        # Se o arquivo existir, tenta carregar os dados das denúncias
        try:
            with open(DENUNCIAS, 'r', encoding='utf-8') as f:
                return json.load(f)  # Retorna as denúncias existentes no arquivo
        except Exception as e:
            # Caso ocorra erro na leitura do arquivo, exibe mensagem e retorna lista vazia
            print(f"[ERRO] Não foi possível carregar o arquivo {DENUNCIAS}: {e}")
            return []
    
def procurar_login(database_lista, usuario_digitado, senha_digitada):
    # Função que procura um usuário na lista pelo nome e senha fornecidos
    for dados_usuario in database_lista:
        # Para cada usuário na lista, verifica se o nome e senha conferem
        if dados_usuario.get('usuario') == usuario_digitado:
            if dados_usuario.get('senha') == senha_digitada:
                # Se encontrar correspondência, retorna os dados do usuário e True
                return dados_usuario, True
    # Se não encontrar, retorna None e False
    return None, False

def perguntas_nova_conta():
    # Função que faz as perguntas para cadastro de uma nova conta
    print("\n--- Cadastro de Nova Conta ---")
            
    usuario_digitado = input("Digite um nome de usuário (fictício): ")
    senha_digitada = input("Digite uma senha: ")
    senha_confirmada = input("Confirme sua senha: ")
    caminho_comprovante = input("Cole o caminho completo do arquivo de comprovante: ")

    # Retorna os dados coletados para validação posterior
    return usuario_digitado, senha_digitada, senha_confirmada, caminho_comprovante

def verificar_nova_conta(usuario_digitado, database_lista, senha_digitada, senha_confirmada, caminho_comprovante):
    # Função que valida os dados fornecidos para criação de nova conta

    # Inicializa variáveis de controle para validação
    usuario_valido = False
    senha_valida = False
    comprovante_valido = False
    usuario_ja_existe = False

    # Verifica se o nome de usuário foi informado
    if not usuario_digitado:
        print("[ERRO] O nome de usuário não pode ser vazio.")
    else:
        # Verifica se o nome de usuário já está em uso na base de dados
        for dados_usuario in database_lista:
            if dados_usuario.get('usuario') == usuario_digitado: 
                usuario_ja_existe = True
                break
        
        if usuario_ja_existe:
            print(f"[ERRO] O nome de usuário '{usuario_digitado}' já está em uso.")
        else:
            usuario_valido = True  # Usuário passou na validação

    # Verifica se a senha foi informada e se confere com a confirmação
    if not senha_digitada:
        print("[ERRO] A senha não pode ser vazia.")
    elif senha_digitada != senha_confirmada:
        print("[ERRO] As senhas não conferem.")
    else:
        senha_valida = True  # Senha passou na validação

    # Verifica se o comprovante é um link
if caminho_comprovante.startswith("http://") or caminho_comprovante.startswith("https://"):
    comprovante_valido = True
    comprovante_link = caminho_comprovante  # salva o link para checagem manual depois
    print(f"[INFO] Comprovante enviado como link: {comprovante_link}")
    print("[STATUS] Checagem do comprovante: PENDENTE")
else:
    comprovante_valido = False
    print(f"[ERRO] O comprovante informado não é um link válido: {caminho_comprovante}")
    print("Dica: O comprovante precisa ser uma URL (http ou https).")

    # Se todas as validações passaram, cria e retorna o dicionário com os dados da nova conta
    if usuario_valido and senha_valida and comprovante_valido:
        return {
            "usuario": usuario_digitado,
            "senha": senha_digitada,
            "comprovante_path": caminho_comprovante,
            "status_verificacao": "pendente"  # Status inicial da conta após cadastro
        }    

def adicionar_usuario(database_lista, novo_usuario_dados, usuario_digitado):
    # Função para adicionar um novo usuário à lista e salvar no arquivo JSON
    try:
        database_lista.append(novo_usuario_dados)  # Adiciona novo usuário na lista
        
        # Abre o arquivo de usuários para escrita e salva a lista atualizada formatada
        with open(USUARIOS, 'w', encoding='utf-8') as f:
            json.dump(database_lista, f, indent=4)
        
        print(f"\n[SUCESSO] Conta '{usuario_digitado}' criada!")  # Confirmação para o usuário

    except Exception as e:
        # Caso ocorra erro ao salvar, exibe mensagem crítica de erro
        print(f"\n[ERRO CRÍTICO] Não foi possível salvar sua conta: {e}")

def perguntas_denuncia():
    # Função que coleta as informações para registrar uma nova denúncia
    empresa_nome = input("Qual o nome da empresa a ser denunciada? ")
    empresa_local = input("Qual a localização da empresa (Cidade/Estado)? ")
    titulo_denuncia = input("Qual o título/tipo de abuso (ex: Assédio, Horas extras não pagas)? ")
    
    print("\nDescreva detalhadamente o que aconteceu:")
    print("(Para terminar, pressione ENTER em uma linha vazia)")
    
    descricao_linhas = []
    # Loop para coletar múltiplas linhas da descrição da denúncia
    while True:
        linha = input()
        if linha == "":
            break  # Encerra a coleta quando o usuário digita linha vazia
        descricao_linhas.append(linha)
    
    # Junta as linhas em uma única string com quebras de linha
    descricao_denuncia = "\n".join(descricao_linhas)

    # Retorna os dados coletados para validação posterior
    return empresa_nome, empresa_local, titulo_denuncia, descricao_denuncia

def verificar_denuncia(empresa_nome, empresa_local, titulo_denuncia, descricao_denuncia):
    # Função que valida os dados da denúncia antes de salvar
    if not empresa_nome or not titulo_denuncia or not descricao_denuncia:
        # Campos obrigatórios não preenchidos, exibe erro e retorna None
        print("\n[ERRO] Nome da empresa, Título e Descrição são obrigatórios.")
        print("Denúncia não registrada. Tente novamente.")
        return None, None
    else:
        # Gera um número aleatório para protocolo da denúncia
        protocolo = str(random.randint(100000, 999999))

        # Retorna o dicionário com os dados da denúncia e o protocolo gerado
        return {
            "protocolo": protocolo,
            "empresa_nome": empresa_nome,
            "empresa_local": empresa_local,
            "titulo": titulo_denuncia,
            "descricao": descricao_denuncia,
            "status": "Recebida"  # Status inicial da denúncia
        }, protocolo

def adicionar_nova_denuncia(nova_denuncia_dados, protocolo):
    # Função para adicionar uma nova denúncia ao arquivo JSON e informar o protocolo
    try:
        # Abre o arquivo de denúncias para leitura e carrega a lista atual
        with open(DENUNCIAS, 'r', encoding='utf-8') as f:
            lista_denuncias = json.load(f)
        
        # Adiciona a nova denúncia à lista
        lista_denuncias.append(nova_denuncia_dados)

        # Salva a lista atualizada no arquivo, formatada para melhor leitura
        with open(DENUNCIAS, 'w', encoding='utf-8') as f:
            json.dump(lista_denuncias, f, indent=4)
        
        # Exibe mensagem de sucesso com o número de protocolo para o usuário guardar
        print("\n" + "="*40)
        print("[SUCESSO] Denúncia registrada.")
        print(f"  SEU NÚMERO DE PROTOCOLO É: {protocolo}")
        print("\n  ATENÇÃO: GUARDE ESTE NÚMERO!")
        print("  Você usará ele para checar o 'Status da Denúncia'.")
        print("="*40)

    except Exception as e:
        # Caso ocorra erro ao salvar, exibe mensagem crítica de erro
        print(f"\n[ERRO CRÍTICO] Não foi possível salvar sua denúncia: {e}")


def buscar_protocolo(lista_denuncias, protocolo_alvo):
    # Busca uma denúncia dentro da lista pelo protocolo, retona dict da denúncia ou None
    if not lista_denuncias:
        return None

    for denuncia in lista_denuncias:
        # Compara o protocolo da denúncia atual com o que o usuário digitou
        if denuncia.get('protocolo') == protocolo_alvo:
            return denuncia
    
    return None # Não achou nada
