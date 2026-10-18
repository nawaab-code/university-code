# Playfair cipher

## 1. Question

Develop a Java program to implement Playfair Cipher, encrypt a given plaintext using 5x5 matrix.

## 2. Brief explanation

Build a 5 x 5 key square and encrypt letters in pairs. A pair in one row moves right; a pair in one column moves down; otherwise use the other corners of its rectangle. I and J share a cell.

## 3. Extensive explanation

### Building the square

1. Convert the key to uppercase English letters and replace J with I.
2. Keep each key letter only once, preserving its first appearance.
3. Append the remaining alphabet, omitting J. The resulting string has exactly 25 letters.
4. Display five letters per row. In the one-dimensional string, row is `index / 5` and column is `index % 5`.

For key `MONARCHY`:

```text
MONAR
CHYBD
EFGIK
LPQST
UVWXZ
```

### Preparing the message

`letters` removes spaces, digits, and punctuation, uppercases letters, and maps J to I. `prepare` reads pairs from left to right.

- If the next letter equals the first, insert X and consume only the first letter. The repeated letter starts the next pair.
- If the last letter is alone, add X.
- If the first letter itself is X, use Q as the filler, so a pair never becomes XX.
- Example: `BALLOON -> BA LX LO ON -> BALXLOON`.
- Example: `XX -> XQ XQ`. A one-letter `X` becomes `XQ`.

### Encrypting each pair

| Relationship | Rule | Example with MONARCHY |
| --- | --- | --- |
| Same row | Move both columns one cell right, wrapping at 5 | MO -> ON |
| Same column | Move both rows one cell down, wrapping at 5 | MC -> CE |
| Rectangle | Keep each row; swap the two columns | IN -> GA |

The code computes two positions, divides by 5 for rows and takes remainder 5 for columns. After applying one rule, `5 * row + column` locates each encrypted letter.

### Worked example

With key `MONARCHY`, plaintext `INSTRUMENTS` becomes `IN ST RU ME NT SX` after preparation. The ciphertext is `GATLMZCLRQXA`.

### Understanding the methods

- `letters`: normalize text. `Locale.ROOT` makes uppercasing independent of your computer's language setting.
- `square`: remove duplicate key letters and append unused letters.
- `prepare`: produce valid, even-length digraphs.
- `encrypt`: apply row, column, or rectangle rules to prepared pairs.
- `main`: read key and message, then print the matrix, prepared text, and ciphertext.

### Remember for the viva

This is a digraph substitution cipher. Decryption would move left/up for same-row/column pairs and reuse the rectangle rule. Recovering exact original formatting, distinguishing I from J, and automatically removing filler letters are ambiguous. The syllabus asks for encryption, so this program prints the prepared plaintext to make that transformation explicit. It is a historical cipher, unsuitable for protecting real data.

String concatenation keeps this small classroom program easy to reproduce; for very large inputs, use `StringBuilder`.

## 4. How to operate/run the files

Requires a JDK (Java 11 or later); no external Java libraries. Open a terminal in this question's folder:

```bash
javac PlayfairCipher.java
java PlayfairCipher
```

Enter these lines when prompted:

```text
MONARCHY
INSTRUMENTS
```

The output includes:

```text
Prepared: INSTRUMENTSX
Encrypted: GATLMZCLRQXA
```

The output is deterministic for the same inputs.

`PlayfairCipher.java` contains the complete solution; compilation creates a `PlayfairCipher.class` file. To remove compiled files, run `rm -f *.class` from this folder.

## Reference

[Oracle Java Cryptography Architecture guide](https://docs.oracle.com/en/java/javase/25/security/java-cryptography-architecture-jca-reference-guide.html) describes the standard crypto classes used in Part A. The examples here target Java 11+ APIs.
