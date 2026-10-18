import os
from pathlib import Path
import stat
import sys
import tempfile

PRIORITY = {"CRITICAL": 0, "HIGH": 1}


def audit(path):
    settings = {}
    for line_no, line in enumerate(path.read_text().splitlines(), 1):
        if "=" in line:
            key, value = line.split("=", 1)
            settings[key.strip().lower()] = (value.strip(), line_no)

    issues = []
    for key in ("password", "db_password", "api_key"):
        if key in settings and settings[key][0]:
            issues.append(("CRITICAL", f"line {settings[key][1]}: plaintext {key}", "Use a secret manager."))
    if settings.get("debug", ("",))[0].lower() in ("true", "1", "yes"):
        issues.append(("HIGH", "debug enabled", "Set debug=false."))
    if settings.get("ssl_enabled", ("",))[0].lower() in ("false", "0", "no"):
        issues.append(("HIGH", "SSL disabled", "Enable TLS."))
    mode = stat.S_IMODE(path.stat().st_mode)
    if mode & 0o077:
        issues.append(("HIGH", f"permissions {mode:04o}", "Run chmod 600 on the file."))
    return sorted(issues, key=lambda item: PRIORITY[item[0]])


def show(path):
    for severity, problem, fix in audit(path):
        print(f"[{severity}] {problem} — Fix: {fix}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        show(Path(sys.argv[1]))
    else:
        with tempfile.TemporaryDirectory() as folder:
            sample = Path(folder) / "sample.conf"
            sample.write_text("password=EXAMPLE_NOT_REAL\ndebug=true\nssl_enabled=false\n")
            os.chmod(sample, 0o666)
            show(sample)
