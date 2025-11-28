# 👁️ A Voz Oculta

> Plataforma de denúncias e conformidade social para a indústria da moda.

**A Voz Oculta** é uma aplicação CLI (Command Line Interface) desenvolvida em Python que permite que trabalhadores denunciem abusos trabalhistas de forma anônima ou verificada, convertendo feedback em indicadores de conformidade para o setor.

## 🚀 Funcionalidades Principais

* **Denúncia Anônima:** Qualquer pessoa pode registrar uma denúncia sem login e receber um protocolo único.
* **Sistema de Contas:** Trabalhadores podem criar contas enviando um link de comprovante de vínculo.
* **Verificação de Usuários:** Administradores aprovam ou reprovam contas com base nos comprovantes.
* **Gestão de Denúncias:** Administradores alteram o status das denúncias (Recebida -> Em Análise -> Encerrada).
* **Rede Social (Feed):** Denúncias marcadas como públicas e já encerradas aparecem em um feed comunitário.
* **Segurança:** Todos os dados locais (`.json`) são criptografados nativamente (XOR + Base64).

## 📂 Estrutura do Projeto

* `main.py`: Arquivo principal. Gerencia o loop do programa e os menus.
* `modulo.py`: Contém a lógica de negócios, validações e funções administrativas.
* `textos.py`: Contém as interfaces de texto e mensagens para o usuário.
* `seguranca.py`: Módulo responsável por criptografar e descriptografar os dados.

## 🛠️ Pré-requisitos

* Python 3.x instalado.
* Nenhuma biblioteca externa é obrigatória (usa apenas bibliotecas padrão: `json`, `os`, `base64`, `datetime`, `random`).

## ⚡ Como Executar

1.  Clone o repositório ou baixe os arquivos.
2.  Abra o terminal na pasta do projeto.
3.  Execute o arquivo principal:
    ```bash
    python main.py
    ```

## 🔐 Acesso Administrativo

Ao rodar o sistema pela primeira vez, uma conta de administrador padrão é criada automaticamente:

* **Usuário:** `admin`
* **Senha:** `1234`

Use esta conta para aprovar novos usuários e gerenciar denúncias.

## 🛡️ Criptografia

O projeto utiliza um sistema de criptografia simétrica XOR.
* Os arquivos `usuarios.json` e `denuncias.json` são ilegíveis externamente.
* **Atenção:** Não tente editar os arquivos JSON manualmente, pois isso corromperá os dados.

## 📝 Licença

Este projeto foi desenvolvido para fins acadêmicos.
