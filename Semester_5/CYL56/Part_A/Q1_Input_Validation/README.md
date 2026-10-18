# Part A, Question 1: Input Validation using Regular Expressions

## Question

Implement a C++ program to validate user inputs using regular expressions. Validate an email address against a standard pattern and an age value within the range 1–120. Test both valid and invalid inputs for each field and display appropriate YES/NO results.

## Brief Explanation

The program checks email shape with a regular expression and checks that an age is a whole number from 1 through 120. Built-in examples and typed input both produce YES or NO.

## Extensive Explanation

### Remember the flow

**Match → convert → range-check.** The email needs only a full regex match. The age must match digits before it is converted, then it must fall within the allowed range.

### Walkthrough

1. `email_ok` calls `std::regex_match`, which checks the *whole* input. The expression allows common characters before `@`, a domain, a dot, and a final alphabetic suffix of at least two letters.
2. `age_ok` first matches one to three digits. `std::stoi` therefore receives only short numeric text; it cannot be given `abc`, a sign, or a very long number.
3. The age is accepted only if `1 <= n <= 120`. Because of this separate range test, `0` and `121` are rejected even though they contain only digits.
4. The sample loops demonstrate valid and invalid cases. The final prompts let you try your own email and age.

### Worked examples

| Input | Check | Result | Reason |
| --- | --- | --- | --- |
| `alice@example.com` | Email | YES | Fits the classroom email pattern |
| `bad@@example.com` | Email | NO | Contains two `@` signs |
| `25` | Age | YES | Numeric and within range |
| `0` | Age | NO | Below the minimum |
| `abc` | Age | NO | Not numeric |

### Limits and viva points

- A regular expression checks syntax, not whether a mailbox exists. This short pattern is intentionally not a complete email standard parser.
- `regex_match` differs from `regex_search`: it requires the whole string to match. That is why extra text cannot be silently accepted.
- The age regex limits input length before conversion, avoiding an exception from trying to convert an enormous number.

## How to Operate/Run the Files

From this question folder:

```sh
g++ -std=c++17 -Wall -Wextra -pedantic main.cpp -o main
./main
```

Enter `alice@example.com` and `25` at the prompts. Then run it again with `bad@@example.com` and `121`. The program prints the built-in examples before the prompts.
