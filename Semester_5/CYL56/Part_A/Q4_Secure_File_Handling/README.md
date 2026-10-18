# Part A, Question 4: Secure File Handling with Path Traversal Prevention

## Question

Implement a C++ file handling module that validates file paths before performing any read or write operation. Reject paths containing directory traversal sequences or sensitive system directories. Demonstrate successful file operations on a safe path and rejection of a malicious traversal path.

## Brief Explanation

`safe_path` permits only relative names within `safe_data`. It rejects absolute paths, `.`/`..` traversal components, and symbolic links before either demonstration file operation.

## Extensive Explanation

### Remember the flow

**Validate path → open file.** Every read or write obtains its path from `safe_path` first.

### Walkthrough

1. `root` is the only permitted storage directory. `main` creates it and rejects it if it is a symbolic link.
2. `safe_path` refuses empty or absolute names. `/etc/passwd` is absolute, so it cannot be used as a target.
3. It examines each relative path component. `..` could escape to the parent directory; `.` adds ambiguity. Both are rejected.
4. It rejects symbolic links encountered along the path because a link can redirect an apparently local path outside the safe directory.
5. The demo writes and reads `safe_data/note.txt`, then tries `../secret.txt` and `/etc/passwd`. Both attempted attacks are rejected before opening.

### Why the checks matter

| Input | Risk | Result |
| --- | --- | --- |
| `note.txt` | Local file | Allowed |
| `../secret.txt` | Parent-directory traversal | Rejected |
| `/etc/passwd` | Sensitive absolute path | Rejected |
| Symlink inside `safe_data` | Could redirect outside | Rejected |

### Limits and viva points

- This is a compact classroom example. File systems can change between the check and the open operation; an attacker with write access to the directory could exploit that race. A hardened Unix service uses directory handles and `openat` with `O_NOFOLLOW`.
- Keep the safe directory writable only by trusted users. A path check alone cannot replace file-system permissions.
- `safe_data/note.txt` is created as demonstration output and is ignored by Git.

## How to Operate/Run the Files

```sh
g++ -std=c++17 -Wall -Wextra -pedantic main.cpp -o main
./main
```

Run from this folder. The program creates `safe_data/note.txt`, displays its content, and prints two rejection messages.
