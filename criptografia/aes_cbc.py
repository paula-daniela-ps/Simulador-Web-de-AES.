from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from .utils import pad, unpad

def encrypt_cbc(data: bytes, chave: bytes) -> tuple[bytes, bytes]:
    iv = get_random_bytes(16)
    cipher = AES.new(chave, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(pad(data))
    return encrypted, iv

def decrypt_cbc(data: bytes, chave: bytes, iv: bytes) -> bytes:
    cipher = AES.new(chave, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(data))
