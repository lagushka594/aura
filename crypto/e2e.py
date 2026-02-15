"""
E2E handled on client.
Server only stores ciphertext + encrypted AES key.
This file exists for validation / future extensions.
"""

def validate_payload(data):
    required = ["ciphertext", "encrypted_key", "iv"]
    return all(k in data for k in required)
