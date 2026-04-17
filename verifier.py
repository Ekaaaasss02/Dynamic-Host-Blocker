# verifier.py — confirms the iptables rule is actually active

import subprocess

def is_blocked(ip):
    """Returns True if DROP rule exists for this IP."""
    try:
        result = subprocess.run(
            ["iptables", "-L", "INPUT", "-n"],
            capture_output=True, text=True, check=True
        )
        blocked = ip in result.stdout
        status  = "CONFIRMED" if blocked else "MISSING"
        print(f"[VERIFIER] {ip} rule status: {status}")
        return blocked
    except subprocess.CalledProcessError as e:
        print(f"[VERIFIER] ERROR checking rules: {e.stderr}")
        return False