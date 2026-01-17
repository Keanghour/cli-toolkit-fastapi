# cnb_cli/commands/encryption.py

from cryptography.fernet import Fernet, InvalidToken

def is_encrypted(value: str) -> bool:
    return value.startswith('gAAAAAB')

def decrypt_data(value: str, key: str):
    if not value or not key or not is_encrypted(value):
        return value

    try:
        cipher = Fernet(key.encode())
        decrypted_value = cipher.decrypt(value.encode())
        return decrypted_value.decode()
    except InvalidToken:
        # If decryption fails, return the original value
        return value

def encrypt_data(value: str, key: str):
    if not value or not key:
        return value

    cipher = Fernet(key.encode())
    encrypted_value = cipher.encrypt(value.encode())
    return encrypted_value.decode()
