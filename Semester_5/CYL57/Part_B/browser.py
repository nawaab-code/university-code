"""Launch Chrome or Chromium with a dedicated TLS capture profile."""
import os
from pathlib import Path
import shutil
import sys


if __name__ == "__main__":
    browser = (shutil.which("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
               or shutil.which("google-chrome") or shutil.which("chromium")
               or shutil.which("chromium-browser"))
    if browser is None:
        sys.exit("Install Google Chrome or Chromium first.")

    os.umask(0o077)
    os.environ["SSLKEYLOGFILE"] = str(Path("session.keys").resolve())
    print("Wireshark TLS key log:", os.environ["SSLKEYLOGFILE"], flush=True)
    os.execv(browser, [browser, f"--user-data-dir={Path('browser-profile').resolve()}",
                       "--disable-quic", "--no-first-run", "about:blank"])
