# Part B, Question 6: Network Threat Monitoring and Risk Scoring

## Question

Build a Python program that processes simulated network events, computes a weighted threat score per IP address based on failed attempts, port scans, and blocked connections, and classifies each host as LOW, MEDIUM, or HIGH risk. Output a ranked report and issue an alert for the most dangerous host.

## Brief Explanation

The program reads `sample_events.csv`, adds fixed weights per event, ranks IP addresses by score, and alerts on the highest-scoring host.

## Extensive Explanation

- A failed login adds 3 points, a port scan 5, and a blocked connection 2. Scores below 10 are LOW, scores from 10 to 19 are MEDIUM, and scores of 20 or more are HIGH.
- Events are accumulated by source IP. The report shows each score, classification, and event counts, sorted from highest score to lowest. IP address breaks score ties.
- The alert names the first ranked host. These weights and thresholds are examples for the lab; an operational system needs calibration and a time window so scores do not grow forever.

## How to Operate/Run the Files

```sh
python3 main.py
```

Run from this folder. Edit `sample_events.csv` to change the simulated events. CSV columns are `ip,event`.
