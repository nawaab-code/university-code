# RSA encryption and decryption

## 1. Question

Write a Java program to implement RSA Algorithm, generate public/private key pairs, encrypt a message with the public key, and decrypt using the private key.

## 2. Brief explanation

Generate a 2048-bit RSA key pair. Encrypt a short message with the public key using OAEP padding; decrypt it with the private key. Anyone may know the public key, but only the private-key holder should be able to decrypt.

## 3. Extensive explanation

### The mathematical idea

RSA starts with two large random primes p and q and forms `n = p*q`. A public exponent e and private exponent d are related through modular arithmetic. The simplified textbook operations are `c = m^e mod n` and `m = c^d mod n`. These raw formulas are not a safe message format: practical RSA encryption must use a padding scheme such as OAEP. Java generates the primes and keys internally.

### Understanding the code

1. Read a message and convert it to UTF-8 bytes. Check the byte count before encryption.
2. `KeyPairGenerator.getInstance("RSA")` and `initialize(2048)` generate a 2048-bit modulus and matching public/private keys.
3. `Cipher` selects RSA with OAEP using SHA-256.
4. `OAEPParameterSpec` explicitly selects SHA-256 for both OAEP's main digest and MGF1. This avoids relying on provider-specific MGF1 defaults. The label is the default empty value.
5. Initialize the cipher with `keys.getPublic()` and encrypt.
6. Print the public key using its X.509 SubjectPublicKeyInfo encoding, and print the ciphertext, both in Base64. The private key remains in memory.
7. Reinitialize with `keys.getPrivate()` and the same padding parameters, decrypt, then decode UTF-8.

### Why a 190-byte limit?

OAEP's maximum message length is `k - 2*hLen - 2`, where k is the modulus size in bytes and hLen is the digest length. Here `2048/8 - 2*32 - 2 = 190` bytes. A Unicode character may take several UTF-8 bytes, so 190 characters are not necessarily allowed. The program reports oversized input clearly instead of silently splitting it into RSA blocks.

Ciphertext is always one modulus long: 256 bytes for this key. Base64 adds display overhead. OAEP is randomized, so encrypting the same text does not always give the same ciphertext.

### Why does the transformation mention ECB?

`RSA/ECB/...` is Java's transformation naming convention. RSA does not operate in the symmetric ECB block mode; it encrypts a bounded message using the RSA operation and OAEP encoding.

### Example and real use

`Hello RSA` must return as `Decrypted: Hello RSA`. For a large file, encrypt the file with AES-GCM, then encrypt only the AES key with RSA-OAEP. That is hybrid encryption. The example generates a fresh key pair per run; its ciphertext cannot be recovered in a later run unless the matching private key is retained securely.

### Remember for the viva

Public key encrypts, private key decrypts for confidentiality. A digital signature is a different operation and should use a signature API, not a reversed version of this encryption program. RSA is slower and has a smaller message limit than AES. Never use unpadded textbook RSA.

## 4. How to operate/run the files

Requires a JDK (Java 11 or later); no external Java libraries. Open a terminal in this question's folder:

```bash
javac RSACipher.java
java RSACipher
```

Enter these lines when prompted:

```text
Hello RSA
```

The output includes:

```text
Decrypted: Hello RSA
```

The IV, public key where applicable, and ciphertext are generated at runtime; their exact values vary.

`RSACipher.java` contains the complete solution; compilation creates a `RSACipher.class` file. To remove compiled files, run `rm -f *.class` from this folder.

## Reference

[Oracle Java Cryptography Architecture guide](https://docs.oracle.com/en/java/javase/25/security/java-cryptography-architecture-jca-reference-guide.html) describes the standard crypto classes used in Part A. The examples here target Java 11+ APIs.
