import streamlit as st
from criptografia.aes_ecb import decrypt_ecb
from criptografia.aes_cbc import decrypt_cbc

def main():
    st.header("Descriptografar Texto com AES")

    criptografado_hex = st.text_area("Texto criptografado (em hexadecimal)")
    chave = st.text_input("Chave AES (16 caracteres)", max_chars=16, value="1234567890abcdef")
    modo = st.selectbox("Modo de operação AES", ["ECB", "CBC"])

    if modo == "CBC":
        iv_hex = st.text_input("IV (Vetor de Inicialização, hexadecimal)")

    if st.button("Descriptografar"):
        if len(chave) != 16:
            st.error("A chave precisa ter exatamente 16 caracteres.")
            return

        try:
            dados = bytes.fromhex(criptografado_hex.strip())
            chave_bytes = chave.encode("utf-8")

            if modo == "ECB":
                texto = decrypt_ecb(dados, chave_bytes)

            elif modo == "CBC":
                iv = bytes.fromhex(iv_hex.strip())
                texto = decrypt_cbc(dados, chave_bytes, iv)

            st.success("Texto descriptografado com sucesso!")
            st.text_area("Texto original:", value=texto.decode("utf-8"), height=150)

        except Exception as e:
            st.error(f"Erro na descriptografia: {str(e)}")

if __name__ == "__main__":
    main()
