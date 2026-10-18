# Part B, Question 2: Software Dependency Vulnerability Checker

## Question

Implement a Python tool that checks a project's installed package versions against a vulnerability database using version range comparison. Report vulnerable packages with CVE details and severity, and list safe packages separately, sorted by priority.

## Brief Explanation

The checker compares a package/version inventory with a small local CVE database. It prints matching vulnerabilities by severity and lists packages with no local match separately.

## Extensive Explanation

### Remember the flow

**Read inventory → compare each version with CVE ranges → sort findings → list unmatched packages.**

### Files and data

- `installed_packages.json` is a reproducible snapshot of package names and versions. It represents what a project has installed for this exercise.
- `vulnerabilities.json` contains CVE IDs, package names, affected ranges, severity, a short description, and an advisory URL.
- `main.py` performs the comparison. You may give it another inventory JSON path as its first argument.

### Walkthrough

1. `version("2.30.0")` turns a dotted numeric version into `(2, 30, 0)`. Numeric tuples compare correctly where text comparison fails: `(2, 10, 0)` is greater than `(2, 9, 0)`.
2. `affected` checks every comma-separated condition in one range. For example, `>=2.3.0,<2.31.0` means both a lower and upper bound must hold.
3. A CVE can have several affected ranges. `any(...)` means one matching range is enough to report it.
4. Each matching package/CVE pair becomes a finding. `PRIORITY` sorts CRITICAL before HIGH before MEDIUM before LOW.
5. A package with no matching entry goes into the separate “No match in this local database” list.

### Worked example

The bundled inventory has `requests 2.30.0` and `urllib3 2.2.1`, which match the two bundled CVE entries. `certifi` has no entry in this small database, so it appears in the no-match list.

### Limits and viva points

- **No match is not proof of safety.** This database is intentionally tiny and is not updated automatically.
- The short comparator supports simple numeric dotted versions and `>=`/`<` ranges used by the sample. It is not a full PEP 440 implementation and does not handle prereleases or package-specific version rules.
- The sample CVEs and ranges are based on the [Requests advisory](https://github.com/psf/requests/security/advisories/GHSA-j8r2-6x86-q33q) and [urllib3 advisory](https://github.com/urllib3/urllib3/security/advisories/GHSA-34jh-p97f-mpxf).

## How to Operate/Run the Files

```sh
python3 main.py
python3 main.py installed_packages.json
```

Run from this folder. The first command uses the bundled inventory; the second shows how to supply an inventory path. Use a JSON object such as `{"requests": "2.30.0"}`.
