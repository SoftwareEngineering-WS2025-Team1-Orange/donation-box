import json
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64
import secrets
from typing import Any, Dict
from .settings import settings


def generate_key(key_length: int = 32) -> bytes:
    return secrets.token_bytes(key_length)


def get_encryption_key() -> bytes:
    encryption_key = settings.encryption_key
    assert encryption_key is not None, "No environment variable ENCRYPTION_KEY found"

    try:
        key = base64.b64decode(encryption_key)
        assert len(key) in [16, 24, 32], "Key length must be 16, 24, or 32 bytes for AES."
        return key
    except (TypeError, ValueError):
        raise ValueError("Invalid value of environment variable ENCRYPTION_KEY")


def encrypt(data: bytes, key: bytes = get_encryption_key()) -> bytes:
    iv = os.urandom(12)
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(data) + encryptor.finalize()
    tag = encryptor.tag
    return base64.b64encode(iv + ciphertext + tag)


def decrypt(encrypted_data: bytes, key: bytes = get_encryption_key()) -> bytes:
    encrypted_data = base64.b64decode(encrypted_data)
    iv = encrypted_data[:12]
    ciphertext = encrypted_data[12:-16]
    tag = encrypted_data[-16:]

    cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()

    return decrypted_data


def store_json_encrypted(data: Dict[str, Any], filename: str) -> None:
    json_data = json.dumps(data).encode()
    encrypted_data = encrypt(json_data)
    with open(filename, 'wb') as f:
        f.write(encrypted_data)


def load_json_encrypted(filename: str) -> Dict[str, Any]:
    with open(filename, 'rb') as f:
        encrypted_data = f.read()
    decrypted_data = decrypt(encrypted_data)
    return json.loads(decrypted_data.decode())
