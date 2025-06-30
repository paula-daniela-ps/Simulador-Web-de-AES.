#  Simulador Web de Criptografia AES

Aplicação web educacional desenvolvida com **Python + Streamlit**, com foco na **criptação simétrica (AES)**, comparação entre modos de operação e experimentação de conceitos da segurança digital.

---

##  Arquitetura do Projeto

O sistema está organizado em camadas funcionais com separação de responsabilidades, facilitando manutenção, organização e expansão futura:

| Camada         | Descrição                                                                 |
|----------------|---------------------------------------------------------------------------|
| Interface (UI) | Navegação e interação com o usuário via Streamlit e páginas organizadas   |
| Lógica AES     | Implementação dos modos de operação ECB e CBC, geração de chave, padding  |
| Dados/Assets   | Arquivos de entrada, imagens didáticas e diretório para logs temporários  |

---

---

##  Tecnologias Utilizadas

| Camada       | Tecnologias                  |
|--------------|------------------------------|
| Backend      | Python, PyCryptodome, bcrypt |
| Frontend     | Streamlit                    |
| Utilitários  | time, os, base64             |

---

##  Funcionalidades

- 🔐 **Criptografar Textos ou Arquivos**
- 🔓 **Descriptografar conteúdos com parâmetros personalizados**
- ⚖️ **Comparar desempenho entre ECB x CBC, AES-128 x AES-256**
- 📊 **Exibir tempo de execução e estrutura dos blocos criptografados**
- 🧩 **Diferenciar criptografia (AES) de hash de senhas (bcrypt)**

---
