import csv
from collections import defaultdict
from pathlib import Path

WEIGHTS = {"FAILED_LOGIN": 3, "PORT_SCAN": 5, "BLOCKED_CONNECTION": 2}
scores = defaultdict(int)

with Path(__file__).with_name("sample_events.csv").open(newline="") as file:
    for row in csv.DictReader(file):
        scores[row["ip"]] += WEIGHTS[row["event"]]


def risk(score):
    if score >= 20:
        return "HIGH"
    if score >= 10:
        return "MEDIUM"
    return "LOW"


ranked = sorted(scores.items(), key=lambda item: (-item[1], item[0]))
for ip, score in ranked:
    print(f"{ip}: score={score}, risk={risk(score)}")
if ranked:
    print(f"ALERT: most dangerous host is {ranked[0][0]}")
