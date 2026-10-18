# SSH session capture and analysis

## 1. Question

Initiate an SSH session between two local systems or virtual machines. Capture traffic using Wireshark and analyse the session key exchange, encryption setup, and user authentication.

## 2. Brief explanation

Capture a fresh SSH connection between a client and a lab server. Observe version banners and key-exchange negotiation, then correlate the encrypted packets with the SSH client's verbose log to identify encryption and successful user authentication.

## 3. Extensive explanation

### Connection sequence

1. TCP connects to the server's SSH port, normally 22.
2. Both endpoints send readable version strings, typically beginning `SSH-2.0-`.
3. SSH_MSG_KEXINIT messages offer key-exchange methods, host-key algorithms, ciphers, MACs, and compression choices.
4. The selected key exchange derives shared secrets. The server proves its host identity with a host-key signature. The client checks that host key against its trusted `known_hosts` data; on first contact, compare the fingerprint with the server administrator or its console.
5. SSH_MSG_NEWKEYS activates negotiated keys independently in each direction. The derived session keys themselves are not sent in plaintext.
6. User authentication happens inside encryption: public key, password, or another configured method. An interactive shell or remote command follows.

Host authentication and user authentication are different. The host key identifies the server. The user's password or key proves permission to log in to that server. SSH is its own protocol; it does not run inside TLS.

### What Wireshark can and cannot show

The version banners and initial KEXINIT lists are normally visible. Some exchange packets may appear as structured fields depending on Wireshark version and the selected KEX algorithm. After NEWKEYS, packet contents including authentication and shell commands are encrypted. A packet capture alone generally cannot reveal a password, prove which authentication method succeeded, or show your command text.

Use `ssh-debug.log` as **endpoint evidence** for selected algorithms and authentication. Do not report log details as though they were decoded from ciphertext. SSH session secrets are not the TLS `SSLKEYLOGFILE`, and loading a TLS key log will not decrypt SSH.

### Understanding the helper

`ssh_session.sh USER SERVER_IP` runs:

```bash
ssh -vv -E ssh-debug.log -o ControlMaster=no -o ControlPath=none USER@SERVER_IP
```

- `-vv` enables detailed negotiation and authentication diagnostics.
- `-E` writes those diagnostics to a local file while leaving the terminal available for login and commands.
- `ControlMaster=no` and `ControlPath=none` avoid reusing an existing multiplexed SSH session; this produces a fresh handshake.
- The SSH client's standard host-key checking remains enabled.
- `set -euo pipefail` stops the shell helper on failures or missing variables.

### Observation table

| Item | Evidence source |
| --- | --- |
| Client/server addresses and ports | TCP packet details |
| Version banners | SSH protocol details or Follow TCP Stream |
| Offered KEX, ciphers, host-key algorithms | Initial KEXINIT packets |
| Selected KEX, host key, cipher, MAC/AEAD | Verbose SSH log; correlate with offers |
| NEWKEYS activation | Wireshark SSH packet sequence |
| Successful user authentication and method | Client log and successful terminal session |
| Shell command secrecy | Encrypted packets after NEWKEYS, no readable command text |

With AEAD ciphers, integrity is integrated into the cipher rather than a separate conventional MAC. Algorithm choices vary by OpenSSH version and configuration.

## 4. How to operate/run the files

Use two owned systems or two VMs on a host-only virtual network, for example client `192.168.56.10` and server `192.168.56.20`. Both need OpenSSH; only the server needs an SSH server service. On an Ubuntu/Debian lab server:

```bash
sudo apt-get update
sudo apt-get install openssh-server
sudo systemctl start ssh
```

Use an existing account on that server. From the client:

1. Start Wireshark on the host-only network interface before connecting. Capture filter: `host 192.168.56.20 and tcp port 22` (replace with your server IP).
2. Open a terminal in this question folder and run:

```bash
bash ssh_session.sh labuser 192.168.56.20
```

3. Verify the presented host-key fingerprint using the server console (`ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub`, if Ed25519 is the offered host key). Accept only the expected server; authenticate with its configured account.
4. After login, run `whoami`, `hostname`, and `exit`.
5. Stop capture and save `ssh.pcapng`. Display filter: `ssh` or `tcp.port == 22`. For one connection use `tcp.stream == N`.
6. Read `ssh-debug.log`. Locate lines containing `kex: algorithm`, `cipher`, `Authenticating`, and `Authenticated to`. Match their order with the packet trace and complete the observation table.

The log is generated locally and ignored by Git. Repeating the helper may append to the existing log; remove it before a new experiment if you want a clean record. A refused connection usually means the server service, address, or firewall needs checking. Permission denied means transport worked but account authentication failed.

If you started the SSH service only for this lab, stop it afterward with `sudo systemctl stop ssh`. Remove the capture and debug log when no longer needed. macOS can be the client; these service commands apply to the Linux server VM.

## References

[OpenSSH client manual](https://man.openbsd.org/ssh) documents the helper's flags and authentication. [Wireshark SSH fields](https://www.wireshark.org/docs/dfref/s/ssh.html) lists SSH display filters.
