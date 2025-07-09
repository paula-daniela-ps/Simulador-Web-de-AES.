import streamlit as st
from criptografia.aes_ecb import decrypt_ecb
from criptografia.aes_cbc import decrypt_cbc

st.set_page_config(page_title="Descriptografar AES", layout="wide")

st.markdown("# Modo de Uso - Descriptografar Texto com AES")
st.write("""
Esta página permite descriptografar **textos em hexadecimal** usando AES (ECB ou CBC).

**Como usar:**
1. Escolha o modo de operação (ECB ou CBC).
2. A chave será reutilizada automaticamente, se você criptografou anteriormente.
3. Insira o texto criptografado em hexadecimal.
4. Para CBC, o IV (vetor de inicialização) também será reutilizado automaticamente, se disponível.
5. Clique em **Descriptografar**.
""")

def main():
    st.header("Descriptografar Texto com AES")

    modo = st.selectbox("Modo de operação AES", ["ECB", "CBC"])
    tamanho_chave_bits = st.selectbox("Tamanho da Chave AES", ["128 bits", "256 bits"])
    tamanho_chave = 16 if "128" in tamanho_chave_bits else 32

    # Recupera a chave da sessão, se disponível
    chave_hex = st.session_state.get("chave_aes", b"").hex() if "chave_aes" in st.session_state else ""
    chave_input = st.text_input("Chave AES (hex) - será preenchida automaticamente se já foi gerada", value=chave_hex)

    # Recupera texto criptografado da sessão, se disponível
    criptografado_hex = st.text_area("Texto criptografado (em hexadecimal)", value=st.session_state.get("cripto_hex", ""))

    # Recupera IV da sessão se for CBC
    iv_hex = ""
    if modo == "CBC":
        iv_hex = st.text_input("IV (Vetor de Inicialização, hexadecimal)", value=st.session_state.get("iv_hex", ""))

    if st.button("Descriptografar"):
        if not chave_input:
            st.error("Você precisa fornecer a chave AES usada na criptografia.")
            return
        if not criptografado_hex:
            st.error("Você precisa fornecer o texto criptografado.")
            return
        if modo == "CBC" and not iv_hex:
            st.error("Você precisa fornecer o IV para modo CBC.")
            return

        try:
            chave_bytes = bytes.fromhex(chave_input.strip())
            dados = bytes.fromhex(criptografado_hex.strip())

            if modo == "ECB":
                texto = decrypt_ecb(dados, chave_bytes)
            else:
                iv = bytes.fromhex(iv_hex.strip())
                texto = decrypt_cbc(dados, chave_bytes, iv)

            texto_decodificado = texto.decode("utf-8")
            st.success("Texto descriptografado com sucesso!")
            st.text_area("Texto original:", value=texto_decodificado, height=150)

        except UnicodeDecodeError:
            st.error("A descriptografia funcionou, mas o resultado não é um texto UTF-8 válido.")
        except Exception as e:
            st.error(f"Erro na descriptografia: {str(e)}")

if __name__ == "__main__":
    main()
