# Part A, Question 5: Memory Safety using RAII and Smart Pointers

## Question

Design a C++ class that manages a dynamically allocated integer array using RAII and smart pointers. Implement bounds-checked access that throws an exception for invalid indices and demonstrate that memory is released automatically when the object goes out of scope, without any explicit delete.

## Brief Explanation

`IntegerArray` owns an array through `std::unique_ptr<int[]>`. Its `at()` method checks the index and throws `std::out_of_range` if invalid.

## Extensive Explanation

- `std::make_unique<int[]>(size)` allocates the array and transfers ownership to the class member. The smart pointer frees the array when the `IntegerArray` object leaves scope, including during exception unwinding.
- Both mutable and const `at()` overloads enforce bounds. An index equal to the array size is invalid.
- The demo writes valid elements, catches an invalid index, and then exits a nested scope. No manual `delete` is present.

## How to Operate/Run the Files

```sh
g++ -std=c++17 -Wall -Wextra -pedantic main.cpp -o main
./main
```
