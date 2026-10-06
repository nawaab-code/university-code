# Part B, Question 1: Secure Configuration File Auditor

## Question

Implement a Python program that creates a sample configuration file containing common security misconfigurations such as plaintext passwords, debug mode enabled, SSL disabled, and insecure file permissions. Audit the file and report all issues with severity labels sorted by priority, along with a remediation hint.

## Brief Explanation

The program creates a deliberately weak sample configuration, checks its settings and file mode, then prints prioritized findings and fixes.

## Extensive Explanation

- It reads simple `KEY=VALUE` settings and records line numbers. Nonempty `password`, `db_password`, and `api_key` values are treated as plaintext secrets.
- Enabled debug mode and disabled SSL are flagged. The file mode is checked for any group or other permissions; secret files should normally be restricted to owner read/write (`0600`).
- Findings are sorted CRITICAL, HIGH, MEDIUM, LOW. The sample is created inside a private temporary directory and deleted when the program ends, so its deliberately loose file mode is contained.
- This is a teaching auditor for a flat configuration format, not a parser for YAML, JSON, or every security setting.

## How to Operate/Run the Files

```sh
python3 main.py
python3 main.py /path/to/config.conf
```

The first command creates and audits the built-in sample. The second audits your own `KEY=VALUE` file.
