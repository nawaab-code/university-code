"""Run the CYL57 firewall or ARP experiment in isolated Linux namespaces."""
import argparse
from contextlib import ExitStack, nullcontext
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import time

PART_B = Path(__file__).resolve().parent
NFT_RULES = """\
add table inet cyl57
add chain inet cyl57 input { type filter hook input priority 0; policy accept; }
add rule inet cyl57 input tcp dport 8080 counter drop
add rule inet cyl57 input udp dport 9999 counter reject
"""


def run(*command, **kwargs):
    subprocess.run(command, check=True, **kwargs)


def cleanup_ip(*args):
    subprocess.run(("ip", *args), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def create_namespace(cleanup, role):
    name = f"cyl57-{role}"
    run("ip", "netns", "add", name)
    cleanup.callback(cleanup_ip, "netns", "del", name)
    run("ip", "-n", name, "link", "set", "lo", "up")
    return name


def configure_link(namespace, link, address):
    run("ip", "-n", namespace, "addr", "add", address, "dev", link)
    run("ip", "-n", namespace, "link", "set", link, "up")


def stop_process(process):
    if process.poll() is None:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()


def start_process(cleanup, namespace, *command, log=None):
    args = ("ip", "netns", "exec", namespace, *command)
    with (open(log, "w") if log else nullcontext()) as output:
        process = subprocess.Popen(
            args, stdout=output, stderr=subprocess.STDOUT, start_new_session=True,
        )
    cleanup.callback(stop_process, process)
    return process


def check_startup(*processes):
    time.sleep(1)
    for process in processes:
        if process.poll() is not None:
            raise RuntimeError(f"Process exited during startup: {' '.join(process.args)}. Check its lab log.")


def request_page(namespace, address):
    run("ip", "netns", "exec", namespace, "curl", "--fail", "--silent", "--show-error",
        "--noproxy", "*", "--max-time", "5", f"http://{address}:8080/",
        stdout=subprocess.DEVNULL)


def firewall_lab(cleanup):
    probe = create_namespace(cleanup, "probe")
    target = create_namespace(cleanup, "target")
    # Create the pair directly inside the namespaces so namespace removal cleans it up.
    run("ip", "-n", probe, "link", "add", "p57", "type", "veth", "peer",
        "name", "t57", "netns", target)
    configure_link(probe, "p57", "10.57.1.1/24")
    configure_link(target, "t57", "10.57.1.2/24")

    server = start_process(cleanup, target, sys.executable, "-m", "http.server", "8080",
                           "--bind", "10.57.1.2", log="server.log")
    capture = start_process(cleanup, probe, "tcpdump", "-U", "-n", "-i", "p57",
                            "-w", "firewall.pcap", log="capture.log")
    check_startup(server, capture)
    request_page(probe, "10.57.1.2")

    send_probes = ("ip", "netns", "exec", probe, sys.executable,
                   str(PART_B / "Q4_Packet_Crafting/packets.py"), "10.57.1.2", "--send")
    print("Before firewall rules:", flush=True)
    run(*send_probes)
    run("ip", "netns", "exec", target, "nft", "-f", "-", input=NFT_RULES, text=True)
    print("After firewall rules:", flush=True)
    run(*send_probes)
    run("ip", "netns", "exec", target, "nft", "list", "table", "inet", "cyl57")


def create_bridge_peer(cleanup, role, number):
    namespace = create_namespace(cleanup, role)
    bridge_end = f"c57-{number}"
    run("ip", "link", "add", bridge_end, "type", "veth", "peer",
        "name", "eth0", "netns", namespace)
    cleanup.callback(cleanup_ip, "link", "del", bridge_end)
    run("ip", "link", "set", bridge_end, "master", "cyl57-br")
    run("ip", "link", "set", bridge_end, "up")
    run("ip", "-n", namespace, "link", "set", "eth0", "address", f"02:00:00:57:00:0{number}")
    configure_link(namespace, "eth0", f"10.57.0.{number}/24")
    return namespace


def arp_lab(cleanup):
    run("ip", "link", "add", "cyl57-br", "type", "bridge")
    cleanup.callback(cleanup_ip, "link", "del", "cyl57-br")
    run("ip", "link", "set", "cyl57-br", "up")
    victim = create_bridge_peer(cleanup, "victim", 2)
    gateway = create_bridge_peer(cleanup, "gateway", 1)
    attacker = create_bridge_peer(cleanup, "attacker", 3)
    run("ip", "netns", "exec", attacker, "sysctl", "-qw", "net.ipv4.ip_forward=1",
        "net.ipv4.conf.all.send_redirects=0", "net.ipv4.conf.eth0.send_redirects=0")

    server = start_process(cleanup, gateway, sys.executable, "-m", "http.server", "8080",
                           "--bind", "10.57.0.1", log="server.log")
    victim_capture = start_process(cleanup, victim, "tcpdump", "-U", "-n", "-i", "eth0",
                                   "-w", "victim.pcap", log="victim-capture.log")
    mitm_capture = start_process(cleanup, attacker, "tcpdump", "-U", "-n", "-i", "eth0",
                                 "-w", "mitm.pcap", log="capture.log")
    check_startup(server, victim_capture, mitm_capture)

    print("Before poisoning:", flush=True)
    request_page(victim, "10.57.0.1")
    run("ip", "-n", victim, "neigh", "show")

    poisoning = start_process(cleanup, attacker, sys.executable,
                              str(PART_B / "Q5_ARP_Spoofing/arp_demo.py"), "--send", "--duration", "15")
    check_startup(poisoning)
    time.sleep(2)
    print("During poisoning:", flush=True)
    run("ip", "-n", victim, "neigh", "show")
    run("ip", "-n", gateway, "neigh", "show")
    request_page(victim, "10.57.0.1")
    if poisoning.wait(timeout=20):
        raise RuntimeError("ARP sender failed.")

    time.sleep(1)
    print("After restoration:", flush=True)
    run("ip", "-n", victim, "neigh", "show")


def interrupt(_signum, _frame):
    raise KeyboardInterrupt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("experiment", choices=("firewall", "arp"))
    args = parser.parse_args()
    if sys.platform != "linux" or os.geteuid() != 0:
        parser.error("Run with sudo on a Linux lab VM.")

    tools = ("ip", "tcpdump", "curl", "nft" if args.experiment == "firewall" else "sysctl")
    for tool in tools:
        if shutil.which(tool) is None:
            parser.error(f"Required tool is missing: {tool}")
    try:
        run(sys.executable, "-c", "import scapy.all")
        signal.signal(signal.SIGTERM, interrupt)
        with ExitStack() as cleanup:
            if args.experiment == "firewall":
                firewall_lab(cleanup)
            else:
                arp_lab(cleanup)
    except KeyboardInterrupt:
        parser.exit(130, "Lab interrupted.\n")
    except (OSError, RuntimeError, subprocess.SubprocessError) as error:
        parser.exit(1, f"{error}\n")

    captures = "firewall.pcap" if args.experiment == "firewall" else "mitm.pcap and victim.pcap"
    print(f"Saved {captures} and removed the isolated topology.")


if __name__ == "__main__":
    main()
