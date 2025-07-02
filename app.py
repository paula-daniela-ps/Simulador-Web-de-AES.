import streamlit as st

import streamlit as st

import streamlit as st

# Configura página
st.set_page_config(page_title="Título com Imagem", layout="wide")

# Caminho ou URL da imagem de fundo
imagem_fundo = "/mnt/data/a1aa4429-767d-4635-92c7-8fef3642d9c1.png"

# Código HTML + CSS para o banner com texto sobre a imagem
html_banner = f"""
<div style="
    position: relative;
    text-align: center;
    color: white;
    font-family: 'Arial Black', Arial, sans-serif;
    font-weight: bold;
    font-size: 72px;
    background-image: url('{imagem_fundo}');
    background-size: cover;
    background-position: center;
    height: 150px;
    display: flex;
    align-items: center;
    justify-content: flex start;
    ">
    <span>Simulador Web AES</span>
</div>
"""

st.markdown(html_banner, unsafe_allow_html=True)

st.write("""
Este simulador demonstra **dois conceitos fundamentais da segurança da informação**:

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

### Comparação prática

O simulador também exibe um **gráfico comparando os tempos de execução** entre:
- Criptografia AES (criptografar e descriptografar)
- Hash de senhas com bcrypt

Assim, você compreende melhor:
- A **diferença entre proteger dados** e **verificar senhas**
- A importância da escolha da técnica certa para cada situação
""")


st.write("""
O Simulador Web de AES é uma aplicação interativa desenvolvida em Python com Streamlit, com objetivo didático de auxiliar no ensino de segurança digital. Ele explora a criptografia simétrica utilizando o algoritmo AES (Advanced Encryption Standard), permitindo que os usuários:

- Realizem criptografia e descriptografia de textos e arquivos fictícios (.txt, .csv);
- Compare os modos de operação ECB (Electronic Codebook) e CBC (Cipher Block Chaining), destacando as fragilidades do ECB;
- Testem o desempenho criptográfico com diferentes tamanhos de entrada e chaves (AES-128 vs. AES-256);
- Compreendam a diferença entre criptografia simétrica (AES) e funções de hash como o `bcrypt`, usadas para proteger senhas.

A aplicação é voltada para fins educacionais, promovendo a experimentação prática e o entendimento dos princípios de segurança da informação.

""")


#adicionar introção + contextualização de temas etc...

