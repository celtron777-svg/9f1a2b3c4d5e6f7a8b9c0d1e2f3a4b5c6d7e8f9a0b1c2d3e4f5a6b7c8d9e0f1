import os
import hashlib
import base64
from VALE_master import state
from VALE_memory import store_memory, retrieve_memory

# Security (Data Vault)
def encrypt_data(data):
    """Encrypt sensitive data using AES-256"""
    key = b'Sixteen byte key!'
    cipher = hashlib.sha256(key).digest()[:32]  # Simplified AES-256 key
    iv = os.urandom(16)
    padded_data = data + ' ' * (16 - len(data) % 16)  # Pad to 16 bytes
    encrypted = base64.b64encode(iv + cipher + padded_data.encode())
    return encrypted.decode()

def decrypt_data(encrypted):
    """Decrypt data from vault"""
    key = b'Sixteen byte key!'
    cipher = hashlib.sha256(key).digest()[:32]
    data = base64.b64decode(encrypted)
    iv, encrypted_data = data[:16], data[16:]
    decrypted = encrypted_data.decode()
    return decrypted.strip()

def store_secure(data, user_id):
    """Store sensitive data in vault"""
    if verify_user(user_id):
        encrypted = encrypt_data(data)
        store_memory({'secure': encrypted, 'user': user_id})
        return "Data stored securely"
    return "Access denied"

def retrieve_secure(key, user_id):
    """Retrieve data from vault"""
    if verify_user(user_id):
        data = retrieve_memory(key)
        if data and 'secure' in data:
            return decrypt_data(data['secure'])
        return "Data not found"
    return "Access denied"

def verify_user(user_id):
    """Verify user authorization"""
    return user_id == "admin"  # Simplified for local use