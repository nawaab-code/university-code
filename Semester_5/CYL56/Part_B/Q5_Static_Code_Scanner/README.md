# Part B, Question 5: Static Code Vulnerability Scanner

## Question

Implement a Python tool that scans source code line-by-line using pattern matching to detect common security vulnerabilities such as dangerous function calls, hardcoded credentials, and insecure URLs. Report each finding with its line number and severity level, sorted by priority.

## Brief Explanation

Four regular-expression rules flag `eval`/`exec`, shell execution, quoted hardcoded credentials, and `http://` URLs. Findings show severity and line number.

## Extensive Explanation

- The scanner reads each line and applies every rule, so one line can produce multiple findings. HIGH findings appear before MEDIUM findings; line number breaks ties.
- The sample is stored as plain text so its unsafe examples are never run. You can pass another source file as an argument.
- Regex scanning is easy to learn but cannot understand code structure. It can flag comments or strings and miss equivalent code written differently. Review each finding before acting on it; a production scanner would use a parser and data-flow analysis.

## How to Operate/Run the Files

```sh
python3 main.py
python3 main.py /path/to/source.py
```

The first command scans `sample_source.txt` and demonstrates all requested categories.
