# code by nikidziuba

import hashlib
from Crypto.Cipher import AES
import os
import demjson3


def pad(data, block_size):
    print(f'Padding data: {data}')
    padding_length = block_size - len(data) % block_size
    padding = bytes([padding_length] * padding_length)
    return data.encode() + padding


def dump(file, data):
    print(f'Dumping data to file: {file}')
    with open(file, 'w') as f:
        f.write(str(data).replace('\'', '"').replace('True', 'true').replace('False', 'false'))


def encrypt(file, data, password) -> bool:
    print(f'Encrypting file: {file}, data: {data}, password: {password}')
    with open(file, 'rb') as f_og:
        with open(file + '.bak', 'wb') as f:
            f.write(f_og.read())

    data = str(data).replace('\'', '"').replace('True', 'true').replace('False', 'false')

    iv = os.urandom(16)
    print(f'IV: {iv}')

    key = hashlib.pbkdf2_hmac('sha1', bytes(password, 'utf-8'), iv, 100, 16)
    cipher = AES.new(key, AES.MODE_CBC, iv)

    encrypted_data = iv + cipher.encrypt(pad(data, AES.block_size))

    try:
        with open(file, 'wb') as f:
            f.write(encrypted_data)
    except Exception as e:
        print(f'Error encrypting file. Restoring backup...\nError: {e.with_traceback(e.__traceback__)}')
        with open(file + '.bak', 'rb') as f_og:
            with open(file, 'wb') as f:
                f.write(f_og.read())
        return False
    return True


def decrypt(file, password) -> dict | None:
    print(f'Decrypting file: {file}, password: {password}')
    with open(file, 'rb') as f:
        data = f.read()
    iv = data[:16]
    print(f'IV: {iv}')

    key = hashlib.pbkdf2_hmac('sha1', bytes(password, 'utf-8'), iv, 100, 16)
    cipher = AES.new(key, AES.MODE_CBC, iv)

    try:
        decrypted_data = cipher.decrypt(data[16:]).decode()
    except Exception as e:
        print(f'Error decrypting file. Wrong password? Password {password}\nError: {e.with_traceback(e.__traceback__)}')
        return None

    while decrypted_data[-1] != '}':
        decrypted_data = decrypted_data[:-1]

    return demjson3.decode(decrypted_data)
