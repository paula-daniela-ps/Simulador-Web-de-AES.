import streamlit as st
import os
import datetime
import time
import secrets
from criptografia.aes_ecb import encrypt_ecb
from criptografia.aes_cbc import encrypt_cbc

st.set_page_config(page_title="Criptografar AES", layout="wide")

st.markdown("###  Modo de Uso - Criptografar Texto ou Arquivo")
st.write("""
Esta página permite criptografar **textos simples ou arquivos (.txt, .csv)** utilizando o algoritmo AES (Advanced Encryption Standard).

**Como usar:**
1. Escolha o tipo de entrada: Texto ou Arquivo.
2. Escolha o tamanho da chave (AES-128 ou AES-256).
3. A chave será gerada automaticamente uma única vez por sessão.
4. Insira o texto ou envie um arquivo.
5. Clique em **Criptografar** e veja o resultado.
""")

def salvar_resultado(modo, conteudo_hex, tipo):
    agora = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nome_arquivo = f"data/resultados/{tipo}_{modo}_{agora}.txt"
    os.makedirs("data/resultados", exist_ok=True)
    with open(nome_arquivo, "w") as f:
        f.write(conteudo_hex)
    return nome_arquivo

def log_execucao(modo, tempo_ms, tipo):
    log_path = "data/logs/log_execucao.csv"
    os.makedirs("data/logs", exist_ok=True)
    agora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linha = f"{agora},{tipo},{modo},{tempo_ms:.2f}\n"
    if not os.path.exists(log_path):
        with open(log_path, "w") as f:
            f.write("DataHora,Tipo,Modo,Tempo_ms\n")
    with open(log_path, "a") as f:
        f.write(linha)

def criptografar_conteudo(dados: bytes, chave: bytes, modo: str):
    if modo == "ECB":
        resultado = encrypt_ecb(dados, chave)
        return resultado.hex(), None
    elif modo == "CBC":
        resultado, iv = encrypt_cbc(dados, chave)
        return resultado.hex(), iv.hex()
    else:
        raise ValueError("Modo inválido")

def main():
    st.header("Criptografar com AES")

    tipo = st.radio("Escolha o tipo de entrada:", ["Texto", "Arquivo"])
    modo = st.selectbox("Modo de operação AES", ["ECB", "CBC"])

    # Chave persistente por sessão
    tamanho_chave_bits = st.selectbox("Tamanho da Chave AES", ["128 bits", "256 bits"])
    tamanho_chave = 16 if "128" in tamanho_chave_bits else 32

    if "chave_aes" not in st.session_state or len(st.session_state["chave_aes"]) != tamanho_chave:
        st.session_state["chave_aes"] = secrets.token_bytes(tamanho_chave)

    chave_bytes = st.session_state["chave_aes"]
    chave_hex = chave_bytes.hex()
    st.text_input("Chave AES gerada automaticamente (hex)", value=chave_hex, disabled=True)

    if tipo == "Texto":
        exemplo_texto = """Este é um texto de exemplo para testar a criptografia AES. Você pode substituir este texto pelo seu próprio conteúdo e clicar em Criptografar."""
        texto = st.text_area("Digite o texto para criptografar:", value=exemplo_texto)

        if st.button("Criptografar Texto"):
            if not texto:
                st.error("Você precisa digitar um texto.")
                return

            dados = texto.encode("utf-8")
            inicio = time.time()
            resultado_hex, iv_hex = criptografar_conteudo(dados, chave_bytes, modo)
            fim = time.time()

            st.success(f"Texto criptografado com sucesso ({modo})!")
            if iv_hex:
                st.text("IV (vetor de inicialização):")
                st.code(iv_hex, language="plaintext")
            st.text("Texto criptografado:")
            st.code(resultado_hex, language="plaintext")

            tempo_ms = (fim - inicio) * 1000
            caminho = salvar_resultado(modo, resultado_hex, tipo="texto")
            log_execucao(modo, tempo_ms, tipo="texto")
            st.info(f"Resultado salvo em: `{caminho}`")
            st.success(f"Tempo de execução: {tempo_ms:.2f} ms")

    else:
        arquivo = st.file_uploader("Envie um arquivo .txt ou .csv", type=["txt", "csv"])

        if st.button("Criptografar Arquivo"):
            if arquivo is None:
                st.error("Você precisa enviar um arquivo válido.")
                return

            dados = arquivo.read()
            inicio = time.time()
            resultado_hex, iv_hex = criptografar_conteudo(dados, chave_bytes, modo)
            fim = time.time()

            st.success(f"Arquivo criptografado com sucesso ({modo})!")
            if iv_hex:
                st.text("IV (vetor de inicialização):")
                st.code(iv_hex, language="plaintext")
            st.text("Conteúdo criptografado (hex):")
            st.code(resultado_hex[:1000], language="plaintext")  

            tempo_ms = (fim - inicio) * 1000
            caminho = salvar_resultado(modo, resultado_hex, tipo="arquivo")
            log_execucao(modo, tempo_ms, tipo="arquivo")
            st.success(f"Tempo de execução: {tempo_ms:.2f} ms")

if __name__ == "__main__":
    main()
