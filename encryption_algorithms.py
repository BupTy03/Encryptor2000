def cesar_cipher_encrypt(message: str, key: str):
    result = ''
    for ch in message:
        result += chr(ord(ch) + 3)
    return result


def cesar_cipher_decrypt(message: str, key: str):
    result = ''
    for ch in message:
        result += chr(ord(ch) - 3)
    return result


def vigenere_cipher_encrypt(message: str, key: str):
    result = ''
    key_length = len(key)
    if key_length <= 0:
        key = chr(3)
        key_length = len(key)

    for i in range(0, len(message)):
        result += chr(ord(message[i]) + ord(key[i % key_length]))
    return result


def vigenere_cipher_decrypt(message: str, key: str):
    result = ''
    key_length = len(key)
    if key_length <= 0:
        key = chr(3)
        key_length = len(key)

    for i in range(0, len(message)):
        result += chr(ord(message[i]) - ord(key[i % key_length]))
    return result
