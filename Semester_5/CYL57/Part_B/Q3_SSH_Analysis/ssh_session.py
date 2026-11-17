"""Start a fresh SSH session and save its negotiation log to ssh-debug.log."""
import subprocess
import sys

if len(sys.argv) != 3:
    sys.exit("Usage: python3 ssh_session.py USER SERVER_IP")
user, server = sys.argv[1:]

# -vv logs key exchange, cipher and authentication; ControlPath=none forces a new handshake.
subprocess.run(["ssh", "-vv", "-E", "ssh-debug.log", "-o", "ControlPath=none", "-l", user, "--", server])
