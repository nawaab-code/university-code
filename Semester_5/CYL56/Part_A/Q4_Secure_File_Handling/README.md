# Part A, Question 4: Secure File Handling with Path Traversal Prevention

## Question

Implement a C++ file handling module that validates file paths before performing any read or write operation. Reject paths containing directory traversal sequences or sensitive system directories. Demonstrate successful file operations on a safe path and rejection of a malicious traversal path.

## Brief Explanation

`SafeFiles` confines operations to a local `safe_data` directory. It rejects absolute paths, `.` and `..` components, and symlinks in an existing target path.

## Extensive Explanation

- Rejecting absolute paths prevents direct access to paths such as `/etc/passwd`. Rejecting `..` prevents escaping the assigned directory by traversal.
- Each existing path component is checked for symbolic links, which could otherwise redirect access outside the directory.
- The demo writes and reads `safe_data/note.txt`, then rejects `../secret.txt` and `/etc/passwd`.
- The program is a teaching example for a single-user directory. A concurrent attacker who can replace path components between validation and opening could still exploit a race. A hardened Unix service should use directory handles with `openat`/`O_NOFOLLOW` and controlled directory permissions.

## How to Operate/Run the Files

```sh
g++ -std=c++17 -Wall -Wextra -pedantic main.cpp -o main
./main
```

Run from this folder. The program creates `safe_data/note.txt` here.
