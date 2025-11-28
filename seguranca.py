import json
import base64
import os

# Chave simétrica para operação XOR. Se alterada, dados antigos tornam-se ilegíveis.
CHAVE_SECRETA = "chave_mestra_do_projeto_voz_oculta_2025"

def _xor_dados(dados_bytes):
    """Aplica cifragem XOR bit a bit usando a chave secreta."""
    chave_bytes = CHAVE_SECRETA.encode('utf-8')
    resultado = bytearray()
    
    for i, byte in enumerate(dados_bytes):
        resultado.append(byte ^ chave_bytes[i % len(chave_bytes)])
    
    return bytes(resultado)

def salvar_seguro(dados, caminho_arquivo):
    """Serializa, aplica XOR e codifica em Base64 antes de salvar."""
    try:
        # 1. Serialização JSON
        json_str = json.dumps(dados, indent=4, ensure_ascii=False)
        # 2. Criptografia
        dados_criptografados = _xor_dados(json_str.encode('utf-8'))
        # 3. Codificação para transporte (Base64) e escrita
        with open(caminho_arquivo, 'wb') as f:
            f.write(base64.b64encode(dados_criptografados))
    except Exception as e:
        print(f"[ERRO DE SEGURANÇA] Falha ao salvar: {e}")

def ler_seguro(caminho_arquivo):
    """Lê arquivo Base64, decodifica e reverte o XOR para obter JSON."""
    if not os.path.exists(caminho_arquivo):
        return []
    
    try:
        with open(caminho_arquivo, 'rb') as f:
            conteudo_base64 = f.read()
            
        if not conteudo_base64: return []

        # 1. Decodificação Base64 e Descriptografia XOR
        dados_bytes = _xor_dados(base64.b64decode(conteudo_base64))
        # 2. Desserialização JSON
        return json.loads(dados_bytes.decode('utf-8'))

    except Exception:
        print(f"[AVISO] Arquivo {caminho_arquivo} ilegível. Iniciando vazio.")
        return []
