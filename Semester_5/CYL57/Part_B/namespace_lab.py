"""Run the firewall or ARP experiment in isolated Linux namespaces."""
import argparse
from contextlib import ExitStack
import os
from pathlib import Path
import signal
import subprocess
import sys
import time

PART_B = Path(__file__).resolve().parent
PYTHON = sys.executable


def ip(*args, **options):
    subprocess.run(("ip", *args), check=True, **options)


def create(cleanup, kind, name, *options):
    ip(kind, "add", name, *options)
    cleanup.callback(ip, kind, "delete", name)
    return name


def stop(process):
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()


def start(cleanup, namespace, *command, log=None):
    output = cleanup.enter_context(open(log, "w")) if log else None
    process = subprocess.Popen(("ip", "netns", "exec", namespace, *command),
                               stdout=output, stderr=subprocess.STDOUT, start_new_session=True)
    cleanup.callback(stop, process)
    return process


def configure(namespace, interface, address):
    ip("-n", namespace, "addr", "add", f"{address}/24", "dev", interface)
    ip("-n", namespace, "link", "set", interface, "up")


def serve(cleanup, namespace, address):
    return start(cleanup, namespace, PYTHON, "-m", "http.server", "8080", "--bind", address, log="server.log")


def capture(cleanup, namespace, interface, name, log="capture.log"):
    return start(cleanup, namespace, "tcpdump", "-U", "-n", "-i", interface, "-w", name, log=log)


def check_running(*processes):
    for process in processes:
        if process.poll() is not None:
            raise RuntimeError(f"Lab process exited: {' '.join(process.args)}")


def get_page(namespace, address):
    ip("netns", "exec", namespace, "curl", "-fsS", "--noproxy", "*", "--max-time", "5",
       f"http://{address}:8080/", stdout=subprocess.DEVNULL)


def firewall(cleanup):
    probe = create(cleanup, "netns", "cyl57-probe")
    target = create(cleanup, "netns", "cyl57-target")
    ip("-n", probe, "link", "add", "p57", "type", "veth", "peer", "name", "t57", "netns", target)
    configure(probe, "p57", "10.57.1.1")
    configure(target, "t57", "10.57.1.2")

    server = serve(cleanup, target, "10.57.1.2")
    trace = capture(cleanup, probe, "p57", "firewall.pcap")
    time.sleep(1)
    check_running(server, trace)
    get_page(probe, "10.57.1.2")

    probes = ("netns", "exec", probe, PYTHON, str(PART_B / "Q4_Packet_Crafting/packets.py"),
              "10.57.1.2", "--send")
    print("Before firewall rules:", flush=True)
    ip(*probes)
    ip("netns", "exec", target, "nft", "-f", "-", text=True, input="""\
add table inet cyl57
add chain inet cyl57 input { type filter hook input priority 0; policy accept; }
add rule inet cyl57 input tcp dport 8080 counter drop
add rule inet cyl57 input udp dport 9999 counter reject
""")
    print("After firewall rules:", flush=True)
    ip(*probes)
    ip("netns", "exec", target, "nft", "list", "table", "inet", "cyl57")
    check_running(trace)


def bridge_peer(cleanup, role, number):
    namespace = create(cleanup, "netns", f"cyl57-{role}")
    port = f"c57-{number}"
    # Deleting the namespace removes both ends of this veth pair.
    ip("link", "add", port, "type", "veth", "peer", "name", "eth0", "netns", namespace)
    ip("link", "set", port, "master", "cyl57-br", "up")
    ip("-n", namespace, "link", "set", "eth0", "address", f"02:00:00:57:00:0{number}")
    configure(namespace, "eth0", f"10.57.0.{number}")
    return namespace


def arp(cleanup):
    bridge = create(cleanup, "link", "cyl57-br", "type", "bridge")
    ip("link", "set", bridge, "up")
    victim = bridge_peer(cleanup, "victim", 2)
    gateway = bridge_peer(cleanup, "gateway", 1)
    attacker = bridge_peer(cleanup, "attacker", 3)
    ip("netns", "exec", attacker, "sysctl", "-qw", "net.ipv4.ip_forward=1",
       "net.ipv4.conf.all.send_redirects=0", "net.ipv4.conf.eth0.send_redirects=0")

    server = serve(cleanup, gateway, "10.57.0.1")
    victim_trace = capture(cleanup, victim, "eth0", "victim.pcap", "victim-capture.log")
    mitm_trace = capture(cleanup, attacker, "eth0", "mitm.pcap")
    time.sleep(1)
    check_running(server, victim_trace, mitm_trace)

    print("Before poisoning:", flush=True)
    get_page(victim, "10.57.0.1")
    ip("-n", victim, "neigh", "show")
    sender = start(cleanup, attacker, PYTHON, str(PART_B / "Q5_ARP_Spoofing/arp_demo.py"), "--send")

    time.sleep(3)
    check_running(sender)
    print("During poisoning:", flush=True)
    ip("-n", victim, "neigh", "show")
    ip("-n", gateway, "neigh", "show")
    get_page(victim, "10.57.0.1")
    if sender.wait(timeout=20):
        raise RuntimeError("ARP sender failed.")
    print("After restoration:", flush=True)
    ip("-n", victim, "neigh", "show")
    check_running(victim_trace, mitm_trace)


def interrupt(_signum, _frame):
    raise KeyboardInterrupt


if __name__ == "__main__":
    experiments = {"firewall": firewall, "arp": arp}
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("experiment", choices=experiments)
    args = parser.parse_args()
    if sys.platform != "linux" or os.geteuid() != 0:
        parser.error("Run with sudo on a Linux lab VM.")

    signal.signal(signal.SIGTERM, interrupt)
    try:
        import scapy.all
        with ExitStack() as cleanup:
            experiments[args.experiment](cleanup)
    except KeyboardInterrupt:
        parser.exit(130, "Lab interrupted.\n")
    except (ImportError, OSError, RuntimeError, subprocess.SubprocessError) as error:
        parser.exit(1, f"{error}\n")
