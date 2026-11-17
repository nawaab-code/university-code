"""Build TCP, UDP and ICMP probes, save them to probes.pcap, and optionally send them."""
import argparse
import ipaddress

from scapy.all import ICMP, IP, TCP, UDP, Raw, sr1, wrpcap

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("target", nargs="?", default="10.57.1.2")
parser.add_argument("--send", action="store_true", help="Send the probes (needs sudo)")
args = parser.parse_args()
if not ipaddress.ip_address(args.target).is_private:
    parser.error("Use a private IPv4 lab address.")

probes = [
    IP(dst=args.target) / TCP(dport=8080, flags="S"),        # TCP SYN
    IP(dst=args.target) / UDP(dport=9999) / Raw(b"CYL57"),  # UDP with payload
    IP(dst=args.target) / ICMP(),                           # ICMP echo request
]
wrpcap("probes.pcap", probes)
print("Wrote probes.pcap")

if args.send:
    for probe in probes:
        reply = sr1(probe, timeout=2, verbose=False)
        print(probe.summary(), "->", reply.summary() if reply else "no reply")
