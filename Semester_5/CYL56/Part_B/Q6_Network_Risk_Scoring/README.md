# Part B, Question 6: Network Threat Monitoring and Risk Scoring

## Question

Build a Python program that processes simulated network events, computes a weighted threat score per IP address based on failed attempts, port scans, and blocked connections, and classifies each host as LOW, MEDIUM, or HIGH risk. Output a ranked report and issue an alert for the most dangerous host.

## Brief Explanation

The program assigns points to simulated security events, totals points per source IP, ranks hosts, classifies risk, and alerts on the top host.

## Extensive Explanation

### Remember the flow

**Event → weight → total per IP → sort → classify.** One small `WEIGHTS` dictionary contains the scoring rule.

### Walkthrough

1. `csv.DictReader` reads each `ip,event` row from `sample_events.csv`.
2. A failed login adds 3 points, a port scan 5, and a blocked connection 2. `defaultdict(int)` starts each unseen IP at zero.
3. `ranked` sorts by descending score. The IP string breaks ties so output stays deterministic.
4. `risk` returns HIGH for scores of 20 or more, MEDIUM for scores from 10 to 19, and LOW below 10.
5. The first item in the sorted list is the most dangerous host by this scoring rule, so the program prints an alert for it.

### Bundled example

| IP | Score calculation | Total | Risk |
| --- | --- | ---: | --- |
| `192.0.2.10` | `3×3 + 2×5 + 1×2` | 21 | HIGH |
| `198.51.100.20` | `1×3 + 1×5 + 1×2` | 10 | MEDIUM |
| `203.0.113.30` | `1×2` | 2 | LOW |

### Limits and viva points

- The weights and thresholds are illustrative and should be calibrated before operational use.
- Scores accumulate over the entire file. A real monitor needs a time window or decay so old events do not influence risk forever.
- A high score means review the host; it is not a definitive attack verdict.

## How to Operate/Run the Files

```sh
python3 main.py
```

Run from this folder. Edit `sample_events.csv` to try other combinations; keep the header `ip,event` and use only event names in `WEIGHTS`.
