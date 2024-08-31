import os
from base64 import urlsafe_b64encode

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def hash_data(
    data: bytes = b"password", salt: bytes = os.urandom(16), iterations: int = 100000
) -> str:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
        backend=default_backend(),
    )
    key = kdf.derive(data)
    combined = f"pbkdf2_sha256${iterations}${urlsafe_b64encode(salt).decode()}${urlsafe_b64encode(key).decode()}"

    return combined
