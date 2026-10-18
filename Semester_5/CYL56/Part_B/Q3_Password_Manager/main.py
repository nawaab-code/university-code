import hashlib
import hmac
import secrets
import string

ALPHABET = string.ascii_letters + string.digits + "!@#$%^&*"


def strong(password):
    return (len(password) >= 12 and any(c.islower() for c in password)
            and any(c.isupper() for c in password)
            and any(c.isdigit() for c in password)
            and any(c in string.punctuation for c in password))


def generate():
    while True:
        password = "".join(secrets.choice(ALPHABET) for _ in range(20))
        if strong(password):
            return password


def digest(password, salt):
    return hashlib.sha256(salt + password.encode()).digest()


password = generate()
salt = secrets.token_bytes(16)
stored = digest(password, salt)
print("Generated password:", password)  # Classroom demo only.
print("Strong:", strong(password))
print("Salt:", salt.hex())
print("SHA-256 hash:", stored.hex())
print("Correct password:", hmac.compare_digest(digest(password, salt), stored))
print("Incorrect password:", hmac.compare_digest(digest("wrong", salt), stored))
