#!/usr/bin/env bash
# Connect to the learner's lab server and retain SSH negotiation diagnostics.
set -euo pipefail
if [[ $# -ne 2 ]]; then
    echo "Usage: bash ssh_session.sh USER SERVER_IP" >&2
    exit 1
fi
ssh -vv -E ssh-debug.log -o ControlMaster=no -o ControlPath=none "$1@$2"
