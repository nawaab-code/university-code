# ARP spoofing in an isolated local network

## 1. Question

Simulate an ARP spoofing attack in a controlled local network using tools like arpspoof or Ettercap. Capture the ARP traffic with Wireshark to observe the malicious ARP replies and analyze how the attacker intercepts traffic (Man-in-the-Middle).

## 2. Brief explanation

ARP maps a local IPv4 address to an Ethernet MAC address without authenticating the claim. A forged reply can make a victim send frames for another machine to the attacker's MAC. Poison both peers and enable forwarding on the attacker to observe a working man-in-the-middle path in an entirely isolated lab.

This solution uses Scapy as the packet-crafting alternative to arpspoof/Ettercap, so both the forged claims and their restoration are visible in short Python code.

## 3. Extensive explanation

### The fixed topology

`isolated_lab.sh` builds a private Linux bridge and three network namespaces. The bridge has no host IP and no physical uplink. No internet route is added.

| Role | Namespace | IP | MAC |
| --- | --- | --- | --- |
| Gateway/server | cyl57-gateway | 10.57.0.1 | 02:00:00:57:00:01 |
| Victim/client | cyl57-victim | 10.57.0.2 | 02:00:00:57:00:02 |
| Attacker/forwarder | cyl57-attacker | 10.57.0.3 | 02:00:00:57:00:03 |

All three use `eth0` inside their own namespace and share a /24 link through `cyl57-br`. The gateway role runs an HTTP server locally, rather than routing to the internet. Because the peers are on one subnet, the victim ARPs directly for 10.57.0.1; a default route is unnecessary for this exchange.

```text
Normal:    victim --------------------> gateway HTTP server
Poisoned:  victim ----> attacker ------> gateway HTTP server
           victim <---- attacker <----- gateway HTTP server
```

### The two false claims

The attacker sends unsolicited ARP replies (`op=2`):

1. To the victim: **10.57.0.1 is at 02:00:00:57:00:03**.
2. To the gateway: **10.57.0.2 is at 02:00:00:57:00:03**.

`psrc` is the IPv4 address being claimed; `hwsrc` is the claimed MAC address. `pdst` and `hwdst` identify the intended recipient. The outer `Ether` header delivers each reply directly to its recipient. Both false claims use the attacker's MAC. Poisoning one direction alone does not guarantee observation of both halves of the conversation.

The attacker enables IPv4 forwarding inside its own namespace so intercepted IP packets continue to the intended peer. ICMP redirects are disabled there to avoid teaching the peers a path that bypasses the attacker. Poisoning without forwarding can interrupt traffic instead of producing a working MITM path.

### Understanding arp_demo.py

- `reply` constructs a single Ethernet/ARP reply.
- `poison_packets` constructs the two false bindings using the fixed lab constants.
- Without options, `main` writes `arp-demo.pcap` containing five synthetic frames: a genuine gateway binding, the two forged replies, and two genuine restoration bindings. No traffic is sent.
- `--send` sends both false claims once per second for a bounded duration (default 15 seconds, maximum 60). It checks the selected interface has the fixed attacker MAC.
- A `finally` block sends corrective bindings three times when the loop exits, including on Ctrl-C. Corrective claims restore genuine mappings; deleting the isolated namespaces also removes their neighbor tables.
- The script is deliberately tied to the provided topology rather than scanning or accepting arbitrary LAN victims.

The offline file demonstrates header changes only. It does not contain HTTP, prove a neighbor-cache change, or show intercepted live traffic. The live namespace setup is the implementation of the full network experiment.

### Evidence that interception actually happened

Seeing an ARP reply does not prove that the receiver accepted it. Seeing packets on a bridge does not alone prove the attacker was in the forwarding path. Collect all of these:

1. Before poisoning, the victim's neighbor table maps 10.57.0.1 to the genuine MAC ending `01`.
2. During poisoning, the victim maps 10.57.0.1 to MAC ending `03`; the gateway maps the victim's IP to MAC ending `03`.
3. In `victim.pcap`, a during-attack HTTP frame has destination Ethernet MAC ending `03` while destination IP remains 10.57.0.1. Before attack, its destination MAC ends `01`.
4. In `mitm.pcap`, inspect both the received victim frame and the forwarded frame toward MAC ending `01`. Forwarding changes Ethernet headers and decrements IP TTL; the TCP application conversation is preserved.
5. The HTTP request succeeds during the attack, and the genuine gateway mapping returns after restoration.

HTTP is used to make the payload visible. ARP poisoning does not by itself decrypt correctly authenticated HTTPS or SSH. Encrypted traffic may be relayed while its content remains protected.

### Wireshark filters

| Purpose | Display filter |
| --- | --- |
| All ARP traffic | `arp` |
| ARP replies | `arp.opcode == 2` |
| Gateway IP claims | `arp.src.proto_ipv4 == 10.57.0.1` |
| Forged gateway claims | `arp.src.proto_ipv4 == 10.57.0.1 and arp.src.hw_mac == 02:00:00:57:00:03` |
| Attacker's Ethernet traffic | `eth.addr == 02:00:00:57:00:03` |
| HTTP experiment | `tcp.port == 8080` |

Wireshark's duplicate-IP/expert warnings can provide clues but are not guaranteed on every trace. Explicitly compare bindings and Ethernet destinations. Record frame numbers, timestamps, before/during/after neighbor tables, and HTTP success in your lab record.

ARP spoofing is possible because ordinary ARP lacks message authentication. Common defenses include dynamic ARP inspection paired with trusted binding data, segmentation, and carefully managed static neighbor entries. End-to-end authenticated encryption protects application content even if the local forwarding path is manipulated.

## 4. How to operate/run the files

### Offline inspection (no privileges or network sending)

Install Scapy in the course's virtual environment, then run from this question folder:

```bash
../../.venv/bin/python arp_demo.py
```

Open `arp-demo.pcap` in Wireshark. Compare `arp.src.proto_ipv4` and `arp.src.hw_mac` across its five synthetic frames. For environment setup see the [course README](../../README.md).

### Full live experiment (Linux lab VM only)

Use an Ubuntu/Debian VM, sudo, and the course virtual environment inside that VM:

```bash
sudo apt-get update
sudo apt-get install python3-venv iproute2 tcpdump curl
```

From this question folder:

```bash
sudo bash isolated_lab.sh "$(cd ../../.venv/bin && pwd)/python"
```

The script runs for roughly 20 seconds. It creates the three namespaces, starts the server and packet captures, makes a baseline HTTP request, prints the legitimate binding, starts poisoning, prints poisoned bindings, makes another HTTP request through the attacker, waits for restoration, and prints the restored binding. On exit it stops namespace processes and removes the topology.

Open `victim.pcap` and `mitm.pcap` in Wireshark and use the evidence checklist above. `arp-demo.pcap` remains a synthetic teaching trace even when the live lab has also run. Server/capture logs and generated traces stay local and are ignored by Git.

Run on a full Linux VM if network namespaces are blocked by a container runtime. Existing namespaces/bridge with these names cause the setup to stop instead of modifying them. Normal exit/Ctrl-C removes the topology; SIGKILL or a system crash cannot run cleanup. Inspect and remove only your own stale lab namespaces before retrying. The script requires a normal Linux namespace implementation and kernel forwarding; these live steps cannot run directly on macOS or Windows.

## References

[Scapy usage guide](https://scapy.readthedocs.io/en/stable/usage.html) documents Ethernet/ARP construction and `sendp`. [Linux network namespaces](https://man7.org/linux/man-pages/man8/ip-netns.8.html) explains isolation. [Wireshark ARP fields](https://www.wireshark.org/docs/dfref/a/arp.html) lists display filters.
