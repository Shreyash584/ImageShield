import secrets
import string
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from hashlib import sha256

BLOCK = 16  # AES block size

def generate_key_16chars() -> str:
    # URL-safe readable characters; 16 ASCII chars = 16 bytes in UTF-8
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(16))

def aes_encrypt_with_hash(data: bytes, key_str: str) -> bytes:
    """
    Encrypts data with AES-CBC using a 16-char key (UTF-8 bytes).
    Appends SHA-256 hex digest (64 ASCII bytes) to the end of the output.
    Output layout: IV(16) + CIPHERTEXT(?) + HASH_HEX(64 ASCII)
    """
    key = key_str.encode('utf-8')  # 16 bytes
    iv = secrets.token_bytes(16)
    h = sha256(data).hexdigest().encode('ascii')  # 64 bytes ASCII

    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    ct = cipher.encrypt(pad(data, BLOCK))
    return iv + ct + h

def aes_decrypt_verify(blob: bytes, key_str: str) -> bytes:
    """
    Reverses the above:
    - Split HASH (last 64 bytes ASCII)
    - Split IV (first 16 bytes)
    - Decrypt the middle as ciphertext
    - Verify SHA-256
    Returns the original plaintext bytes if verification passes,
    raises ValueError if verification fails.
    """
    if len(blob) < 16 + 64:
        raise ValueError("Encrypted file too short or corrupted.")

    h_ascii = blob[-64:]
    try:
        expected_hex = h_ascii.decode('ascii')
    except UnicodeDecodeError:
        raise ValueError("Hash footer corrupted.")

    iv = blob[:16]
    ct = blob[16:-64]
    key = key_str.encode('utf-8')

    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    try:
        pt = unpad(cipher.decrypt(ct), BLOCK)
    except ValueError:
        # wrong key or corrupted ciphertext/padding
        raise ValueError("Decryption failed (bad key or corrupted data).")

    actual_hex = sha256(pt).hexdigest()
    if actual_hex != expected_hex:
        raise ValueError("Integrity check failed (SHA-256 mismatch).")

    return pt
