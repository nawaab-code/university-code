# Part A, Question 1: Input Validation using Regular Expressions

## Question

Implement a C++ program to validate user inputs using regular expressions. Validate an email address against a standard pattern and an age value within the range 1–120. Test both valid and invalid inputs for each field and display appropriate YES/NO results.

## Brief Explanation

The program matches email syntax with a regular expression, checks that age contains only digits, then enforces the numeric age range. It prints YES or NO for built-in examples and user input.

## Extensive Explanation

- `std::regex_match` requires the entire email to match the pattern. The pattern allows common local-part characters, an `@`, a dotted domain, and a two-or-more-letter final domain label.
- Age must contain one to three ASCII digits. Only then is it converted with `std::stoi`; its value must be from 1 through 120 inclusive. This avoids accepting `-1`, whitespace, or words.
- The email pattern is a practical classroom validator. Complete standards-compliant email validation and proof that an address exists require more than one regular expression.

## How to Operate/Run the Files

From this folder:

```sh
g++ -std=c++17 -Wall -Wextra -pedantic main.cpp -o main
./main
```

Enter an email and an age when prompted. Try `alice@example.com` and `25`, then `bad@@example.com` and `121`.
