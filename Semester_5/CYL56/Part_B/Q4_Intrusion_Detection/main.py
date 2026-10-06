"""Detect three simple patterns in a simulated network log."""
import csv
from collections import defaultdict
from pathlib import Path

LOG = Path(__file__).with_name("sample_log.csv")
FAILED_LIMIT = 3
PORT_LIMIT = 3
TRANSFER_LIMIT = 1_000_000


def detect(rows):
    failed = defaultdict(int)
    ports = defaultdict(set)
    alerts = []
    for row in rows:
        ip = row["ip"]
        if row["event"] == "LOGIN_FAILED":
            failed[ip] += 1
        elif row["event"] == "CONNECT":
            ports[ip].add(int(row["port"]))
        elif row["event"] == "TRANSFER" and int(row["bytes"]) > TRANSFER_LIMIT:
            alerts.append((ip, "large transfer", f"{row['bytes']} bytes"))
    for ip, count in failed.items():
        if count >= FAILED_LIMIT:
            alerts.append((ip, "brute-force login", f"{count} failures"))
    for ip, distinct_ports in ports.items():
        if len(distinct_ports) >= PORT_LIMIT:
            alerts.append((ip, "port scan", f"{len(distinct_ports)} distinct ports"))
    return sorted(alerts, key=lambda alert: (alert[0], alert[1]))


def main():
    with LOG.open(newline="", encoding="utf-8") as file:
        alerts = detect(csv.DictReader(file))
    for ip, threat, evidence in alerts:
        print(f"ALERT {ip}: {threat} ({evidence})")
    print(f"Total alerts: {len(alerts)}")


if __name__ == "__main__":
    main()
