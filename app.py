import streamlit as st
import os

st.set_page_config(page_title="Introdução", layout="wide")

# Verifica se a imagem existe na pasta assets
if os.path.isfile("assets/Logo.png"):
    st.image("assets/Logo.png", use_column_width=True)
    st.success("Imagem carregada com sucesso!")
else:
    st.error("Arquivo assets/Logo.png não encontrado. Verifique o caminho e se o arquivo está no repositório.")

# Texto explicativo simples para teste
st.write("""
# Simulador Web AES

Bem-vindo ao simulador!
""")

# HTML do banner com imagem de fundo e texto sobreposto
html_banner = f"""
<div style="
    background-image: url('data:image/png;base64,{encoded}');
    background-size: cover;
    background-position: center;
    width: 100%;
    height: 350px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    color: white;
    text-align: center;
    text-shadow: 2px 2px 6px black;
">
    <h1 style="font-size: 100px; margin: 0;">Simulador Web AES</h1>
</div>
"""

# Exibe banner
st.markdown(html_banner, unsafe_allow_html=True)

# Texto principal explicativo
st.write("""

---

### 1. Criptografia Simétrica com AES

A criptografia AES (Advanced Encryption Standard) é um algoritmo **simétrico**, o que significa que:
- A **mesma chave secreta** é usada tanto para **criptografar** quanto para **descriptografar** os dados.
- É ideal para proteger **mensagens, arquivos e dados confidenciais** que precisam ser recuperados depois.

No simulador, você verá:
- Como uma mensagem é criptografada usando AES
- Como a mesma mensagem pode ser recuperada com a chave correta
- O **tempo de execução** das operações de criptografia e descriptografia

---

### 2. Hash de Senhas com bcrypt

bcrypt é uma **função de hash** usada para proteger senhas.
- Ao invés de armazenar a senha original, armazenamos um **hash irreversível**.
- Quando o usuário faz login, a senha digitada é comparada com o hash.

No simulador, você verá:
- Como uma senha é transformada em um hash seguro
- Como verificar se uma senha está correta sem revelar o valor original
- O **tempo de execução** da geração do hash e da verificação

---

### 3. Comparação prática

O simulador também exibe um **gráfico comparando os tempos de execução** entre:
- Criptografia AES (criptografar e descriptografar)
- Hash de senhas com bcrypt

Assim, você compreende melhor:
- A **diferença entre proteger dados** e **verificar senhas**
- A importância da escolha da técnica certa para cada situação

---
         
O **Simulador Web de AES** é uma aplicação interativa desenvolvida em **Python com Streamlit**, com objetivo didático de auxiliar no ensino de segurança digital. Ele explora a criptografia simétrica utilizando o algoritmo AES (Advanced Encryption Standard), permitindo que os usuários:

- Realizem criptografia e descriptografia de textos e arquivos fictícios (.txt, .csv);
- Compare os modos de operação **ECB (Electronic Codebook)** e **CBC (Cipher Block Chaining)**, destacando as fragilidades do ECB;
- Testem o desempenho criptográfico com diferentes tamanhos de entrada e chaves (**AES-128 vs. AES-256**);
- Compreendam a diferença entre **criptografia simétrica (AES)** e **funções de hash como o bcrypt**, usadas para proteger senhas.

A aplicação é voltada para fins educacionais, promovendo a experimentação prática e o entendimento dos princípios de segurança da informação.

""")
