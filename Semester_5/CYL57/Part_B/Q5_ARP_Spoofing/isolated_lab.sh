#!/usr/bin/env bash
# Linux VM only: private bridge plus victim, gateway/server, and attacker namespaces.
set -euo pipefail
if [[ $EUID -ne 0 ]]; then echo "Run with sudo on a Linux lab VM." >&2; exit 1; fi
python="${1:-python3}"
python="$(command -v "$python")"
folder="$(cd "$(dirname "$0")" && pwd)"
for tool in ip sysctl tcpdump curl; do command -v "$tool" >/dev/null; done
"$python" -c 'import scapy.all'
for ns in cyl57-victim cyl57-gateway cyl57-attacker; do
    if ip netns list | awk '{print $1}' | grep -qx "$ns"; then
        echo "Namespace $ns already exists; refusing to modify it." >&2; exit 1
    fi
done
if ip link show cyl57-br >/dev/null 2>&1; then echo "cyl57-br already exists." >&2; exit 1; fi
cleanup() {
    for ns in cyl57-victim cyl57-gateway cyl57-attacker; do
        for pid in $(ip netns pids "$ns" 2>/dev/null); do kill "$pid" 2>/dev/null || true; done
        ip netns del "$ns" 2>/dev/null || true
    done
    ip link del cyl57-br 2>/dev/null || true
}
trap cleanup EXIT
ip link add cyl57-br type bridge
ip link set cyl57-br up
for role in victim gateway attacker; do
    case "$role" in victim) n=2 ;; gateway) n=1 ;; attacker) n=3 ;; esac
    ip netns add "cyl57-$role"
    ip link add "c57-$n" type veth peer name "n57-$n"
    ip link set "c57-$n" master cyl57-br
    ip link set "c57-$n" up
    ip link set "n57-$n" netns "cyl57-$role"
    ip -n "cyl57-$role" link set "n57-$n" name eth0
    ip -n "cyl57-$role" link set eth0 address "02:00:00:57:00:0$n"
    ip -n "cyl57-$role" addr add "10.57.0.$n/24" dev eth0
    ip -n "cyl57-$role" link set eth0 up
    ip -n "cyl57-$role" link set lo up
done
# Only the attacker's namespace gets forwarding; no host settings are changed.
ip netns exec cyl57-attacker sysctl -qw net.ipv4.ip_forward=1
ip netns exec cyl57-attacker sysctl -qw net.ipv4.conf.all.send_redirects=0
ip netns exec cyl57-attacker sysctl -qw net.ipv4.conf.eth0.send_redirects=0
ip netns exec cyl57-gateway "$python" -m http.server 8080 --bind 10.57.0.1 > server.log 2>&1 &
# Capture both endpoints: seeing packets alone on a shared bridge would not prove MITM.
ip netns exec cyl57-victim tcpdump -U -n -i eth0 -w victim.pcap > victim-capture.log 2>&1 &
ip netns exec cyl57-attacker tcpdump -U -n -i eth0 -w mitm.pcap > capture.log 2>&1 &
sleep 1
printf 'BEFORE poisoning: establish legitimate neighbor entries.\n'
ip netns exec cyl57-victim curl --fail --silent --max-time 5 http://10.57.0.1:8080/ >/dev/null
ip -n cyl57-victim neigh show
ip netns exec cyl57-attacker "$python" "$folder/arp_demo.py" --send --duration 15 &
attack_pid=$!
sleep 3
printf 'DURING poisoning: gateway IP should map to attacker MAC ending 03.\n'
ip -n cyl57-victim neigh show
ip -n cyl57-gateway neigh show
ip netns exec cyl57-victim curl --fail --silent --max-time 5 http://10.57.0.1:8080/ >/dev/null
wait "$attack_pid"
sleep 1
printf 'AFTER restoration: gateway IP should map to genuine MAC ending 01.\n'
ip -n cyl57-victim neigh show
printf 'Saved mitm.pcap and victim.pcap; removing the isolated topology.\n'
