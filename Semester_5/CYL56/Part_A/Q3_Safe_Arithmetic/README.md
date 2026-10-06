# Part A, Question 3: Safe Arithmetic and Integer Overflow Detection

## Question

Implement a C++ program that implements safe addition and multiplication operations which detect integer overflow before performing the calculation. Throw an appropriate exception if overflow would occur. Demonstrate correct results for normal inputs and exception handling for overflow cases.

## Brief Explanation

`safe_add` and `safe_multiply` check signed `int` boundaries before doing arithmetic. Both throw `std::overflow_error` when a result would be outside the supported range.

## Extensive Explanation

- Addition compares `a` with `INT_MAX - b` when `b` is positive and with `INT_MIN - b` when `b` is negative. These subtractions are safe in their respective branches.
- Multiplication divides a boundary by a nonzero operand before multiplying. Branching on operand signs handles positive and negative overflow, including `INT_MIN * -1`.
- Signed overflow in C++ is undefined behavior, so checking after multiplication is too late. The demonstration includes ordinary operations and boundary cases.

## How to Operate/Run the Files

```sh
g++ -std=c++17 -Wall -Wextra -pedantic main.cpp -o main
./main
```

The program prints results for safe operations and messages for rejected overflow cases.
