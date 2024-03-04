from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
import os
import secrets
import base64









def open_database(name):
    password = input("Enter the encryption password: ")

    path = f"{name}.pwd"

    # Encrypt the file with the password
    data = decrypt_file_with_password(password, path)

    return data

def create_database(name):
    salt = generate_salt()
    password = input("Enter the encryption password: ")

    key = derive_key_from_password(password, salt)
    test = b'''{
"facebook":{
"username":"",
"password":"",
"description":""
},
"twitter":{
    "username":"",
    "password":"",
    "description":""
    }}'''
    cipher_suite = Fernet(key)
    encrypted_data = cipher_suite.encrypt(test)

    with open(f"{name}.pwd", 'wb') as file:
        file.write(salt + encrypted_data)



def generate_salt():
    return secrets.token_bytes(16)


def derive_key_from_password(password, salt, iterations=100000):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        salt=salt,
        iterations=iterations,
        length=32,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key




def decrypt_file_with_password(password, input_file):
    with open(input_file, 'rb') as file:
        data = file.read()

    # Extract the salt from the first 16 bytes of the data
    salt = data[:16]
    encrypted_data = data[16:]

    key = derive_key_from_password(password, salt)

    cipher_suite = Fernet(key)
    decrypted_data = cipher_suite.decrypt(encrypted_data)

    return decrypted_data


def encrypt_file_with_password(password, input_file, output_file):
    salt = generate_salt()
    key = derive_key_from_password(password, salt)

    with open(input_file, 'rb') as file:
        data = file.read()

    cipher_suite = Fernet(key)
    encrypted_data = cipher_suite.encrypt(data)

    with open(output_file, 'wb') as file:
        file.write(salt + encrypted_data)
