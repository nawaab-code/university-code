# Part B, Question 4: Log-Based Intrusion Detection System

## Question

Write a Python program that analyses network log entries and raises alerts for brute-force login attempts, port scanning activity, and large data transfers exceeding a defined threshold. Demonstrate detection of all three threat types from a simulated log dataset.

## Brief Explanation

The program reads `sample_log.csv`, counts failed logins and distinct connection ports per IP, and checks transfer size. The sample triggers all three alerts.

## Extensive Explanation

- Three or more failed logins from one IP trigger a brute-force alert. Three or more distinct ports trigger a port-scan alert.
- A single transfer above 1,000,000 bytes triggers a large-transfer alert. The threshold is strict: exactly 1,000,000 bytes does not alert.
- The CSV includes documentation-only example IP addresses. Results are sorted by IP and threat name for stable output.
- This small exercise counts across the whole input. A deployed IDS should use time windows, normalize log formats, suppress duplicates, and tune thresholds for its network.

## How to Operate/Run the Files

```sh
python3 main.py
```

Run from this folder; edit `sample_log.csv` to try other events. CSV columns are `ip,event,port,bytes`.
