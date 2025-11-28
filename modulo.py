import os
import json
from datetime import datetime
import random 
import seguranca 

# ==========================================
# 1. INICIALIZAÇÃO DE ARQUIVOS
# ==========================================

def inicializar_usuarios(arquivo):
    """Carrega DB ou cria admin padrão se vazio."""
    lista = seguranca.ler_seguro(arquivo)
    if not lista:
        padrao = [{"usuario": "admin", "senha": "1234", "tipo": "admin"}]
        seguranca.salvar_seguro(padrao, arquivo)
        return padrao
    return lista

def inicializar_denuncias(caminho):
    """Carrega DB de denúncias."""
    return seguranca.ler_seguro(caminho)

# ==========================================
# 2. AUTENTICAÇÃO E CADASTRO
# ==========================================

def login_usuario(usuario, senha, database_lista):
    """Autentica usuário e retorna objeto + tipo (user/admin)."""
    for u in database_lista:
        if u["usuario"] == usuario and u["senha"] == senha:
            return u, u.get("tipo", "user")
    return None, None

def perguntas_nova_conta():
    print("\n--- Criar nova conta ---")
    return (input("Usuário: "), input("Senha: "), 
            input("Confirme senha: "), input("Link do comprovante: "))

def verificar_nova_conta(user, db_lista, senha, senha_conf, link):
    """Valida duplicidade, senha e formato do link."""
    # 1. Validação de Usuário
    if not user: return print("[ERRO] Usuário vazio.")
    if any(u.get('usuario') == user for u in db_lista):
        return print(f"[ERRO] '{user}' já existe.")

    # 2. Validação de Senha
    if not senha: return print("[ERRO] Senha vazia.")
    if senha != senha_conf: return print("[ERRO] Senhas não conferem.")

    # 3. Validação de Link
    if not link.startswith(("http://", "https://")):
        return print("[ERRO] Link deve começar com http:// ou https://")

    return {
        "usuario": user, "senha": senha, "tipo": "user",
        "comprovante_link": link, "status_verificacao": "pendente"
    }

def adicionar_usuario(db_lista, dados, caminho):
    db_lista.append(dados)
    seguranca.salvar_seguro(db_lista, caminho)
    print("[✔] Usuário cadastrado com sucesso!")

# ==========================================
# 3. DENÚNCIAS E FEED
# ==========================================

def perguntas_denuncia():
    print("-- Dados da denúncia --")
    emp = input("Empresa: ")
    loc = input("Localização: ")
    tit = input("Título: ")
    desc = input("Descrição: ")
    
    print("\n[REDE SOCIAL] Publicar no feed após encerramento?")
    publica = input("S/N: ").upper() == 'S'
    return emp, loc, tit, desc, publica

def gerar_codigo_protocolo(lista):
    """Gera protocolo único formato YYNNNN."""
    ano = datetime.now().strftime("%y")
    while True:
        proto = f"{ano}{random.randint(1000, 9999)}"
        if not any(d.get("protocolo") == proto for d in lista):
            return proto

def verificar_denuncia(emp, loc, tit, desc, publica, lista):
    if not all([emp, tit, desc]):
        print("[ERRO] Campos obrigatórios vazios.")
        return None, None
    
    prot = gerar_codigo_protocolo(lista)
    return {
        "usuario": "Anônimo", "empresa_nome": emp, "empresa_local": loc,
        "titulo": tit, "descricao": desc, "publica": publica,
        "protocolo": prot, "status": "Recebida"
    }, prot

def adicionar_nova_denuncia(dados, caminho):
    lista = seguranca.ler_seguro(caminho)
    lista.append(dados)
    seguranca.salvar_seguro(lista, caminho)
    print(f"[✔] Denúncia registrada! Protocolo: {dados['protocolo']}")

def buscar_protocolo(lista, protocolo):
    for d in lista:
        if d.get("protocolo") == protocolo: return d
    return None

def obter_feed_social(lista):
    """Filtra denúncias públicas e encerradas."""
    return [d for d in lista if d.get("publica") and d.get("status") == "Encerrada"]

# ==========================================
# 4. ADMINISTRAÇÃO
# ==========================================

def listar_usuarios(lista):
    print("\n--- Usuários Comuns ---")
    users = [u for u in lista if u.get("tipo") != "admin"]
    if not users: print("Nenhum usuário encontrado.")
    for u in users:
        print(f"User: {u['usuario']} | Status: {u.get('status_verificacao')} | Link: {u.get('comprovante_link')}")

def aprovar_reprovar_usuario(db_users, path_users, alvo, status, db_denuncias, path_denuncias):
    if status not in ['aprovado', 'reprovado']: return print("[ERRO] Status inválido.")
    
    # 1. Atualiza Usuário
    found = False
    for u in db_users:
        if u['usuario'] == alvo:
            u['status_verificacao'] = status
            found = True
            break
            
    if found:
        seguranca.salvar_seguro(db_users, path_users)
        print(f"[SUCESSO] Usuário atualizado para: {status}")
        
        # 2. Cascata: Cancela denúncias se reprovado
        if status == 'reprovado':
            alterou = False
            for d in db_denuncias:
                if d.get('usuario') == alvo:
                    d['status'] = 'Cancelada (Usuário Reprovado)'
                    alterou = True
            if alterou:
                seguranca.salvar_seguro(db_denuncias, path_denuncias)
                print("[SISTEMA] Denúncias do usuário canceladas.")
    else:
        print("[ERRO] Usuário não encontrado.")

def listar_denuncias(lista):
    print("\n--- Todas as Denúncias ---")
    if not lista: print("Nenhuma denúncia.")
    for d in lista:
        print(f"Prot: {d['protocolo']} | Empresa: {d['empresa_nome']} | Status: {d['status']}")

def alterar_status_denuncia(lista, caminho, protocolo, status):
    for d in lista:
        if d['protocolo'] == protocolo:
            d['status'] = status
            seguranca.salvar_seguro(lista, caminho)
            print(f"[SUCESSO] Status alterado para: {status}")
            return
    print("[ERRO] Protocolo não encontrado.")
