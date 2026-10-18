# Part B, Question 4: Log-Based Intrusion Detection System

## Question

Write a Python program that analyses network log entries and raises alerts for brute-force login attempts, port scanning activity, and large data transfers exceeding a defined threshold. Demonstrate detection of all three threat types from a simulated log dataset.

## Brief Explanation

The program scans a simulated CSV log and alerts on repeated failed logins, connections to several ports, or a transfer larger than the threshold.

## Extensive Explanation

### Remember the flow

**Count failures → collect distinct ports → compare transfer size.** These three signals map directly to the three requested threat types.

### Walkthrough

1. `csv.DictReader` gives each row named fields: `ip`, `event`, `port`, and `bytes`.
2. `failed[ip]` counts `LOGIN_FAILED` rows. Three or more failures from one IP produce a brute-force alert.
3. `ports[ip]` is a set, so connecting to the same port repeatedly counts once. Three or more *different* ports produce a port-scan alert.
4. A `TRANSFER` row above 1,000,000 bytes produces a large-transfer alert immediately. Exactly 1,000,000 bytes does not exceed the threshold.
5. The alerts are sorted before printing so the report order is predictable.

### Bundled example

| Example IP | Evidence | Alert |
| --- | --- | --- |
| `192.0.2.10` | Three failed logins | Brute-force login |
| `198.51.100.20` | Three different destination ports | Port scan |
| `203.0.113.30` | 1,500,000-byte transfer | Large transfer |

### Limits and viva points

- These addresses are documentation/example IPs. The CSV is simulated; no packets are captured.
- The program counts the whole file rather than a time window. A real IDS should define a period, tune thresholds, handle noisy logs, and avoid repeated alerts.
- Detection is a signal for investigation, not proof that an IP is malicious.

## How to Operate/Run the Files

```sh
python3 main.py
```

Run from this folder. Edit `sample_log.csv` to experiment with thresholds and events. Keep the header `ip,event,port,bytes`.
