import streamlit as st
import time
import pandas as pd
import altair as alt
import secrets
from criptografia.aes_ecb import encrypt_ecb, decrypt_ecb
from criptografia.aes_cbc import encrypt_cbc, decrypt_cbc

st.set_page_config(page_title="Comparar Desempenho AES", layout="wide")

st.title("Comparar Desempenho dos Modos AES (ECB vs CBC)")

st.markdown("""
   Modo de Uso - Comparar Desempenho dos Modos AES (ECB vs CBC)\n
   Esta página permite comparar o desempenho dos modos de operação AES (ECB e CBC) em termos de tempo de criptografia, além de eficiência com diferentes tamanhos de chave (AES-128 e AES-256). 
1. Insira o texto para criptografia e selecione os modos de operação e tamanhos de chave que deseja testar.
2. Selecione múltiplas combinações de parâmetros.
3. Clique no botão para executar os testes e visualizar os resultados.
""")

# --- Campos para entrada
texto = st.text_area("Texto para criptografia", height=150, value="Exemplo de texto para teste AES.")
modos = st.multiselect("Modos de operação", options=["ECB", "CBC"], default=["ECB", "CBC"])
tamanhos_chave = st.multiselect("Tamanhos de chave (bits)", options=[128, 256], default=[128, 256])

def medir_tempo_criptografia(modo, dados, chave_bytes):
    start = time.perf_counter()
    if modo == "ECB":
        cript = encrypt_ecb(dados, chave_bytes)
    elif modo == "CBC":
        cript, _ = encrypt_cbc(dados, chave_bytes)
    else:
        raise ValueError(f"Modo {modo} não suportado")
    end = time.perf_counter()
    return cript, (end - start) * 1000

def medir_tempo_descriptografia(modo, dados_cript, chave_bytes, iv=None):
    start = time.perf_counter()
    if modo == "ECB":
        resultado = decrypt_ecb(dados_cript, chave_bytes)
    elif modo == "CBC":
        resultado = decrypt_cbc(dados_cript, chave_bytes, iv)
    else:
        raise ValueError(f"Modo {modo} não suportado")
    end = time.perf_counter()
    return resultado, (end - start) * 1000

if st.button("Executar Comparação"):
    if not texto.strip():
        st.error("Por favor, insira um texto válido.")
    elif not modos:
        st.error("Selecione ao menos um modo de operação.")
    elif not tamanhos_chave:
        st.error("Selecione ao menos um tamanho de chave.")
    else:
        resultados = []
        dados = texto.encode("utf-8")

        total = len(modos) * len(tamanhos_chave)
        progresso = st.progress(0)

        for i, (modo, chave_bits) in enumerate([(m, c) for m in modos for c in tamanhos_chave]):
            tamanho_chave = chave_bits // 8
            chave_bytes = secrets.token_bytes(tamanho_chave)

            # Criptografia e descriptografia
            if modo == "ECB":
                cript, tempo_crip = medir_tempo_criptografia("ECB", dados, chave_bytes)
                _, tempo_decrip = medir_tempo_descriptografia("ECB", cript, chave_bytes)
                iv = None
            elif modo == "CBC":
                cript, tempo_crip = medir_tempo_criptografia("CBC", dados, chave_bytes)
                cript_cbc, iv = encrypt_cbc(dados, chave_bytes)
                _, tempo_decrip = medir_tempo_descriptografia("CBC", cript_cbc, chave_bytes, iv)
                cript = cript_cbc

            eficiencia = 1000 / tempo_crip if tempo_crip > 0 else 0

            resultados.append({
                "Modo": modo,
                "Tamanho da Chave (bits)": chave_bits,
                "Tempo Criptografia (ms)": round(tempo_crip, 3),
                "Tempo Descriptografia (ms)": round(tempo_decrip, 3),
                "Eficiência (1/ms)": round(eficiencia, 3)
            })

            progresso.progress((i + 1) / total)

        df = pd.DataFrame(resultados)
        st.subheader("Tabela de Resultados")
        st.dataframe(df)

        st.markdown("""
        ### Gráficos de Desempenho

        - **Tempo de Criptografia**: mostra quanto tempo (em milissegundos) cada configuração levou para criptografar o texto.
        - **Eficiência**: medida inversa do tempo de criptografia (1 dividido pelo tempo), para destacar quais configurações são mais rápidas.

        As barras coloridas indicam diferentes tamanhos de chave AES utilizados.
        """)

        # Gráfico tempo criptografia
        graf_cripto = alt.Chart(df).mark_bar().encode(
            x=alt.X("Tempo Criptografia (ms):Q", title="Tempo Criptografia (ms)"),
            y=alt.Y("Modo:N", sort='-x'),
            color=alt.Color("Tamanho da Chave (bits):N"),
            tooltip=["Modo", "Tamanho da Chave (bits)", "Tempo Criptografia (ms)"]
        ).properties(title="Tempo de Criptografia por Configuração", height=300)

        # Gráfico eficiência
        graf_efic = alt.Chart(df).mark_bar().encode(
            x=alt.X("Eficiência (1/ms):Q", title="Eficiência (1/ms)"),
            y=alt.Y("Modo:N", sort='-x'),
            color=alt.Color("Tamanho da Chave (bits):N"),
            tooltip=["Modo", "Tamanho da Chave (bits)", "Eficiência (1/ms)"]
        ).properties(title="Eficiência por Configuração", height=300)

        st.altair_chart(graf_cripto, use_container_width=True)
        st.altair_chart(graf_efic, use_container_width=True)
