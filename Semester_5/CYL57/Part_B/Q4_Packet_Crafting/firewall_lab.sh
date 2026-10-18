#!/usr/bin/env bash
# Linux only. Two temporary, isolated network namespaces; no physical NICs.
set -euo pipefail
if [[ $EUID -ne 0 ]]; then echo "Run with sudo on a Linux lab VM." >&2; exit 1; fi
python="${1:-python3}"
python="$(command -v "$python")"
folder="$(cd "$(dirname "$0")" && pwd)"
for tool in ip nft tcpdump curl; do command -v "$tool" >/dev/null; done
"$python" -c 'import scapy.all'
for ns in cyl57-probe cyl57-target; do
    if ip netns list | awk '{print $1}' | grep -qx "$ns"; then
        echo "Namespace $ns already exists; refusing to modify it." >&2; exit 1
    fi
done
cleanup() {
    for ns in cyl57-probe cyl57-target; do
        for pid in $(ip netns pids "$ns" 2>/dev/null); do kill "$pid" 2>/dev/null || true; done
        ip netns del "$ns" 2>/dev/null || true
    done
}
trap cleanup EXIT
ip netns add cyl57-probe
ip netns add cyl57-target
ip link add p57 type veth peer name t57
ip link set p57 netns cyl57-probe
ip link set t57 netns cyl57-target
ip -n cyl57-probe addr add 10.57.1.1/24 dev p57
ip -n cyl57-target addr add 10.57.1.2/24 dev t57
ip -n cyl57-probe link set p57 up
ip -n cyl57-target link set t57 up
ip -n cyl57-probe link set lo up
ip -n cyl57-target link set lo up
ip netns exec cyl57-target "$python" -m http.server 8080 --bind 10.57.1.2 > server.log 2>&1 &
ip netns exec cyl57-probe tcpdump -U -n -i p57 -w firewall.pcap > capture.log 2>&1 &
sleep 1
ip netns exec cyl57-probe curl --fail --silent --max-time 5 http://10.57.1.2:8080/ >/dev/null
printf 'BEFORE rules: TCP SYN should get SYN-ACK; UDP gets ICMP port-unreachable.\n'
ip netns exec cyl57-probe "$python" "$folder/packets.py" 10.57.1.2 --send
ip netns exec cyl57-target nft -f - <<'RULES'
add table inet cyl57
add chain inet cyl57 input { type filter hook input priority 0; policy accept; }
add rule inet cyl57 input tcp dport 8080 counter drop
add rule inet cyl57 input udp dport 9999 counter reject
RULES
printf 'AFTER rules: TCP times out; UDP gets explicit rejection; ICMP still replies.\n'
ip netns exec cyl57-probe "$python" "$folder/packets.py" 10.57.1.2 --send
ip netns exec cyl57-target nft list table inet cyl57
sleep 1
printf 'Saved firewall.pcap. Namespace cleanup also removes their firewall rules.\n'
