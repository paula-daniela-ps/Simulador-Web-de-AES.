import streamlit as st
import os

st.set_page_config(page_title="Introdução", layout="wide")

if os.path.isfile("assets/Logo.png"):
    st.image("assets/Logo.png", use_column_width=True)
    st.success("Imagem carregada com sucesso!")
else:
    st.error("Arquivo assets/Logo.png não encontrado. Verifique o caminho e o nome do arquivo.")

st.write("""
# Simulador Web AES

Bem-vindo ao simulador!
""")
