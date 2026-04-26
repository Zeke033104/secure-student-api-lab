import os
from cryptography.fernet import Fernet

KEY_FILE = os.path.join(os.path.dirname(__file__), "fernet.key")

def get_or_create_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            return f.read() 
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)
        return key
                        
                        
cipher_suite = Fernet(get_or_create_key())

def encrypt(value: str) -> str:
    return cipher_suite.encrypt(value.encode()).decode()
"""encrypt as a plaintext string and return a base64-encoded string"""

def decrypt(value: str) -> str:
    return cipher_suite.decrypt(value.encode()).decode()
"""decrypt a cipher text string and return the original plaintext string"""