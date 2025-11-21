import os
import json
from datetime import datetime

# Inicialização dos bancos de dados

def inicializar_usuarios(caminho):
    """Carrega ou cria o arquivo de usuários."""
    if os.path.exists(caminho):
        try:
            with open(caminho, 'r', encoding='utf-8') as arquivo:
                return json.load(arquivo)
        except json.JSONDecodeError:
            print("[ERRO] Arquivo de usuários corrompido. Criando um novo.")
            return []
    return []


def inicializar_denuncias(caminho):
    """Carrega ou cria o arquivo de denúncias."""
    if os.path.exists(caminho):
        try:
            with open(caminho, 'r', encoding='utf-8') as arquivo:
                return json.load(arquivo)
        except json.JSONDecodeError:
            print("[ERRO] Arquivo de denúncias corrompido. Criando um novo.")
            return []
    return []


# Validação da criação de conta

def verificar_nova_conta(usuario_digitado, database_lista, senha_digitada, senha_confirmada, caminho_comprovante):

    usuario_valido = False
    senha_valida = False
    comprovante_valido = False
    usuario_ja_existe = False

    # Verificação do nome de usuário
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

    # Verificação da senha
    if not senha_digitada:
        print("[ERRO] A senha não pode ser vazia.")
    elif senha_digitada != senha_confirmada:
        print("[ERRO] As senhas não conferem.")
    else:
        senha_valida = True

    # Verificação do comprovante como link
    if caminho_comprovante.startswith("http://") or caminho_comprovante.startswith("https://"):
        comprovante_valido = True
        print(f"[INFO] Comprovante enviado como link: {caminho_comprovante}")
        print("[STATUS] Checagem do comprovante: PENDENTE")
    else:
        print(f"[ERRO] O comprovante informado não é um link válido: {caminho_comprovante}")
        print("Dica: Deve começar com http:// ou https://")

    # Se tudo estiver válido, retorna os dados
    if usuario_valido and senha_valida and comprovante_valido:
        return {
            "usuario": usuario_digitado,
            "senha": senha_digitada,
            "comprovante_link": caminho_comprovante,
            "status_verificacao": "pendente"
        }

    return None


# Adicionar novo usuário ao sistema

def adicionar_usuario(database_lista, dados_usuario, caminho_db):
    """Salva o novo usuário no banco de dados JSON."""
    database_lista.append(dados_usuario)

    with open(caminho_db, 'w', encoding='utf-8') as arquivo:
        json.dump(database_lista, arquivo, indent=4, ensure_ascii=False)

    print("[✔] Usuário cadastrado com sucesso!")


# Login

def procurar_login(database_lista, usuario_digitado, senha_digitada):
    """Procura usuário pelo nome e senha."""
    for usuario in database_lista:
        if usuario.get('usuario') == usuario_digitado and usuario.get('senha') == senha_digitada:
            return usuario, True
    return None, False


# Inputs para criação de conta

def perguntas_nova_conta():
    print("\n--- Criar nova conta ---")
    usuario = input("Digite o nome de usuário: ")
    senha = input("Digite sua senha: ")
    senha_confirma = input("Confirme sua senha: ")
    comprovante = input("Cole o link do comprovante de vínculo: ")
    return usuario, senha, senha_confirma, comprovante


# Coleta de dados de denúncia

def perguntas_denuncia():
    print("-- Dados da empresa --")
    empresa_nome = input("Nome da empresa: ")
    empresa_local = input("Localização: ")
    titulo = input("Título da denúncia: ")
    descricao = input("Descreva a denúncia: ")
    return empresa_nome, empresa_local, titulo, descricao


# Criação e validação de denúncia

def gerar_codigo_protocolo():
    agora = datetime.now()
    return agora.strftime("PROTOC-%Y%m%d-%H%M%S")


def verificar_denuncia(empresa_nome, empresa_local, titulo, descricao):
    """Valida os campos da denúncia."""
    if not empresa_nome or not titulo or not descricao:
        print("[ERRO] Campos obrigatórios não podem estar vazios.")
        return None, None

    protocolo = gerar_codigo_protocolo()

    dados = {
        "empresa_nome": empresa_nome,
        "empresa_local": empresa_local,
        "titulo": titulo,
        "descricao": descricao,
        "protocolo": protocolo,
        "status": "Recebida"
    }

    return dados, protocolo


def adicionar_nova_denuncia(denuncia, caminho):
    """Adiciona denúncia ao banco de dados."""
    denuncias = inicializar_denuncias(caminho)
    denuncias.append(denuncia)

    with open(caminho, 'w', encoding='utf-8') as arquivo:
        json.dump(denuncias, arquivo, indent=4, ensure_ascii=False)

    print(f"[✔] Denúncia registrada! Protocolo: {denuncia['protocolo']}")


# Busca de denúncias

def buscar_protocolo(denuncias_lista, protocolo_digitado):
    """Busca denúncia pelo número de protocolo."""
    for d in denuncias_lista:
        if d.get("protocolo") == protocolo_digitado:
            return d
    return None


def encontrar_denuncias_por_usuario(usuario, denuncias_lista):
    """Retorna todas as denúncias feitas por um usuário."""
    return [d for d in denuncias_lista if d.get("usuario") == usuario]
