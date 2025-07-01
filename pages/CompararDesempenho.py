import streamlit as st
import time
import pandas as pd
import altair as alt
from criptografia.aes_ecb import encrypt_ecb
from criptografia.aes_cbc import encrypt_cbc
from criptografia.utils import gerar_chave

def medir_tempo(funcao, *args):
    inicio = time.time()
    funcao(*args)
    fim = time.time()
    return (fim - inicio) * 1000  # tempo em milissegundos

def main():
    st.header("Comparar Desempenho dos Modos AES")

    tamanho_texto = st.slider("Tamanho do texto (em caracteres)", 16, 10000, 1024, step=64)
    texto = "A" * tamanho_texto
    dados = texto.encode("utf-8")
    chave = gerar_chave(16)

    if st.button("Comparar ECB vs CBC"):
        tempo_ecb = medir_tempo(encrypt_ecb, dados, chave)
        tempo_cbc = medir_tempo(encrypt_cbc, dados, chave)

        st.success("🔎 Resultados:")
        st.write(f"🔹 ECB: `{tempo_ecb:.2f} ms`")
        st.write(f"🔹 CBC: `{tempo_cbc:.2f} ms`")

        # Criar DataFrame
        df = pd.DataFrame({
            "Modo": ["ECB", "CBC"],
            "Tempo (ms)": [tempo_ecb, tempo_cbc]
        })

        # Cores personalizadas
        cor_personalizada = alt.Color("Modo:N", scale=alt.Scale(
            domain=["ECB", "CBC"],
            range=["#1f77b4", "#ff7f0e"]  # Azul e laranja
        ))

        # Gráfico com Altair
        chart = alt.Chart(df).mark_bar().encode(
            x=alt.X("Modo:N", title="Modo de Criptografia"),
            y=alt.Y("Tempo (ms):Q", title="Tempo de Execução (ms)"),
            color=cor_personalizada,
            tooltip=["Modo", "Tempo (ms)"]
        ).properties(
            width=500,
            height=400,
            title="Desempenho da Criptografia AES"
        )

        st.altair_chart(chart, use_container_width=True)

if __name__ == "__main__":
    main()
