import streamlit as st
import time
import altair as alt
import pandas as pd
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import bcrypt

# === Função auxiliar para medir tempo ===
def medir_tempo(func, *args, **kwargs):
    inicio = time.perf_counter()
    resultado = func(*args, **kwargs)
    fim = time.perf_counter()
    return resultado, (fim - inicio) * 1000  # tempo em milissegundos

# === Configuração da página ===
st.set_page_config(page_title="AES vs Bcrypt", layout="wide")

# === Título e descrição ===
st.title("Comparação: Criptografia AES × Hash de Senhas (bcrypt)")

st.markdown("""
Este simulador demonstra a diferença prática entre:

- **Criptografia simétrica (AES)**: permite encriptar e depois recuperar os dados.
- **Hash de senhas (bcrypt)**: gera uma assinatura irreversível usada para validar senhas.

Preencha os campos abaixo e clique em **Executar Comparação**.
""")

# === Entrada do usuário com colunas lado a lado ===
col1, col2 = st.columns(2)

with col1:
    texto = st.text_input("Mensagem para criptografar (AES)", value="Exemplo confidencial")

with col2:
    senha = st.text_input("Senha para hash (bcrypt)", type="password", value="senha_segura")

# === Execução da comparação ===
if st.button("Executar Comparação"):
    texto_bytes = texto.encode("utf-8")
    chave = get_random_bytes(16)  # AES-128

    # --- AES modo ECB ---
    st.subheader("Criptografia AES - Modo ECB (Electronic Codebook)")

    cipher_ecb = AES.new(chave, AES.MODE_ECB)
    cript_ecb, tempo_ecb = medir_tempo(cipher_ecb.encrypt, pad(texto_bytes, AES.block_size))
    cipher_ecb2 = AES.new(chave, AES.MODE_ECB)
    decript_ecb = unpad(cipher_ecb2.decrypt(cript_ecb), AES.block_size)

    st.markdown("**Texto criptografado (ECB - hexadecimal):**")
    st.code(cript_ecb.hex())

    st.markdown("**Texto descriptografado (ECB):**")
    st.success(decript_ecb.decode("utf-8"))

    st.info(f"Tempo ECB: {tempo_ecb:.2f} ms")

    st.divider()

    # --- AES modo CBC ---
    st.subheader("Criptografia AES - Modo CBC (Cipher Block Chaining)")

    cipher_cbc = AES.new(chave, AES.MODE_CBC)
    iv_cbc = cipher_cbc.iv
    cript_cbc, tempo_cbc = medir_tempo(cipher_cbc.encrypt, pad(texto_bytes, AES.block_size))

    cipher_cbc2 = AES.new(chave, AES.MODE_CBC, iv_cbc)
    decript_cbc = unpad(cipher_cbc2.decrypt(cript_cbc), AES.block_size)

    st.markdown("**Texto criptografado (CBC - hexadecimal):**")
    st.code(cript_cbc.hex())

    st.markdown(f"**IV usado (hexadecimal):** `{iv_cbc.hex()}`")

    st.markdown("**Texto descriptografado (CBC):**")
    st.success(decript_cbc.decode("utf-8"))

    st.info(f"Tempo CBC: {tempo_cbc:.2f} ms")

    st.divider()

    # --- Hash com bcrypt ---
    st.subheader("Hash de Senha com Bcrypt")

    senha_bytes = senha.encode("utf-8")
    hash_bcrypt, tempo_hash = medir_tempo(lambda: bcrypt.hashpw(senha_bytes, bcrypt.gensalt()))
    hash_str = hash_bcrypt.decode()

    correta = bcrypt.checkpw(senha_bytes, hash_bcrypt)
    incorreta = bcrypt.checkpw(b"senha_errada", hash_bcrypt)

    st.markdown("**Hash gerado:**")
    st.code(hash_str)
    st.caption("O hash exibido é apenas para fins demonstrativos. Em sistemas reais, nunca exiba hashes em tela.")

    col_hash1, col_hash2 = st.columns(2)
    col_hash1.write(f"Senha correta verificada? {correta}")
    col_hash2.write(f"Senha errada verificada? {incorreta}")

    st.info(f"Tempo de Geração de Hash (bcrypt): {tempo_hash:.2f} ms")

    st.divider()

    # --- Gráfico comparativo de tempos ---
    st.subheader("Gráfico: Comparação de Tempo de Execução")

    df_tempo = pd.DataFrame({
        "Operação": ["AES-ECB", "AES-CBC", "bcrypt Hash"],
        "Tempo (ms)": [tempo_ecb, tempo_cbc, tempo_hash]
    })

    grafico = alt.Chart(df_tempo).mark_bar().encode(
        y=alt.Y("Operação", sort="-x"),
        x=alt.X("Tempo (ms)", title="Tempo em milissegundos"),
        color=alt.Color("Operação", legend=None, scale=alt.Scale(scheme="set2")),
        tooltip=["Operação", "Tempo (ms)"]
    ).properties(
        height=200,
        width=600,
        title="Tempo de Execução"
    )

    st.altair_chart(grafico, use_container_width=True)

    # Comentário de segurança
    st.markdown(
        """
        Apesar do modo ECB apresentar tempos de execução ligeiramente menores, ele é considerado inseguro para proteger dados reais,<br>
        pois revela padrões e não utiliza aleatoriedade, podendo expor informações sensíveis.<br><br>
        O modo CBC, embora um pouco mais lento, oferece segurança significativamente maior ao usar um vetor de inicialização (IV)<br>
        e encadear os blocos, evitando a exposição de padrões no texto cifrado.<br><br>
        Já o bcrypt é projetado para hashing de senhas, com custo computacional ajustável para dificultar ataques de força bruta,<br>
        sendo intencionalmente mais lento para aumentar a segurança.
        """,
        unsafe_allow_html=True
    )
