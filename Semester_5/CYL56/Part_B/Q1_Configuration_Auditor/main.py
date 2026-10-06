"""Audit a small key=value configuration and its file permissions."""
import argparse
import os
from pathlib import Path
import stat
import tempfile

PRIORITY = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}


def audit(path: Path):
    findings = []
    values = {}
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if "=" not in line:
            findings.append(("LOW", f"line {number}: malformed setting", "Use KEY=VALUE syntax."))
            continue
        key, value = (part.strip() for part in line.split("=", 1))
        values[key.lower()] = (value, number)
    for key in ("password", "db_password", "api_key"):
        if key in values and values[key][0]:
            findings.append(("CRITICAL", f"line {values[key][1]}: plaintext {key}",
                             "Store the secret in a secret manager or protected environment variable."))
    if values.get("debug", ("",))[0].lower() in ("true", "1", "yes"):
        findings.append(("HIGH", "debug mode enabled", "Set DEBUG=false in production."))
    if values.get("ssl_enabled", ("",))[0].lower() in ("false", "0", "no"):
        findings.append(("HIGH", "SSL disabled", "Enable TLS and validate certificates."))
    mode = stat.S_IMODE(path.stat().st_mode)
    if mode & 0o077:
        findings.append(("HIGH", f"file permissions {mode:04o} expose data to group/others",
                         "Restrict the file to owner read/write: chmod 600."))
    return sorted(findings, key=lambda item: (PRIORITY[item[0]], item[1]))


def report(path: Path):
    print(f"Auditing: {path}")
    findings = audit(path)
    for severity, issue, hint in findings:
        print(f"[{severity}] {issue}\n  Fix: {hint}")
    print(f"Total findings: {len(findings)}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path, nargs="?", help="configuration file to audit")
    args = parser.parse_args()
    if args.path:
        report(args.path)
    else:
        # The deliberately weak sample is isolated in a private temporary directory.
        with tempfile.TemporaryDirectory() as directory:
            sample = Path(directory) / "sample.conf"
            sample.write_text("password=EXAMPLE_NOT_REAL\ndebug=true\nssl_enabled=false\n", encoding="utf-8")
            os.chmod(sample, 0o666)
            report(sample)


if __name__ == "__main__":
    main()
