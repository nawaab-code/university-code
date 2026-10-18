#!/usr/bin/env bash
# Start a separate Chrome profile, log session secrets, and disable QUIC for TCP/TLS.
set -euo pipefail
cd "$(dirname "$0")"
if [[ "$(uname -s)" == Darwin ]]; then
    browser="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
else
    browser="$(command -v google-chrome || command -v chromium || command -v chromium-browser || true)"
fi
if [[ -z "$browser" || ! -x "$browser" ]]; then
    echo "Install Google Chrome or Chromium first." >&2
    exit 1
fi
umask 077
export SSLKEYLOGFILE="$PWD/session.keys"
echo "Wireshark TLS key log file: $SSLKEYLOGFILE"
echo "Start capture, then browse in the new lab window. Close it when finished."
"$browser" --user-data-dir="$PWD/browser-profile" --disable-quic --no-first-run about:blank
