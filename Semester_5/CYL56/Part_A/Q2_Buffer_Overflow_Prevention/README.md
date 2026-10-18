# Part A, Question 2: Buffer Overflow Prevention using Encapsulation

## Question

Implement a C++ class that encapsulates a fixed-size character buffer and prevents buffer overflow by checking input length before writing. Throw an appropriate exception if the input exceeds buffer capacity. Demonstrate both safe storage and overflow detection.

## Brief Explanation

A class hides a 16-byte character array. It checks the input length before copying and throws `std::length_error` if the input cannot fit.

## Extensive Explanation

### Remember the flow

**Capacity → check → copy.** The array has 16 bytes, but one byte is reserved for the NUL terminator. Therefore the maximum stored text length is 15 bytes.

### Walkthrough

1. `data` is private. Callers must use `store`; they cannot write into the array directly through this interface.
2. `text.size() >= sizeof(data)` rejects lengths 16 and above. A length of 15 is permitted because the terminator takes byte 16.
3. `std::memcpy` copies `text.size() + 1` bytes, including the terminating `\0`. It runs only after the size check.
4. The first example fits and prints the stored value. The second exceeds capacity and is caught as `std::length_error`.

### Boundary table

| Input bytes | Needed bytes including `\0` | Result |
| ---: | ---: | --- |
| 0 | 1 | Accepted |
| 15 | 16 | Accepted |
| 16 | 17 | Rejected |

### Limits and viva points

- This protects writes made through `store`. Encapsulation makes the check unavoidable for class users.
- `std::string::size()` counts bytes. A Unicode character may use multiple UTF-8 bytes, so the 15-byte limit is not always 15 visible characters.
- The old value remains intact on a rejected write because the check happens before `memcpy`.

## How to Operate/Run the Files

```sh
g++ -std=c++17 -Wall -Wextra -pedantic main.cpp -o main
./main
```

Run from this folder. Expected behavior: `safe input` is stored and the longer string is rejected.
