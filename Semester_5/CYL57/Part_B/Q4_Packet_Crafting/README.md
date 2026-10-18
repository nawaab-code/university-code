# Custom packets and firewall behavior

## 1. Question

Use a packet crafting tool such as Scapy (Python) to create custom TCP, UDP, or ICMP packets. Send these packets to a target system and observe how a firewall responds. Use Wireshark to capture and analyze the traffic, including flags, headers, and dropped packets.

## 2. Brief explanation

Build one TCP SYN, one UDP datagram, and one ICMP echo request. First inspect them offline. Then send them inside an isolated Linux lab before and after adding firewall rules. Compare replies, timeouts, and rule counters; a timeout alone does not prove a firewall dropped a packet.

## 3. Extensive explanation

### Understanding packets.py

Scapy's `/` operator stacks protocol layers:

```python
IP(dst=target) / TCP(dport=8080, flags="S")
IP(dst=target) / UDP(dport=9999) / Raw(b"CYL57")
IP(dst=target) / ICMP()
```

- IP supplies the destination address. Scapy fills defaults and calculates lengths/checksums when serializing.
- The TCP probe uses flag S (SYN), the first step of establishing a connection. It is a probe, not a complete TCP client.
- UDP carries five payload bytes, `CYL57`, to port 9999.
- The default ICMP packet is an echo request.
- `wrpcap` saves constructed packets in `probes.pcap`. This file contains only our constructed probes, not observed replies or evidence of firewall action.
- With `--send`, `sr1` sends one probe and waits up to two seconds for its first matching reply. The script sends only three probes per run.
- Input is limited to the three private IPv4 ranges and loopback. Use only an owned lab target; a private address is not itself proof of permission.

### Understanding the isolated firewall lab

`firewall_lab.sh` creates two Linux network namespaces connected by a veth pair. A namespace has its own interfaces, routes, processes' network view, and firewall rules.

```text
cyl57-probe                         cyl57-target
10.57.1.1 / p57 <--- veth pair ---> 10.57.1.2 / t57
Scapy + tcpdump                    HTTP server + nftables
```

Neither namespace is attached to a physical interface or given an internet route. The script starts an HTTP server on TCP 8080, verifies it with curl, captures on the probe side, and runs the probes. It then adds nftables rules **inside the target namespace**: drop TCP 8080, reject UDP 9999, and accept other input. The script repeats the probes, prints counters, and removes both namespaces and their rules on exit.

### Expected observations, not prerecorded results

| Probe | Before rules | After rules | Explanation |
| --- | --- | --- | --- |
| TCP SYN to 8080 | SYN-ACK from listening server | No reply within timeout | DROP silently discards SYN |
| UDP to 9999 | ICMP port unreachable | ICMP rejection, often port unreachable | Closed UDP port and firewall REJECT can look similar; counters distinguish them |
| ICMP echo | Echo reply | Echo reply | Policy allows ICMP |

The host kernel may send RST after a SYN-ACK because Scapy's SYN did not create a normal kernel TCP connection. That RST is not necessarily a firewall block. nftables counters on the relevant rule supply direct local evidence that the target firewall matched a probe. Background IPv6/control traffic may also appear in the capture.

### Wireshark inspection

Capture filter, if capturing manually: `host 10.57.1.2`. Open `firewall.pcap` and try:

| Purpose | Display filter |
| --- | --- |
| All experiment traffic | `ip.addr == 10.57.1.2` |
| TCP SYN probes | `tcp.port == 8080 and tcp.flags.syn == 1` |
| Reset packets | `tcp.flags.reset == 1` |
| UDP probe | `udp.port == 9999` |
| ICMP requests, replies, and errors | `icmp` |

Expand Ethernet, IP, and transport headers where present. `probes.pcap` uses raw IP encapsulation; the live veth capture includes Ethernet. Record source/destination IPs and ports, TTL, protocol, TCP flags and sequence numbers, UDP length and payload, ICMP type/code, timing, and rule counters. A missing response can also mean a down host, packet loss, capture at the wrong location, or a reply outside the timeout. Captures on both sides or target counters resolve that ambiguity.

## 4. How to operate/run the files

### Offline packet creation (macOS, Linux, or Windows)

From `Semester_5/CYL57`, create an environment and install the one Python dependency:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
cd Part_B/Q4_Packet_Crafting
../../.venv/bin/python packets.py
```

On Windows use `.venv\Scripts\python.exe` with the equivalent paths. Open `probes.pcap` in Wireshark and inspect the three packets. No packets are sent without `--send`.

### Live experiment (Linux lab VM only)

The complete provided topology uses Linux network namespaces, unavailable natively on macOS and Windows. Use an Ubuntu/Debian VM with sudo access. Install tools there:

```bash
sudo apt-get update
sudo apt-get install python3-venv iproute2 nftables tcpdump curl
```

Set up the Python environment as above inside that VM. From this question folder:

```bash
sudo bash firewall_lab.sh "$(cd ../../.venv/bin && pwd)/python"
```

The script takes roughly ten seconds and prints results before/after the rules plus counters. Open its `firewall.pcap` in Wireshark; save the terminal output and your packet observations for your record. It also produces local `server.log`, `capture.log`, and `probes.pcap` files. Offline and live outputs are ignored by Git.

For an already configured owned lab target, the manual send command is:

```bash
sudo ../../.venv/bin/python packets.py 192.168.56.20 --send
```

Start Wireshark before that command and separately configure/inspect the target's firewall. Use the provided namespace script when you want repeatable known rules and a known open port.

If sudo or namespace creation fails inside a restricted container, use a full Linux VM. If a stale `cyl57-probe` or `cyl57-target` namespace exists, inspect it and remove it only if it is left over from your own prior lab; the script refuses to overwrite existing namespaces. Normal exit and Ctrl-C clean up automatically; SIGKILL or a VM crash cannot run cleanup traps.

## References

[Scapy usage guide](https://scapy.readthedocs.io/en/stable/usage.html) explains protocol stacking and send/receive helpers. [Linux network namespaces](https://man7.org/linux/man-pages/man8/ip-netns.8.html) describes namespace execution and lifecycle. [nftables manual](https://netfilter.org/projects/nftables/manpage.html) documents counters, drop, and reject.
