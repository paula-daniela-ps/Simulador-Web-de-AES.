from Crypto.Random import get_random_bytes

def pad(data: bytes, block_size: int = 16) -> bytes:
    padding_len = block_size - (len(data) % block_size)
    padding = bytes([padding_len] * padding_len)
    return data + padding

def unpad(data: bytes) -> bytes:
    padding_len = data[-1]
    return data[:-padding_len]

def gerar_chave(tamanho: int = 16) -> bytes:
    return get_random_bytes(tamanho)
