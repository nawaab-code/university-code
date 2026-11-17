"""Open Chrome/Chromium with a fresh profile that logs TLS keys to session.keys."""
import os
import shutil
import subprocess
import sys

browser = next(filter(None, map(shutil.which, [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "google-chrome", "chromium", "chromium-browser"])), None)
if browser is None:
    sys.exit("Install Google Chrome or Chromium first.")

keys = os.path.abspath("session.keys")
print("Wireshark TLS key log:", keys)
# QUIC is disabled so the page loads over TCP + TLS, which Wireshark shows as TLS.
subprocess.run([browser, "--user-data-dir=browser-profile", "--disable-quic", "--no-first-run"],
               env={**os.environ, "SSLKEYLOGFILE": keys})
