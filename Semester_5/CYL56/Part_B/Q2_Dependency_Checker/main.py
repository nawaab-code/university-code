import json
from pathlib import Path
import sys

HERE = Path(__file__).parent
PRIORITY = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}


def version(text):
    parts = tuple(map(int, text.split(".")))
    return parts + (0,) * (3 - len(parts))


def affected(installed, rule):
    for condition in rule.split(","):
        if condition.startswith(">="):
            if installed < version(condition[2:]):
                return False
        elif condition.startswith("<"):
            if installed >= version(condition[1:]):
                return False
        else:
            raise ValueError(f"unsupported range: {condition}")
    return True


inventory = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "installed_packages.json"
packages = json.loads(inventory.read_text())
database = json.loads((HERE / "vulnerabilities.json").read_text())
findings, no_match = [], []
for name, installed in packages.items():
    matches = [item for item in database if item["package"] == name
               and any(affected(version(installed), rule) for rule in item["ranges"])]
    if matches:
        findings.extend((item["severity"], name, installed, item) for item in matches)
    else:
        no_match.append(f"{name} {installed}")

for severity, name, installed, item in sorted(findings, key=lambda row: PRIORITY[row[0]]):
    print(f"[{severity}] {name} {installed}: {item['cve']} — {item['details']}")
    print(f"  {item['url']}")
print("No match in this local database:", ", ".join(sorted(no_match)) or "none")
