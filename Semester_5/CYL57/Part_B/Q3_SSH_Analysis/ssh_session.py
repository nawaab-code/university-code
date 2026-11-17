"""Start a fresh OpenSSH session and save the negotiation log."""
import argparse
import os


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("user")
    parser.add_argument("server", help="Lab server IP address or hostname")
    args = parser.parse_args()

    os.umask(0o077)
    try:
        os.execvp("ssh", ["ssh", "-vv", "-E", "ssh-debug.log", "-o", "ControlPath=none",
                          "-l", args.user, "--", args.server])
    except OSError as error:
        parser.exit(1, f"{error}\n")
