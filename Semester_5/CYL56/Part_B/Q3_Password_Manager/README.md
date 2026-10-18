# Part B, Question 3: Secure Password Manager with Hashing and Strength Checking

## Question

Develop a Python program that generates a cryptographically secure random password, evaluates it against strength criteria, hashes it with a random salt using SHA-256, and verifies both a correct and an incorrect password against the stored hash.

## Brief Explanation

The program generates a random password, checks its strength, salts and hashes it with SHA-256, then verifies a correct and an incorrect guess.

## Extensive Explanation

### Remember the flow

**Generate → check → salt and hash → recompute and compare.** The stored value is the salt plus hash, not the plaintext password.

### Walkthrough

1. `secrets.choice` selects each character using a cryptographically secure random source. The program repeats generation until `strong` returns `True`.
2. `strong` requires at least 12 characters and at least one lowercase, uppercase, digit, and punctuation character. The generated password has 20 characters.
3. `secrets.token_bytes(16)` creates a fresh 16-byte salt. The digest is `SHA256(salt || UTF-8 password)`.
4. To verify a guess, the program computes the same digest using the stored salt. `hmac.compare_digest` compares the two byte strings without an ordinary early-exit equality check.
5. The correct password prints `True`; the deliberately wrong guess prints `False`.

### Why use a salt?

Two users who choose the same password should not automatically have the same stored digest. A unique random salt changes the hash input for each record. The salt need not be secret, but it must be stored with the digest so verification can repeat the calculation.

### Limits and viva points

- Salted SHA-256 is included because the syllabus specifically asks for it. For actual password storage, use a slow password-hashing scheme such as Argon2, scrypt, or PBKDF2.
- The password is printed only for this demonstration. Real software must not print or log it.
- Character-class checks are one simple strength rule; unpredictability and sufficient length matter most.

## How to Operate/Run the Files

```sh
python3 main.py
```

Run it twice to see that both the password and salt change. The hash changes with them; verification still succeeds only for the correct password.
