import time, random, datetime
from config import LOG_FILE

ATTACK_IPS = ["10.0.0.5", "10.0.0.66", "172.16.0.99"]
NORMAL_IPS = ["192.168.1.10", "192.168.1.20"]

SAFE_PORTS = range(1024, 65535) 


def write_event(ip, event_type, detail=""):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"{ts} | {ip} | {event_type} | {detail}\n"
    with open(LOG_FILE, "a") as f:
        f.write(line)
    print(f"[SIM] {line.strip()}")

def simulate():
    print("[SIM] Starting traffic simulation...")
    print("[SIM] Using only non-reserved ports (1024-65535)")
    while True:
        ip = random.choice(ATTACK_IPS)
        event = random.choice(["ssh_fail", "port_scan", "http_flood"])
        port = random.randint(1024, 65535)
        write_event(ip, event, f"port={port}")
        time.sleep(random.uniform(0.3, 1.2))

if __name__ == "__main__":
    simulate()
