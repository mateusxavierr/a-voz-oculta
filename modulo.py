import os
import json
from datetime import datetime

# ==========================================
# 1. INICIALIZAÇÃO E ARQUIVOS
# ==========================================

def inicializar_usuarios(arquivo):
    """Carrega usuários ou cria arquivo com admin padrão se não existir."""
    if not os.path.exists(arquivo):
        # Cria arquivo com admin padrão
        usuarios = [{"usuario": "admin", "senha": "1234", "tipo": "admin"}]
        try:
            with open(arquivo, "w", encoding='utf-8') as f:
                json.dump(usuarios, f, indent=4, ensure_ascii=False)
            return usuarios
        except Exception as e:
            print(f"[ERRO] Falha ao criar arquivo de usuários: {e}")
            return []
    else:
        try:
            with open(arquivo, "r", encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("[ERRO] Arquivo de usuários corrompido. Resetando para padrão.")
            return [{"usuario": "admin", "senha": "1234", "tipo": "admin"}]

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

# ==========================================
# 2. AUTENTICAÇÃO E CADASTRO
# ==========================================

def login_usuario(usuario, senha, database_lista):
    """Verifica credenciais e retorna usuário e tipo."""
    for u in database_lista:
        if u["usuario"] == usuario and u["senha"] == senha:
            # Se tiver chave 'tipo', usa ela. Se não, assume 'user'
            tipo = u.get("tipo", "user")
            return u, tipo
    return None, None

def perguntas_nova_conta():
    print("\n--- Criar nova conta ---")
    usuario = input("Digite o nome de usuário: ")
    senha = input("Digite sua senha: ")
    senha_confirma = input("Confirme sua senha: ")
    comprovante = input("Cole o link do comprovante de vínculo (http/https): ")
    return usuario, senha, senha_confirma, comprovante

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
        print(f"[INFO] Comprovante reconhecido como link.")
    else:
        print(f"[ERRO] O comprovante deve ser um link (começar com http:// ou https://)")

    # Retorno
    if usuario_valido and senha_valida and comprovante_valido:
        return {
            "usuario": usuario_digitado,
            "senha": senha_digitada,
            "tipo": "user", # Define explicitamente como user comum
            "comprovante_link": caminho_comprovante,
            "status_verificacao": "pendente"
        }
    return None

def adicionar_usuario(database_lista, dados_usuario, caminho_db):
    database_lista.append(dados_usuario)
    with open(caminho_db, 'w', encoding='utf-8') as arquivo:
        json.dump(database_lista, arquivo, indent=4, ensure_ascii=False)
    print("[✔] Usuário cadastrado com sucesso!")

# ==========================================
# 3. DENÚNCIAS (USUÁRIO)
# ==========================================

def perguntas_denuncia():
    print("-- Dados da empresa --")
    empresa_nome = input("Nome da empresa: ")
    empresa_local = input("Localização: ")
    titulo = input("Título da denúncia: ")
    descricao = input("Descreva a denúncia: ")
    return empresa_nome, empresa_local, titulo, descricao

def gerar_codigo_protocolo():
    agora = datetime.now()
    return agora.strftime("PROTOC-%Y%m%d-%H%M%S")

def verificar_denuncia(empresa_nome, empresa_local, titulo, descricao):
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
    denuncias = inicializar_denuncias(caminho)
    denuncias.append(denuncia)
    with open(caminho, 'w', encoding='utf-8') as arquivo:
        json.dump(denuncias, arquivo, indent=4, ensure_ascii=False)
    print(f"[✔] Denúncia registrada! Protocolo: {denuncia['protocolo']}")

def buscar_protocolo(denuncias_lista, protocolo_digitado):
    for d in denuncias_lista:
        if d.get("protocolo") == protocolo_digitado:
            return d
    return None

# ==========================================
# 4. FUNÇÕES DE ADMIN (NOVAS)
# ==========================================

def listar_usuarios(database_lista):
    print("\n--- Lista de Usuários ---")
    encontrou = False
    for u in database_lista:
        if u.get("tipo") != "admin": # Não precisa listar o admin
            status = u.get("status_verificacao", "N/A")
            print(f"Usuário: {u['usuario']} | Status: {status} | Link: {u.get('comprovante_link')}")
            encontrou = True
    if not encontrou:
        print("Nenhum usuário comum cadastrado.")

def aprovar_reprovar_usuario(database_lista, caminho_db, usuario_alvo, novo_status):
    novo_status = novo_status.lower()
    if novo_status not in ['aprovado', 'reprovado']:
        print("[ERRO] Status deve ser 'aprovado' ou 'reprovado'.")
        return

    encontrado = False
    for u in database_lista:
        if u['usuario'] == usuario_alvo:
            u['status_verificacao'] = novo_status
            encontrado = True
            print(f"[SUCESSO] Usuário {usuario_alvo} agora está: {novo_status}")
            break
    
    if encontrado:
        # Salva no arquivo
        with open(caminho_db, 'w', encoding='utf-8') as arquivo:
            json.dump(database_lista, arquivo, indent=4, ensure_ascii=False)
    else:
        print("[ERRO] Usuário não encontrado.")

def listar_denuncias(denuncias_lista):
    print("\n--- Lista de Denúncias ---")
    if not denuncias_lista:
        print("Nenhuma denúncia registrada.")
        return

    for d in denuncias_lista:
        print(f"Prot: {d['protocolo']} | Empresa: {d['empresa_nome']} | Status: {d['status']}")

def alterar_status_denuncia(denuncias_lista, caminho_db, protocolo, novo_status):
    encontrado = False
    for d in denuncias_lista:
        if d['protocolo'] == protocolo:
            d['status'] = novo_status
            encontrado = True
            print(f"[SUCESSO] Protocolo {protocolo} atualizado para: {novo_status}")
            break
    
    if encontrado:
        with open(caminho_db, 'w', encoding='utf-8') as arquivo:
            json.dump(denuncias_lista, arquivo, indent=4, ensure_ascii=False)
    else:
        print("[ERRO] Protocolo não encontrado.")
