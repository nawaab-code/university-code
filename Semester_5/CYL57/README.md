# CYL57 - Cryptography and Network Security Laboratory

Solutions for all 10 questions in the [course syllabus](syllabus.pdf). Every question has its own folder containing runnable source files and a README with the question, brief explanation, extensive explanation, worked examples or expected observations, and operating instructions.

## Part A - Java

| Question | Topic | Solution |
| --- | --- | --- |
| A1 | Caesar cipher with a user-defined shift; encryption/decryption | [Caesar cipher](Part_A/Q1_Caesar_Cipher/README.md) |
| A2 | Playfair cipher with a 5 x 5 matrix | [Playfair cipher](Part_A/Q2_Playfair_Cipher/README.md) |
| A3 | DES encryption/decryption using Java security libraries | [DES](Part_A/Q3_DES/README.md) |
| A4 | AES encryption/decryption with a 128-bit key | [AES-128](Part_A/Q4_AES/README.md) |
| A5 | RSA key generation, public-key encryption, private-key decryption | [RSA](Part_A/Q5_RSA/README.md) |

Requires a JDK, Java 11 or later. No external Java dependencies. Open the question folder, compile its `.java` file with `javac`, and run the class using `java`. Each README gives exact commands and input. The programs use standard crypto libraries where the syllabus permits them, keeping code short and reproducible.

## Part B - Wireshark and network experiments

| Question | Topic | Solution |
| --- | --- | --- |
| B1 | Secure browser transaction and TLS handshake analysis | [TLS](Part_B/Q1_TLS_Handshake/README.md) |
| B2 | HTTP/2 negotiation, streams, and TLS encryption | [HTTP/2](Part_B/Q2_HTTP2_Over_TLS/README.md) |
| B3 | SSH key exchange, encryption, and user authentication | [SSH](Part_B/Q3_SSH_Analysis/README.md) |
| B4 | TCP/UDP/ICMP packet crafting and firewall response | [Packet crafting](Part_B/Q4_Packet_Crafting/README.md) |
| B5 | ARP poisoning, neighbor tables, and MITM forwarding | [ARP spoofing](Part_B/Q5_ARP_Spoofing/README.md) |

B1-B2 include a dedicated Chrome/Chromium launcher for macOS/Linux with TLS key logging; B2 also includes concurrent browser requests. B3 includes an SSH helper and a two-system capture procedure. B4-B5 include both offline PCAP generators and complete isolated Linux namespace setups for live experiments. Use a full Linux lab VM for namespace scripts, not the macOS/Windows host. All interface and firewall changes in those scripts belong to temporary lab namespaces.

### Python environment

From this course directory:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

Python 3.8+ is sufficient for the code; use Python 3.10+ with the current Scapy release. Scapy is the only third-party Python dependency. On Windows substitute `.venv\Scripts\python.exe` for `.venv/bin/python`. Live scripts require Linux, sudo, iproute2, tcpdump, curl, and (for B4) nftables. Browser captures require Wireshark and capture permissions. See the relevant question for setup, output files, expected observations, and cleanup.

Generated captures, browser profiles, logs, TLS secrets, Python environments, and Java class files are ignored by Git. Source and documentation are tracked. Offline PCAPs are synthetic teaching data; they are not evidence that a live network experiment succeeded.

## Verification

Run from this directory after installing Scapy. Java (`java`/`javac`), Bash, and OpenSSL must also be available:

```bash
.venv/bin/python -m unittest discover -s tests -v
```

The tests compile every Java program for Java 11 and check known Caesar/Playfair vectors, shifts and filler edge cases, DES/AES/RSA round trips, Unicode and empty messages, RSA byte-length boundaries, and randomized crypto output. They parse the generated packet files to check protocols and conflicting/restored ARP claims. A local HTTPS server verifies the TLS helper's request, key logging, and rejection of an untrusted certificate. They also check shell/Python syntax and the required folder/README structure.

These checks never send crafted packets, change firewall rules, or connect to an external server. Browser/Wireshark interaction, the two-system SSH experiment, and privileged Linux namespace execution require the documented lab environment and were not executed on the macOS development host. Their READMEs describe expected outcomes and the actual evidence to collect; they do not claim fabricated packet observations.
