from pathlib import Path
import re
import sys

RULES = [
    ("HIGH", "eval/exec", r"\b(?:eval|exec)\s*\("),
    ("HIGH", "shell command", r"\bos\.system\s*\(|\bshell\s*=\s*True\b"),
    ("HIGH", "hardcoded credential", r"\b(?:password|passwd|api_key|secret)\s*=\s*['\"][^'\"]+['\"]"),
    ("MEDIUM", "HTTP URL", r"http://[^\s'\"]+"),
]

source = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("sample_source.txt")
findings = []
for number, line in enumerate(source.read_text().splitlines(), 1):
    for severity, label, pattern in RULES:
        if re.search(pattern, line, re.I):
            findings.append((severity, number, label))

for severity, number, label in sorted(findings, key=lambda row: (row[0] != "HIGH", row[1])):
    print(f"[{severity}] line {number}: {label}")
