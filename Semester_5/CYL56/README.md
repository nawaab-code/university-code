# CYL56 Defensive Laboratory — Part A

C++17 solutions for the five Part A questions in the CYL56 syllabus.

| File | Question |
| --- | --- |
| `01_input_validation.cpp` | Email and age validation using regular expressions |
| `02_buffer_overflow_prevention.cpp` | Fixed-size buffer encapsulation and overflow prevention |
| `03_safe_arithmetic.cpp` | Integer addition and multiplication overflow detection |
| `04_secure_file_handling.cpp` | File handling with path traversal prevention |
| `05_raii_smart_pointers.cpp` | RAII, smart pointers, and bounds-checked array access |

## Compile and run

Compile all programs from this directory:

```bash
mkdir -p build
for source in 0*.cpp; do
    g++ -std=c++17 -Wall -Wextra -Wpedantic "$source" -o "build/${source%.cpp}"
done
```

Run any solution, for example:

```bash
./build/01_input_validation
```

Every program includes valid and invalid demonstrations required by its question.
Question 4 creates `safe_files/message.txt` under the current working directory;
this is demonstration output and is ignored by Git.
