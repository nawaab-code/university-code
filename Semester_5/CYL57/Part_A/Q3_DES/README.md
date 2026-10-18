# DES encryption and decryption

## 1. Question

Develop a Java program to implement DES Algorithm. Simulate DES encryption and decryption using Java's security libraries or custom logic.

## 2. Brief explanation

Generate a DES key, encrypt a message with Java's crypto library, then decrypt with the same key and initialization vector (IV). Base64 makes binary output printable. DES is obsolete; this is a syllabus demonstration.

## 3. Extensive explanation

### What DES does

DES is a symmetric block cipher: the same secret key encrypts and decrypts. Its block size is 64 bits (8 bytes), and its effective key size is 56 bits. Eight additional key bits are parity bits. Internally DES uses 16 Feistel rounds, expanding and mixing the right half with a round key, applying S-box substitutions, and swapping halves. Java's provider implements those steps for us, as permitted by the question.

### Why specify DES/CBC/PKCS5Padding?

- `DES` selects the block cipher.
- `CBC` combines each plaintext block with the preceding ciphertext block before encryption. The first block uses an IV instead.
- `PKCS5Padding` fills an incomplete 8-byte block. If the text is already a multiple of 8 bytes, a whole padding block is added.
- A fresh, unpredictable IV prevents identical initial plaintext blocks from always producing identical initial ciphertext under one key.

### Understanding the code

1. Read the full message using `Scanner`.
2. Ask `KeyGenerator` for DES and initialize it with 56 effective bits. Generate a random secret key.
3. Request the complete transformation string from `Cipher` instead of relying on provider defaults.
4. Initialize in encryption mode. The provider creates a random IV, retrieved with `getIV()`.
5. Convert text to UTF-8 bytes and encrypt with `doFinal`. This also adds padding.
6. Print the IV and ciphertext as Base64. Base64 is an encoding, not encryption.
7. Initialize the cipher in decryption mode using the same key and `IvParameterSpec(iv)`.
8. Decrypt with `doFinal`, which also removes padding, and decode UTF-8.

### Imports and objects

`KeyGenerator` creates the key; `SecretKey` holds it; `Cipher` performs the cryptographic operation; `IvParameterSpec` passes the original IV back for decryption. `StandardCharsets.UTF_8` fixes text encoding; `Base64` displays binary data.

### Expected behavior and limits

A message such as `Hello DES` must appear unchanged on the `Decrypted:` line. The IV and ciphertext change between executions because the key and IV are random. Empty messages and multi-block messages also work.

The key remains in memory for this single run and is not printed or saved. To decrypt in a separate run, one would need to store and reload the key, IV, and ciphertext. An IV is not secret, but the key is.

### Remember for the viva

DES's 56-bit key is too small against exhaustive search. CBC also provides no message authentication: successful decryption alone does not establish integrity. Use authenticated modern encryption such as AES-GCM for new systems. This program demonstrates DES because the syllabus explicitly requires it.

## 4. How to operate/run the files

Requires a JDK (Java 11 or later); no external Java libraries. Open a terminal in this question's folder:

```bash
javac DESCipher.java
java DESCipher
```

Enter these lines when prompted:

```text
Hello DES
```

The output includes:

```text
Decrypted: Hello DES
```

The IV, public key where applicable, and ciphertext are generated at runtime; their exact values vary.

`DESCipher.java` contains the complete solution; compilation creates a `DESCipher.class` file. To remove compiled files, run `rm -f *.class` from this folder.

## Reference

[Oracle Java Cryptography Architecture guide](https://docs.oracle.com/en/java/javase/25/security/java-cryptography-architecture-jca-reference-guide.html) describes the standard crypto classes used in Part A. The examples here target Java 11+ APIs.
