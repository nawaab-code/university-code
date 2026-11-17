"""Start a fresh interactive OpenSSH session and log negotiation diagnostics."""
import argparse
import os


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("user")
    parser.add_argument("server", help="Lab server IP address or hostname")
    args = parser.parse_args()

    os.umask(0o077)
    try:
        os.execvp("ssh", [
            "ssh", "-vv", "-E", "ssh-debug.log", "-o", "ControlMaster=no",
            "-o", "ControlPath=none", "-l", args.user, "--", args.server,
        ])
    except OSError as error:
        parser.exit(1, f"Could not start OpenSSH: {error}\n")


if __name__ == "__main__":
    main()
