# Part B, Question 5: Static Code Vulnerability Scanner

## Question

Implement a Python tool that scans source code line-by-line using pattern matching to detect common security vulnerabilities such as dangerous function calls, hardcoded credentials, and insecure URLs. Report each finding with its line number and severity level, sorted by priority.

## Brief Explanation

The scanner reads source text line by line and uses four regex rules to flag dangerous calls, hardcoded credentials, and insecure HTTP URLs.

## Extensive Explanation

### Remember the flow

**Line → apply every pattern → collect findings → sort by severity.** Multiple findings may be reported for one line.

### Walkthrough

1. The script loads `sample_source.txt` by default or a source file path supplied on the command line.
2. `enumerate(..., 1)` starts line numbers at 1, matching what an editor shows.
3. The rules match `eval`/`exec`, `os.system` or `shell=True`, quoted credential assignments, and `http://` URLs.
4. `re.I` makes matching case-insensitive. Each matching rule adds a severity, line number, and label.
5. Sorting places HIGH findings before MEDIUM findings; within a severity, earlier lines come first.

### Bundled example

| Sample line | Finding | Severity |
| --- | --- | --- |
| `password = "classroom-example"` | Hardcoded credential | HIGH |
| `result = eval(user_input)` | Dynamic code execution | HIGH |
| `os.system(command)` | Shell command execution | HIGH |
| `"http://example.invalid/api"` | Insecure URL | MEDIUM |

### Limits and viva points

- The sample is a `.txt` file so its intentionally unsafe lines are never run.
- Regex does not understand syntax or data flow. It may flag a comment or miss code written in a different form. Treat results as leads for review.
- Severity is a simple classroom priority; actual risk depends on how the code is used.

## How to Operate/Run the Files

```sh
python3 main.py
python3 main.py /path/to/source.py
```

The first command scans the bundled example. The second scans any text-based source file.
