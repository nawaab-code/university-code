# Part A, Question 6: Exception-Safe Secure Logging

## Question

Build a C++ logging class that writes timestamped, severity-labelled entries to a file in append mode. The class must fail immediately if the log file cannot be opened, reject empty messages with an exception, and release the file handle automatically on destruction. Demonstrate logging at multiple severity levels and empty-message rejection.

## Brief Explanation

`Logger` opens a file in append mode, writes timestamped INFO/WARNING/ERROR entries, rejects empty messages, and lets `std::ofstream` close the file automatically.

## Extensive Explanation

### Remember the flow

**Open → validate message → write and flush → close by destructor.** No manual `close()` is needed.

### Walkthrough

1. The constructor opens `app.log` with `std::ios::app`, so each run adds entries rather than replacing earlier ones. It throws immediately if opening fails.
2. `log` rejects an empty message with `std::invalid_argument` before writing anything.
3. `std::time` obtains the current time; `std::put_time` formats it. The severity string and message are added to the same line.
4. `flush()` sends buffered output to the file. The stream is checked afterward so a detected write failure becomes an exception.
5. The program writes at three severity levels and catches the deliberate empty-message attempt.

### Example entry

```text
2026-10-18 12:34:56 [WARNING] Failed login
```

The timestamp shown here is only an example; real output uses the local time when you run it.

### Limits and viva points

- The `std::ofstream` member closes in its destructor, including when an exception leaves the scope.
- Avoid logging passwords or tokens in a real application. The demonstration messages are fixed and contain no secrets.
- The label is a simple string to keep the classroom code short; a larger system could restrict it with an enum.

## How to Operate/Run the Files

```sh
g++ -std=c++17 -Wall -Wextra -pedantic main.cpp -o main
./main
cat app.log
```

Run from this folder. Each run appends three lines to `app.log`; the empty message is rejected.
