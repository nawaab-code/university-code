# Part B, Question 3: Secure Password Manager with Hashing and Strength Checking

## Question

Develop a Python program that generates a cryptographically secure random password, evaluates it against strength criteria, hashes it with a random salt using SHA-256, and verifies both a correct and an incorrect password against the stored hash.

## Brief Explanation

The program uses `secrets` to make a password and salt, checks length and character classes, hashes `salt + password` with SHA-256, and verifies with a constant-time comparison.

## Extensive Explanation

- `secrets.choice` draws characters from the operating system's cryptographic random source. Generation repeats until all strength checks pass.
- The checks require at least 12 characters and lowercase, uppercase, digit, and punctuation characters. These checks demonstrate a common classroom policy; password length and unpredictability matter most.
- A fresh 16-byte salt ensures that equal passwords do not automatically have equal hashes. Verification recomputes the digest and uses `hmac.compare_digest`.
- The question specifically asks for salted SHA-256. For a real password store, use a deliberately slow password hashing method such as Argon2, scrypt, or PBKDF2 instead. This demo prints the generated password only to show verification; do not log real passwords.

## How to Operate/Run the Files

```sh
python3 main.py
```

Each run generates a different password and salt, then prints `True` for the correct password and `False` for the incorrect one.
