# Part A, Question 5: Memory Safety using RAII and Smart Pointers

## Question

Design a C++ class that manages a dynamically allocated integer array using RAII and smart pointers. Implement bounds-checked access that throws an exception for invalid indices and demonstrate that memory is released automatically when the object goes out of scope, without any explicit delete.

## Brief Explanation

`IntegerArray` owns its allocation through `std::unique_ptr<int[]>`. Its `at` method checks bounds and throws `std::out_of_range` for an invalid index.

## Extensive Explanation

### Remember the flow

**Acquire in constructor → use through checked method → release at scope end.** That pattern is RAII (Resource Acquisition Is Initialization).

### Walkthrough

1. `std::make_unique<int[]>(n)` allocates an integer array and gives sole ownership to `data`.
2. `size` records the valid index range: `0` through `size - 1`.
3. `at(i)` rejects `i >= size` before accessing `data[i]`; otherwise it returns a reference, so it can be used on either side of an assignment.
4. The example writes to index `0`, then deliberately tries index `3` in a three-element array. Valid indices are only `0`, `1`, and `2`.
5. When the inner scope ends, `numbers` is destroyed and its `unique_ptr` frees the array. There is no explicit `delete`.

### Why RAII helps

Even if an exception occurs, C++ destroys local objects as the stack unwinds. Because the smart pointer owns the allocation, cleanup is attached to object lifetime rather than to a manually remembered cleanup line.

### Limits and viva points

- `std::unique_ptr` represents exclusive ownership; copying `IntegerArray` is therefore disabled automatically.
- The program prints a message after scope exit to show *when* automatic cleanup occurs. It does not measure memory usage.
- `std::vector<int>` is usually simpler for everyday code, but this exercise specifically asks for dynamic allocation with a smart pointer.

## How to Operate/Run the Files

```sh
g++ -std=c++17 -Wall -Wextra -pedantic main.cpp -o main
./main
```

Expect the stored first value, an invalid-index message, and an automatic-release message.
