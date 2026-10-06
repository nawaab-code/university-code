# Part B, Question 2: Software Dependency Vulnerability Checker

## Question

Implement a Python tool that checks a project's installed package versions against a vulnerability database using version range comparison. Report vulnerable packages with CVE details and severity, and list safe packages separately, sorted by priority.

## Brief Explanation

The program compares versions in `installed_packages.json` with affected ranges in `vulnerabilities.json`. Matching CVEs appear in severity order; packages with no match appear separately.

## Extensive Explanation

- Each inventory entry represents one installed package and version. `--live` instead asks the current Python environment for versions of those listed packages.
- Each CVE entry contains package name, severity, affected range, details, and advisory URL. Multiple ranges handle separate vulnerable release branches. A package is flagged when any range matches.
- The version parser deliberately accepts numeric dotted versions only, such as `2.30.0`. It rejects prerelease labels and build suffixes rather than silently comparing them incorrectly.
- “No match” means only that this small local database has no matching entry. It does **not** prove a package is globally safe. Production vulnerability scanning needs a maintained advisory feed and a full version standard such as PEP 440.
- The included CVE entries and ranges are sourced from the [Requests advisory](https://github.com/psf/requests/security/advisories/GHSA-j8r2-6x86-q33q) and [urllib3 advisory](https://github.com/urllib3/urllib3/security/advisories/GHSA-34jh-p97f-mpxf).

## How to Operate/Run the Files

```sh
python3 main.py
python3 main.py --inventory installed_packages.json --database vulnerabilities.json
python3 main.py --live
```

Run from this folder. The default command uses the included reproducible package inventory. `--live` requires its listed packages to be installed in the current Python environment and to have numeric dotted versions.
