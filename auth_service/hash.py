from base64 import urlsafe_b64encode, urlsafe_b64decode

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def hash_data(
    data: bytes = b"password", salt: bytes = b'email', iterations: int = 100000
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


def verify_password(input_password: str, stored_hash: str) -> bool:
    _, iterations, salt_b64, stored_key_b64 = stored_hash.split("$")
    salt = urlsafe_b64decode(salt_b64.encode())

    input_password_bytes = input_password.encode()
    generated_hash = hash_data(data=input_password_bytes, salt=salt, iterations=int(iterations))

    return generated_hash == stored_hash
