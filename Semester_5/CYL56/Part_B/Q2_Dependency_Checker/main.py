"""Compare a package inventory with a local, illustrative CVE database."""
import argparse
import importlib.metadata
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
PRIORITY = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}


def version(value):
    if not re.fullmatch(r"\d+(?:\.\d+)*", value):
        raise ValueError(f"unsupported version {value!r}; use numeric dotted versions")
    parts = tuple(int(x) for x in value.split("."))
    return parts + (0,) * (4 - len(parts))


def affected(installed, spec):
    current = version(installed)
    for condition in spec.split(","):
        match = re.fullmatch(r"(<=|>=|<|>|==)(\d+(?:\.\d+)*)", condition.strip())
        if not match:
            raise ValueError(f"invalid range condition: {condition}")
        op, boundary = match.groups()
        other = version(boundary)
        if not {"<": current < other, "<=": current <= other, ">": current > other,
                ">=": current >= other, "==": current == other}[op]:
            return False
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inventory", type=Path, default=HERE / "installed_packages.json")
    parser.add_argument("--database", type=Path, default=HERE / "vulnerabilities.json")
    parser.add_argument("--live", action="store_true", help="query this Python environment for listed packages")
    args = parser.parse_args()
    packages = json.loads(args.inventory.read_text(encoding="utf-8"))
    database = json.loads(args.database.read_text(encoding="utf-8"))
    if args.live:
        packages = {name: importlib.metadata.version(name) for name in packages}
    findings, no_match = [], []
    for name, installed in packages.items():
        matches = [entry for entry in database if entry["package"].lower() == name.lower()
                   and any(affected(installed, item) for item in entry["ranges"])]
        if matches:
            findings.extend((entry["severity"], name, installed, entry) for entry in matches)
        else:
            no_match.append((name, installed))
    for severity, name, installed, entry in sorted(findings, key=lambda x: (PRIORITY[x[0]], x[1], x[3]["cve"])):
        print(f"[{severity}] {name} {installed}: {entry['cve']} — {entry['details']}")
        print(f"  Advisory: {entry['url']}")
    print("No match in this local database:")
    for name, installed in sorted(no_match):
        print(f"  {name} {installed}")


if __name__ == "__main__":
    main()
