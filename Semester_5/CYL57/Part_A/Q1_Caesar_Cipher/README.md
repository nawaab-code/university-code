# Caesar cipher

## 1. Question

Develop a Java program to implement Caesar Cipher, Perform encryption and decryption with a user-defined shift value.

## 2. Brief explanation

Move every English letter forward by the chosen shift. Move backward by the same amount to decrypt. Preserve case, spaces, digits, and punctuation.

For shift 3, `A -> D`, `Z -> C`, and `Hello -> Khoor`.

## 3. Extensive explanation

### Algorithm and formula

Think of letters as numbers from 0 to 25: A is 0, B is 1, and Z is 25.

- Encryption: `encrypted = (letter + shift) mod 26`.
- Decryption: `original = (encrypted - shift) mod 26`.
- Modulo wraps values around the alphabet. Moving three places after Z reaches C.

### Understanding the code

1. `Scanner` reads a whole message, including spaces, and then an integer shift.
2. `Math.floorMod(key, 26)` makes negative or large shifts equivalent to a number from 0 to 25. For example, -1 becomes 25 and 29 becomes 3. Normalizing before arithmetic also avoids overflow with extreme integer shifts.
3. `shift` walks through the characters. `base` is uppercase A or lowercase a, so case is preserved.
4. The range check restricts the substitution to English A-Z and a-z. Other characters are appended unchanged.
5. `c - base` converts a character to its zero-based position. Add the key, take `% 26`, then add `base` to convert back to a character.
6. `StringBuilder` collects the output without repeatedly rebuilding the whole string.
7. Call the same function with the negative normalized key to recover the original message.

### Worked example

`Attack at dawn!`, shift `3`:

| Step | Value |
| --- | --- |
| A is position 0 | (0 + 3) % 26 = 3 -> D |
| t is position 19 | (19 + 3) % 26 = 22 -> w |
| Encrypted message | `Dwwdfn dw gdzq!` |
| Decrypted message | `Attack at dawn!` |

### Remember for the viva

- This is a monoalphabetic substitution cipher with only 26 distinct shifts, including the unchanged shift 0.
- Brute force tries every shift; frequency analysis also breaks it easily.
- Time is O(n), output space is O(n).
- Input must be an integer in Java's `int` range. This program intentionally leaves non-English characters unchanged.

## 4. How to operate/run the files

Requires a JDK (Java 11 or later); no external Java libraries. Open a terminal in this question's folder:

```bash
javac CaesarCipher.java
java CaesarCipher
```

Enter these lines when prompted:

```text
Attack at dawn!
3
```

The output includes:

```text
Encrypted: Dwwdfn dw gdzq!
Decrypted: Attack at dawn!
```

The output is deterministic for the same inputs.

`CaesarCipher.java` contains the complete solution; compilation creates a `CaesarCipher.class` file. To remove compiled files, run `rm -f *.class` from this folder.

## Reference

[Oracle Java Cryptography Architecture guide](https://docs.oracle.com/en/java/javase/25/security/java-cryptography-architecture-jca-reference-guide.html) describes the standard crypto classes used in Part A. The examples here target Java 11+ APIs.
