from Crypto.Cipher import AES
from .utils import pad, unpad

def encrypt_ecb(data: bytes, chave: bytes) -> bytes:
    cipher = AES.new(chave, AES.MODE_ECB)
    return cipher.encrypt(pad(data))

def decrypt_ecb(data: bytes, chave: bytes) -> bytes:
    cipher = AES.new(chave, AES.MODE_ECB)
    return unpad(cipher.decrypt(data))

