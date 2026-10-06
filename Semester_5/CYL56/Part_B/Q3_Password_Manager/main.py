"""Demonstrate random passwords, strength checks, salted SHA-256 and verification."""
import hashlib
import hmac
import secrets
import string

ALPHABET = string.ascii_letters + string.digits + "!@#$%^&*"


def generate(length=20):
    if length < 12:
        raise ValueError("length must be at least 12")
    while True:
        candidate = "".join(secrets.choice(ALPHABET) for _ in range(length))
        if strength(candidate)[0]:
            return candidate


def strength(password):
    checks = {
        "at least 12 characters": len(password) >= 12,
        "lowercase": any(c.islower() for c in password),
        "uppercase": any(c.isupper() for c in password),
        "digit": any(c.isdigit() for c in password),
        "symbol": any(c in string.punctuation for c in password),
    }
    return all(checks.values()), checks


def hash_password(password):
    salt = secrets.token_bytes(16)
    digest = hashlib.sha256(salt + password.encode("utf-8")).digest()
    return salt.hex(), digest.hex()


def verify(password, salt_hex, digest_hex):
    candidate = hashlib.sha256(bytes.fromhex(salt_hex) + password.encode("utf-8")).digest()
    return hmac.compare_digest(candidate, bytes.fromhex(digest_hex))


def main():
    password = generate()
    strong, checks = strength(password)
    salt, digest = hash_password(password)
    print("Generated password:", password)  # Display only for this classroom demonstration.
    print("Strength:", "STRONG" if strong else "WEAK", checks)
    print("Salt:", salt)
    print("SHA-256 hash:", digest)
    print("Correct password:", verify(password, salt, digest))
    print("Incorrect password:", verify("wrong-password", salt, digest))


if __name__ == "__main__":
    main()
