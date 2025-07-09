# Simulador Web de Criptografia AES

**Aplicação Web educacional** desenvolvida com foco em **criptografia simétrica (AES)**, modos de operação, desempenho e comparação com hash (bcrypt). A interface é baseada em **Streamlit** e projetada para fins didáticos sobre segurança digital.

> Acesse online:  
> https://simulador-web-aes-g9hwlwxq5zdbvcpudmntra.streamlit.app/

---

## Arquitetura do Projeto  

O sistema é organizado em três camadas principais com responsabilidades separadas:

| **Camada**       | **Descrição**                                                                 |
|------------------|------------------------------------------------------------------------------|
| **Interface (UI)** | Interface interativa com o usuário via Streamlit (páginas, formulários, gráficos). |
| **Lógica AES**     | Implementação dos algoritmos de criptografia AES (ECB/CBC), chave e padding.  |
| **Dados/Assets**   | Arquivos de entrada, imagens explicativas e diretório de armazenamento temporário.  |

---

## Mecanismos de Segurança Educacionais

- **Criptografia Simétrica (AES)** com chave de 128 e 256 bits.
- **Hash de Senhas** usando `bcrypt` (não reversível).
- **Visualização de blocos e tempos de execução**.
- **Comparação prática entre criptografia e hash**.

---

## ⚙️ Tecnologias Utilizadas  

| **Camada**       | **Tecnologias**                              |
|------------------|---------------------------------------------|
| **Criptografia** | PyCryptodome (AES), bcrypt                   |
| **Interface**    | Streamlit                                    |
| **Utilitários**  | base64, time, os, pandas                     |

---

## Estrutura de Diretórios   

```plaintext
simulador-aes/
├── app.py                         # Entrada principal
├── criptografia/
│   ├── aes_ecb.py                 # AES modo ECB
│   ├── aes_cbc.py                 # AES modo CBC
│   └── utils.py                   # Geração de chave, padding etc.
├── pages/
│   ├── 1_Criptografar.py
│   ├── 2_Descriptografar.py
│   ├── 3_Comparar ECB vs CBC.py
│   └── 4_Comparar AES vs Hash.py
├── assets/
│   ├── logo.png
│   ├── exemplo.txt
│   └── imagens_teoricas/
├── data/                          # Logs e arquivos temporários
├── requirements.txt
├── README.md
└── LICENSE
```
---
## Como Executar Localmente
Crie e ative um ambiente virtual (opcional):

```plaintext
python -m venv .venv
.venv\Scripts\activate
Instale as dependências:

```
```plaintext
pip install -r requirements.txt
Rode a aplicação:

```
```plaintext
streamlit run app.py
```
Acesse no navegador:
```plaintext
http://localhost:8501/
```
## Observações
A aplicação é voltada para fins educacionais, com visualização prática de conceitos de criptografia.

Não recomendado para produção real, pois não implementa autenticação nem proteção de dados sensíveis.

Ideal para estudantes e professores de cursos de Segurança da Informação, Criptografia, Ciência da Computação e afins.

### Licença
```plaintext
Este projeto é de uso livre para fins acadêmicos e educacionais, sob a Licença MIT. Consulte o arquivo LICENSE para mais detalhes.
