from Crypto.Cipher import DES
from Crypto.Cipher import AES


def cesar_cipher_encrypt(message: str, key: str):
    return ''.join(map(lambda ch: chr((ord(ch) + 3) % 256), message))


def cesar_cipher_decrypt(message: str, key: str):
    return ''.join(map(lambda ch: chr((256 + ord(ch) - 3) % 256), message))


def vigenere_cipher_encrypt(message: str, key: str):
    key_length = len(key)
    if key_length <= 0:
        key = chr(3)
        key_length = len(key)

    result = ''
    for i in range(0, len(message)):
        result += chr((ord(message[i]) + ord(key[i % key_length])) % 256)
    return result


def vigenere_cipher_decrypt(message: str, key: str):
    key_length = len(key)
    if key_length <= 0:
        key = chr(3)
        key_length = len(key)

    result = ''
    for i in range(0, len(message)):
        result += chr((256 + ord(message[i]) - ord(key[i % key_length])) % 256)
    return result


def pad(text: bytearray, by: int):
    while len(text) % by != 0:
        text += b" "
    return text


def str2bytearray(string: str):
    return bytearray(string, encoding="1251")


def bytearray2str(bytearr: bytearray):
    return str(bytearr, encoding="1251")


def des_cipher_encrypt(message: str, key: str):
    byte_key = pad(str2bytearray(key))
    print('Length of byte_key: ' + str(len(byte_key)))
    if len(byte_key) != 8:
        raise ValueError('ValueError: Length of key must be equal to 8')

    message = pad(str2bytearray(message), len(byte_key))

    des = DES.new(byte_key, DES.MODE_ECB)
    output = bytearray(len(message))
    des.encrypt(message, output=output)
    return bytearray2str(output)


def des_cipher_decrypt(message: str, key: str):
    byte_key = pad(str2bytearray(key))
    print('Length of byte_key: ' + str(len(byte_key)))
    if len(byte_key) != 8:
        raise ValueError('ValueError: Length of key must be equal to 8')

    message = pad(str2bytearray(message), len(byte_key))

    des = DES.new(byte_key, DES.MODE_ECB)
    output = bytearray(len(message))
    des.decrypt(message, output=output)
    return bytearray2str(output).strip()


def aes_cipher_encrypt(message: str, key: str):
    byte_key = str2bytearray(key)
    if len(byte_key) not in (16, 24, 32):
        raise ValueError("Incorrect AES key length (%d bytes)" % len(key))

    aes = AES.new(byte_key, AES.MODE_ECB)

    message = pad(str2bytearray(message), len(byte_key))

    output = bytearray(len(message))
    aes.encrypt(message, output=output)
    return bytearray2str(output)


def aes_cipher_decrypt(message: str, key: str):
    byte_key = str2bytearray(key)
    if len(byte_key) not in (16, 24, 32):
        raise ValueError("Incorrect AES key length (%d bytes)" % len(key))

    aes = AES.new(byte_key, AES.MODE_ECB)

    message = pad(str2bytearray(message), len(byte_key))

    output = bytearray(len(message))
    aes.decrypt(message, output=output)
    return bytearray2str(output).strip()
