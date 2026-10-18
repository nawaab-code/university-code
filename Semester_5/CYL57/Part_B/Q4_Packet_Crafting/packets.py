"""Build a three-packet PCAP; optionally send one probe per protocol to a lab target."""
import argparse
import ipaddress
from scapy.all import ICMP, IP, TCP, UDP, Raw, sr1, wrpcap


def packets(target):
    return [IP(dst=target) / TCP(dport=8080, flags="S"),
            IP(dst=target) / UDP(dport=9999) / Raw(b"CYL57"),
            IP(dst=target) / ICMP()]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", nargs="?", default="10.57.1.2")
    parser.add_argument("--send", action="store_true", help="Send three probes (requires privileges)")
    args = parser.parse_args()
    address = ipaddress.IPv4Address(args.target)
    if not any(address in ipaddress.ip_network(net) for net in
               ("10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16", "127.0.0.0/8")):
        parser.error("Use a private IPv4 lab address or loopback address.")
    probes = packets(str(address))
    wrpcap("probes.pcap", probes)
    print("Wrote probes.pcap (constructed probes, not a live capture).")
    if args.send:
        for probe in probes:
            answer = sr1(probe, timeout=2, verbose=False)
            print(probe.summary(), "->", answer.summary() if answer else "No reply (not proof of a drop)")


if __name__ == "__main__":
    main()
