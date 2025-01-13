import os

import pytest
import base64
from donationbox.utils.encryption import encrypt, decrypt, generate_key, get_encryption_key, store_json_encrypted, \
    load_json_encrypted
from donationbox.utils import settings


@pytest.fixture
def encryption_key():
    key = generate_key(32)
    return key


def testGenerateKey(monkeypatch):
    key = generate_key(32)
    assert key is not None
    assert isinstance(key, bytes)
    assert len(key) == 32


def test_get_encryption_key_valid(monkeypatch, encryption_key):
    settings.encryption_key = base64.b64encode(encryption_key).decode()
    key = get_encryption_key()
    assert key == encryption_key


def test_get_encryption_key_none(monkeypatch):
    settings.encryption_key = None
    with pytest.raises(AssertionError):
        get_encryption_key()


def test_get_encryption_key_invalid_length(monkeypatch):
    settings.encryption_key = base64.b64encode(generate_key(21)).decode()
    with pytest.raises(AssertionError):
        get_encryption_key()


def test_get_encryption_key_invalid_format(monkeypatch):
    settings.encryption_key = "12345"
    with pytest.raises(ValueError):
        get_encryption_key()


def test_encrypt_decrypt(monkeypatch, encryption_key):
    original_data = b"Secret message for testing."
    encrypted_data = encrypt(original_data, encryption_key)
    decrypted_data = decrypt(encrypted_data, encryption_key)
    assert original_data == decrypted_data
    assert original_data != encrypted_data
    assert decrypted_data != encrypted_data


def test_encrypt_invalid_key(monkeypatch):
    print("Test encrypting with invalid key")
    with pytest.raises(ValueError):
        encrypt(b"Secret message for testing.", b"12345")


def test_decrypt_invalid_key(monkeypatch):
    print("Test encrypting with invalid key")
    with pytest.raises(ValueError):
        decrypt(b"Encrypted message", b"12345")


def test_store_load_data(monkeypatch):
    data = {"key": "value"}
    filename = "test.json"
    store_json_encrypted(data, filename)
    loaded_data = load_json_encrypted(filename)
    assert data == loaded_data
    os.remove(filename)


def test_store_data_invalid(monkeypatch):
    data = {"key": "value"}
    filename = ""
    with pytest.raises(FileNotFoundError):
        store_json_encrypted(data, filename)


def test_load_data_invalid(monkeypatch):
    filename = ""
    with pytest.raises(FileNotFoundError):
        load_json_encrypted(filename)