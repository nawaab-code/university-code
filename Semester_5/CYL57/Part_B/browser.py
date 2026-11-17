"""Launch a dedicated Chrome or Chromium profile for a Wireshark TLS capture."""
import os
from pathlib import Path
import shutil
import sys


def main():
    candidates = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "google-chrome", "chromium", "chromium-browser",
    ]
    browser = next((path for name in candidates if (path := shutil.which(name))), None)
    if browser is None:
        sys.exit("Install Google Chrome or Chromium first.")

    os.umask(0o077)
    keylog = Path("session.keys").resolve()
    profile = Path("browser-profile").resolve()
    os.environ["SSLKEYLOGFILE"] = str(keylog)
    print(f"Wireshark TLS key log file: {keylog}", flush=True)
    print("Start capture, then browse in the new lab window. Close it when finished.", flush=True)
    os.execv(browser, [
        browser, f"--user-data-dir={profile}", "--disable-quic", "--no-first-run", "about:blank",
    ])


if __name__ == "__main__":
    main()
