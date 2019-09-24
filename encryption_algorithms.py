from Crypto.Cipher import DES
from Crypto.Cipher import AES


def cesar_cipher_encrypt(message: str, key: str):
    return ''.join(map(lambda ch: chr(ord(ch) + 3), message))


def cesar_cipher_decrypt(message: str, key: str):
    return ''.join(map(lambda ch: chr(ord(ch) - 3), message))


def vigenere_cipher_encrypt(message: str, key: str):
    key_length = len(key)
    if key_length <= 0:
        key = chr(3)
        key_length = len(key)

    result = ''
    for i in range(0, len(message)):
        result += chr(ord(message[i]) + ord(key[i % key_length]))
    return result


def vigenere_cipher_decrypt(message: str, key: str):
    key_length = len(key)
    if key_length <= 0:
        key = chr(3)
        key_length = len(key)

    result = ''
    for i in range(0, len(message)):
        result += chr(ord(message[i]) - ord(key[i % key_length]))
    return result


def pad(text: bytearray):
    while len(text) % 8 != 0:
        text += b' '
    return text

# def des_cipher_encrypt(message: str, key: str):
#     default_encoding = 'latin1'
#     byte_key = bytearray(key, encoding=default_encoding)
#     print('len(byte_key): ' + str(len(byte_key)))
#     if len(byte_key) != 8:
#         raise ValueError('ValueError: Length of key must be equal to 8')
#
#     des = DES.new(byte_key, DES.MODE_EAX)
#     return str(des.encrypt(pad(bytearray(message, encoding=default_encoding))), encoding=default_encoding)
#
#
# def des_cipher_decrypt(message: str, key: str):
#     default_encoding = 'latin1'
#     byte_key = bytearray(key, encoding=default_encoding)
#     print('len(byte_key): ' + str(len(byte_key)))
#     if len(byte_key) != 8:
#         raise ValueError('ValueError: Length of key must be equal to 8')
#
#     des = DES.new(byte_key, DES.MODE_EAX)
#     return str(des.decrypt(pad(bytearray(message, encoding=default_encoding))), encoding=default_encoding)


def des_cipher_encrypt(message: str, key: str):
    byte_key = bytearray(map(ord, key))
    print('len(byte_key): ' + str(len(byte_key)))
    if len(byte_key) != 8:
        raise ValueError('ValueError: Length of key must be equal to 8')

    des = DES.new(byte_key, DES.MODE_EAX)
    return ''.join(map(chr, des.encrypt(bytearray(map(ord, message)))))


def des_cipher_decrypt(message: str, key: str):
    byte_key = bytearray(map(ord, key))
    print('len(byte_key): ' + str(len(byte_key)))
    if len(byte_key) != 8:
        raise ValueError('ValueError: Length of key must be equal to 8')

    des = DES.new(byte_key, DES.MODE_EAX)
    return ''.join(map(chr, des.decrypt(bytearray(map(ord, message)))))


def aes_cipher_encrypt(message: str, key: str):
    aes = AES.new(bytearray(key, 'utf8'), AES.MODE_CBC)
    return ''.join(map(chr, aes.encrypt(bytearray(map(ord, message)))))


def aes_cipher_decrypt(message: str, key: str):
    aes = AES.new(bytearray(key, 'utf8'), AES.MODE_CBC)
    return ''.join(map(chr, aes.decrypt(bytearray(map(ord, message)))))
