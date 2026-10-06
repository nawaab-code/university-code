# Part A, Question 2: Buffer Overflow Prevention using Encapsulation

## Question

Implement a C++ class that encapsulates a fixed-size character buffer and prevents buffer overflow by checking input length before writing. Throw an appropriate exception if the input exceeds buffer capacity. Demonstrate both safe storage and overflow detection.

## Brief Explanation

`SafeBuffer` owns a 16-byte array. It accepts up to 15 text bytes, reserves one byte for the NUL terminator, and throws `std::length_error` when input is too long.

## Extensive Explanation

- The buffer is private, so callers cannot write past it directly through the class interface.
- `value.size() >= data_.size()` rejects any string that cannot fit along with its terminator. The `memcpy` runs only after this check and copies exactly `size + 1` bytes.
- The second built-in example triggers the exception. The previously stored value remains intact because validation occurs before writing.
- Capacity is measured in bytes, not Unicode characters; UTF-8 text may use several bytes per character.

## How to Operate/Run the Files

```sh
g++ -std=c++17 -Wall -Wextra -pedantic main.cpp -o main
./main
```

Run from this folder. The output shows one stored value and one rejected value.
