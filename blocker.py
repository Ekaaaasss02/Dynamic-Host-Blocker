# blocker.py — applies and removes iptables rules

import subprocess

_blocked = set()

def block(ip):
    if ip in _blocked:
        print(f"[BLOCKER] {ip} already blocked, skipping.")
        return True
    try:
        subprocess.run(
            ["iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"],
            check=True, capture_output=True
        )
        _blocked.add(ip)
        print(f"[BLOCKER] Blocked {ip}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[BLOCKER] ERROR blocking {ip}: {e.stderr.decode()}")
        return False

def unblock(ip):
    try:
        subprocess.run(
            ["iptables", "-D", "INPUT", "-s", ip, "-j", "DROP"],
            check=True, capture_output=True
        )
        _blocked.discard(ip)
        print(f"[BLOCKER] Unblocked {ip}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[BLOCKER] ERROR unblocking {ip}: {e.stderr.decode()}")
        return False

def list_blocked():
    return list(_blocked)