# Part B, Question 1: Secure Configuration File Auditor

## Question

Implement a Python program that creates a sample configuration file containing common security misconfigurations such as plaintext passwords, debug mode enabled, SSL disabled, and insecure file permissions. Audit the file and report all issues with severity labels sorted by priority, along with a remediation hint.

## Brief Explanation

The program builds a deliberately insecure sample configuration, checks its values and file permissions, and prints issues in severity order with a fix for each.

## Extensive Explanation

### Remember the flow

**Read settings → apply security checks → sort findings → print fixes.** The same `audit` function can inspect the built-in sample or a path supplied by the user.

### Walkthrough

1. The parser reads a simple `key=value` file. It splits at the first `=`, trims surrounding spaces, makes the key lowercase, and remembers the line number.
2. A nonempty `password`, `db_password`, or `api_key` is treated as a plaintext secret and marked CRITICAL. The remediation is to move secrets into a protected secret manager.
3. `debug=true` is flagged because debug output can expose internal information. `ssl_enabled=false` is flagged because it disables transport encryption.
4. `stat.S_IMODE` extracts permission bits. `mode & 0o077` detects *any* group or other access. A secret config should generally be owner-only, such as `0600`.
5. `sorted` uses `PRIORITY` so CRITICAL findings appear before HIGH findings.

### Sample findings

| Setting or mode | Severity | Suggested fix |
| --- | --- | --- |
| `password=EXAMPLE_NOT_REAL` | CRITICAL | Use a secret manager |
| `debug=true` | HIGH | Disable debug mode |
| `ssl_enabled=false` | HIGH | Enable TLS |
| `0666` file mode | HIGH | Set mode to `0600` |

### Limits and viva points

- The sample value is fake. It is created inside a private temporary directory and deleted automatically.
- This simple parser understands flat `key=value` lines. It does not parse YAML, JSON, comments, or nested settings.
- The priority number is an ordering aid: lower numbers mean higher urgency.

## How to Operate/Run the Files

```sh
python3 main.py
python3 main.py /path/to/config.conf
```

The first command creates and audits the sample. The second audits your own flat configuration file. The program uses only Python's standard library.
