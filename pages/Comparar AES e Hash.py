import streamlit as st
import time
import altair as alt
import pandas as pd
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import bcrypt

st.set_page_config(page_title="AES vs Bcrypt", layout="wide")

st.title("Comparação: Criptografia AES × Hash de Senhas (bcrypt)")

st.markdown("""
Este simulador demonstra a diferença prática entre:

- **Criptografia simétrica (AES)**: permite encriptar e depois recuperar os dados.
- **Hash de senhas (bcrypt)**: gera uma assinatura irreversível usada para validar senhas.

Preencha os campos abaixo e clique em **Executar Comparação**.
""")

# === Entrada do usuário ===
col1, col2 = st.columns(2)

with col1:
    texto = st.text_input("Mensagem para criptografar (AES)", value="Exemplo confidencial")

with col2:
    senha = st.text_input("Senha para hash (bcrypt)", type="password", value="senha_segura")


# === Função auxiliar para medir tempo ===
def medir_tempo(func, *args, **kwargs):
    inicio = time.perf_counter()
    resultado = func(*args, **kwargs)
    fim = time.perf_counter()
    return resultado, (fim - inicio) * 1000


# === Ação principal ===
if st.button("Executar Comparação"):
    st.subheader("Criptografia com AES (Simétrica)")

    # --- AES ---
    chave = get_random_bytes(16)  # AES-128
    cipher = AES.new(chave, AES.MODE_CBC)
    iv = cipher.iv
    texto_bytes = texto.encode("utf-8")

    criptografado, tempo_cripto = medir_tempo(cipher.encrypt, pad(texto_bytes, AES.block_size))
    cipher2 = AES.new(chave, AES.MODE_CBC, iv)
    descriptografado, tempo_decripto = medir_tempo(
        lambda: unpad(cipher2.decrypt(criptografado), AES.block_size)
    )

    st.markdown("**Texto criptografado (hexadecimal):**")
    st.code(criptografado.hex(), language="text")

    st.markdown("**Texto descriptografado:**")
    st.success(descriptografado.decode("utf-8"))

    st.info(f"Tempo de Criptografia: {tempo_cripto:.2f} ms")
    st.info(f"Tempo de Descriptografia: {tempo_decripto:.2f} ms")

    st.divider()
    st.subheader("Hash de Senha com Bcrypt")

    senha_bytes = senha.encode("utf-8")
    hash_bcrypt, tempo_hash = medir_tempo(lambda: bcrypt.hashpw(senha_bytes, bcrypt.gensalt()))
    hash_str = hash_bcrypt.decode()

    correta = bcrypt.checkpw(senha_bytes, hash_bcrypt)
    incorreta = bcrypt.checkpw(b"senha_errada", hash_bcrypt)

    st.markdown("**Hash gerado:**")
    st.code(hash_str, language="text")

    col_hash1, col_hash2 = st.columns(2)
    col_hash1.success(f"Senha correta verificada? {correta}")
    col_hash2.error(f"Senha errada verificada? {incorreta}")

    st.info(f"Tempo de Geração de Hash (bcrypt): {tempo_hash:.2f} ms")

    # === Gráfico comparativo ===
    st.divider()
    st.subheader("Gráfico: Comparação de Tempo de Execução")

    df_tempo = pd.DataFrame({
        "Operação": ["AES Criptografia", "AES Descriptografia", "bcrypt Hash"],
        "Tempo (ms)": [tempo_cripto, tempo_decripto, tempo_hash]
    })

    grafico = alt.Chart(df_tempo).mark_bar(size=60).encode(
        x=alt.X("Operação", sort=None),
        y=alt.Y("Tempo (ms)", title="Tempo em milissegundos"),
        color=alt.Color("Operação", legend=None, scale=alt.Scale(scheme="set2")),
        tooltip=["Operação", "Tempo (ms)"]
    ).properties(
        height=350,
        width=600,
        title="Tempo de Execução: AES vs bcrypt"
    )

    st.altair_chart(grafico, use_container_width=True)

    # === Comparação Teórica ===
    st.divider()
    st.subheader("Diferenças entre AES e Bcrypt")

    st.markdown("""
<style>
table {
    width: 100%;
    font-size: 16px;
}
th, td {
    padding: 8px;
    text-align: left;
}
</style>
""", unsafe_allow_html=True)

    st.markdown("""
| Característica            | AES (Criptografia)       | Bcrypt (Hash de Senha)     |
|--------------------------|--------------------------|-----------------------------|
| Tipo                     | Simétrica (reversível)   | Hash (irreversível)         |
| Recupera o original?     | Sim                      | Não                         |
| Usado para               | Proteger dados/mensagens | Autenticação de senhas      |
| Exige chave secreta?     | Sim                      | Não                         |
| Segurança                | Alta (com chave segura)  | Muito alta (com salt + custo) |
| Velocidade               | Muito rápida             | Intencionalmente mais lenta |
""")
