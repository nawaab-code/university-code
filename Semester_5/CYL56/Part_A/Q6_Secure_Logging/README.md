# Part A, Question 6: Exception-Safe Secure Logging

## Question

Build a C++ logging class that writes timestamped, severity-labelled entries to a file in append mode. The class must fail immediately if the log file cannot be opened, reject empty messages with an exception, and release the file handle automatically on destruction. Demonstrate logging at multiple severity levels and empty-message rejection.

## Brief Explanation

`Logger` opens `app.log` in append mode, writes INFO, WARNING, and ERROR entries, and throws for an empty message. The `std::ofstream` member closes automatically.

## Extensive Explanation

- The constructor checks that the stream opened, so callers cannot use an unusable logger.
- Each entry includes a local timestamp and severity label. The stream is flushed and checked after every write, exposing write errors promptly.
- The destructor of `std::ofstream` closes the file even when another operation throws. No explicit close is required.
- Avoid putting secrets in log messages in real applications; this demo uses fixed, non-sensitive messages.

## How to Operate/Run the Files

```sh
g++ -std=c++17 -Wall -Wextra -pedantic main.cpp -o main
./main
cat app.log
```

Run from this folder. Repeated runs append three more entries to `app.log`.
