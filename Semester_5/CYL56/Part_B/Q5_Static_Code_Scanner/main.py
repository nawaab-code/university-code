"""Line-based demonstration scanner; findings need manual confirmation."""
import argparse
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
RULES = [
    ("HIGH", "dangerous eval/exec", re.compile(r"\b(?:eval|exec)\s*\(")),
    ("HIGH", "shell command execution", re.compile(r"\bos\.system\s*\(|\bshell\s*=\s*True\b")),
    ("HIGH", "hardcoded credential", re.compile(r"\b(?:password|passwd|api_key|secret)\s*=\s*['\"][^'\"]+['\"]", re.I)),
    ("MEDIUM", "insecure HTTP URL", re.compile(r"http://[^\s'\"]+", re.I)),
]
PRIORITY = {"HIGH": 0, "MEDIUM": 1}


def scan(path):
    findings = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        for severity, label, pattern in RULES:
            if pattern.search(line):
                findings.append((severity, number, label))
    return sorted(findings, key=lambda item: (PRIORITY[item[0]], item[1], item[2]))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path, nargs="?", default=HERE / "sample_source.txt")
    args = parser.parse_args()
    for severity, line, label in scan(args.source):
        print(f"[{severity}] line {line}: {label}")


if __name__ == "__main__":
    main()
