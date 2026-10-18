import csv
from collections import defaultdict
from pathlib import Path

failed = defaultdict(int)
ports = defaultdict(set)
alerts = []

with Path(__file__).with_name("sample_log.csv").open(newline="") as file:
    for row in csv.DictReader(file):
        ip = row["ip"]
        if row["event"] == "LOGIN_FAILED":
            failed[ip] += 1
        elif row["event"] == "CONNECT":
            ports[ip].add(int(row["port"]))
        elif row["event"] == "TRANSFER" and int(row["bytes"]) > 1_000_000:
            alerts.append((ip, "large transfer"))

for ip, count in failed.items():
    if count >= 3:
        alerts.append((ip, "brute-force login"))
for ip, seen in ports.items():
    if len(seen) >= 3:
        alerts.append((ip, "port scan"))

for ip, threat in sorted(alerts):
    print(f"ALERT {ip}: {threat}")
