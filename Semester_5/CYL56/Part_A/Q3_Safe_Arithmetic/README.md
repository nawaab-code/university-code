# Part A, Question 3: Safe Arithmetic and Integer Overflow Detection

## Question

Implement a C++ program that implements safe addition and multiplication operations which detect integer overflow before performing the calculation. Throw an appropriate exception if overflow would occur. Demonstrate correct results for normal inputs and exception handling for overflow cases.

## Brief Explanation

`safe_add` and `safe_multiply` check whether a signed `int` result would exceed its limits, then either calculate it or throw `std::overflow_error`.

## Extensive Explanation

### Remember the flow

**Check bounds first; calculate second.** An overflowed signed calculation cannot be repaired by inspecting its result afterward.

### Addition, step by step

1. If `b` is positive, adding it can exceed `INT_MAX`. The test is `a > INT_MAX - b`.
2. If `b` is negative, adding it can go below `INT_MIN`. The test is `a < INT_MIN - b`.
3. Only if neither condition holds does the function return `a + b`.

### Multiplication, step by step

Multiplication has four sign combinations. The function checks an appropriate limit by division before doing `a * b`. Division is used because computing the product to test it could already overflow. The `a < 0, b < 0` branch also catches the special `INT_MIN * -1` case.

| Calculation | Outcome |
| --- | --- |
| `20 + 22` | `42` |
| `INT_MAX + 1` | Exception |
| `6 * 7` | `42` |
| `INT_MIN * -1` | Exception |

### Limits and viva points

- `std::numeric_limits<int>::max()` and `min()` use the platform's actual `int` bounds.
- Signed overflow is undefined behavior in C++; “calculate, then compare” is not safe.
- The checks are kept explicit rather than hidden in a compiler-specific intrinsic so the logic is visible during a viva.

## How to Operate/Run the Files

```sh
g++ -std=c++17 -Wall -Wextra -pedantic main.cpp -o main
./main
```

The program prints safe answers and catches the deliberate overflow examples.
