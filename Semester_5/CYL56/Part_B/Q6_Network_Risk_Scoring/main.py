"""Score simulated network events by source IP."""
import csv
from collections import defaultdict
from pathlib import Path

EVENTS = Path(__file__).with_name("sample_events.csv")
WEIGHTS = {"FAILED_LOGIN": 3, "PORT_SCAN": 5, "BLOCKED_CONNECTION": 2}


def risk(score):
    if score >= 20:
        return "HIGH"
    if score >= 10:
        return "MEDIUM"
    return "LOW"


def main():
    scores = defaultdict(int)
    counts = defaultdict(lambda: defaultdict(int))
    with EVENTS.open(newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            event = row["event"]
            if event not in WEIGHTS:
                raise ValueError(f"unknown event: {event}")
            ip = row["ip"]
            scores[ip] += WEIGHTS[event]
            counts[ip][event] += 1
    ranked = sorted(scores.items(), key=lambda item: (-item[1], item[0]))
    for ip, score in ranked:
        print(f"{ip}: score={score}, risk={risk(score)}, events={dict(counts[ip])}")
    if ranked:
        ip, score = ranked[0]
        print(f"ALERT: most dangerous host is {ip} (score {score}, {risk(score)} risk)")


if __name__ == "__main__":
    main()
