# em desenvolvimento
import streamlit as st
import os
import datetime
from criptografia.aes_ecb import encrypt_ecb
from criptografia.aes_cbc import encrypt_cbc

def salvar_resultado(modo, conteudo_hex):
    agora = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nome_arquivo = f"data/resultados/{modo}_{agora}.txt"
    with open(nome_arquivo, "w") as f:
        f.write(conteudo_hex)
    return nome_arquivo

def log_execucao(modo, tempo_ms):
    log_path = "data/logs/log_execucao.csv"
    agora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linha = f"{agora},{modo},{tempo_ms:.2f}\n"
    # Se o log não existir, adiciona cabeçalho
    if not os.path.exists(log_path):
        with open(log_path, "w") as f:
            f.write("DataHora,Modo,Tempo_ms\n")
    with open(log_path, "a") as f:
        f.write(linha)

def main():
    st.header("Criptografar Texto com AES")

    texto = st.text_area("Digite o texto para criptografar:")
    chave = st.text_input("Chave AES (16 caracteres)", max_chars=16, value="1234567890abcdef")
    modo = st.selectbox("Modo de operação AES", ["ECB", "CBC"])

    if st.button("Criptografar"):
        if len(chave) != 16:
            st.error("A chave precisa ter exatamente 16 caracteres.")
            return

        import time
        dados = texto.encode("utf-8")
        chave_bytes = chave.encode("utf-8")
        inicio = time.time()

        if modo == "ECB":
            resultado = encrypt_ecb(dados, chave_bytes)
            resultado_hex = resultado.hex()
            st.success("Texto criptografado com sucesso no modo ECB!")
            st.code(resultado_hex, language="plaintext")

        elif modo == "CBC":
            resultado, iv = encrypt_cbc(dados, chave_bytes)
            resultado_hex = resultado.hex()
            iv_hex = iv.hex()
            st.success("Texto criptografado com sucesso no modo CBC!")
            st.text("IV (vetor de inicialização):")
            st.code(iv_hex, language="plaintext")
            st.text("Texto criptografado:")
            st.code(resultado_hex, language="plaintext")

        fim = time.time()
        tempo_ms = (fim - inicio) * 1000

        # Salvar resultado e log
        caminho = salvar_resultado(modo, resultado_hex)
        log_execucao(modo, tempo_ms)

        st.info(f"Resultado salvo em: `{caminho}`")
        st.success(f"Tempo de execução: {tempo_ms:.2f} ms")

if __name__ == "__main__":
    main()
