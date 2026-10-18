# AES-128 encryption and decryption

## 1. Question

Write a Java program to implement AES Algorithm, use Java Cryptography Extension (JCE) to perform AES encryption and decryption with a 128-bit key.

## 2. Brief explanation

Generate a 128-bit AES key and use AES-GCM to encrypt and decrypt a message. GCM also authenticates the ciphertext, so changing the data or using the wrong key causes decryption to fail.

## 3. Extensive explanation

### What AES does

AES is a symmetric cipher with a 128-bit block size. AES-128 uses a 128-bit key and ten rounds. Its internal operations include SubBytes, ShiftRows, MixColumns, and AddRoundKey; the final round omits MixColumns. Java's JCE provider handles these details.

The block size stays 128 bits even when a different supported key size is chosen. This exercise explicitly uses a 128-bit key through `generator.init(128)`.

### Why AES/GCM/NoPadding?

GCM combines counter-mode encryption with an authentication tag. Counter mode handles partial blocks, so no block padding is necessary. The provider appends the authentication tag to the encrypted bytes returned by `doFinal`.

- The secret key protects the content.
- The IV, also called a nonce, must never repeat with the same key.
- The tag detects unauthorized modification and use of the wrong key or IV.
- The IV can be stored beside the ciphertext; it is not a password or secret key.

### Understanding the code

1. `Scanner` reads the message; UTF-8 converts it to bytes predictably.
2. `KeyGenerator.getInstance("AES")` and `init(128)` produce the required random key.
3. `Cipher.getInstance("AES/GCM/NoPadding")` selects both the algorithm and mode explicitly.
4. Encryption initialization lets the provider generate a fresh IV. `getIV()` retrieves it.
5. `doFinal` encrypts and adds the authentication tag. Base64 converts the output and IV into printable text.
6. `GCMParameterSpec(128, iv)` restores the original IV and selects a 128-bit **tag**, distinct from the 128-bit **key**.
7. Decryption verifies the tag before returning the original plaintext bytes. A failed check raises `AEADBadTagException` rather than returning trustworthy plaintext.

### Example and persistence

For input `Hello AES`, expect `Decrypted: Hello AES`. The encrypted line varies every run. A one-run example keeps its key in memory; the Base64 output alone is not enough to decrypt later. Persisting an encrypted message would require a securely managed key and the original IV, ciphertext, and tag.

### Remember for the viva

AES is symmetric, RSA is asymmetric. AES's block size and key size are separate ideas. GCM adds integrity to confidentiality. Base64 is just representation. Never reuse a GCM nonce with a key, and never replace key generation with a hard-coded classroom password. Empty and Unicode messages work because GCM accepts arbitrary byte lengths.

## 4. How to operate/run the files

Requires a JDK (Java 11 or later); no external Java libraries. Open a terminal in this question's folder:

```bash
javac AESCipher.java
java AESCipher
```

Enter these lines when prompted:

```text
Hello AES
```

The output includes:

```text
Decrypted: Hello AES
```

The IV, public key where applicable, and ciphertext are generated at runtime; their exact values vary.

`AESCipher.java` contains the complete solution; compilation creates a `AESCipher.class` file. To remove compiled files, run `rm -f *.class` from this folder.

## Reference

[Oracle Java Cryptography Architecture guide](https://docs.oracle.com/en/java/javase/25/security/java-cryptography-architecture-jca-reference-guide.html) describes the standard crypto classes used in Part A. The examples here target Java 11+ APIs.
