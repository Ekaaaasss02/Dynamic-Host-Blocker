# main.py — the main loop

from log_parser  import tail_log
from detector    import check
from blocker     import block
from verifier    import is_blocked
from event_logger import log_event
from config      import LOG_FILE

already_blocked = set()

def handle_event(event):
    ip = event["ip"]
    should_block, reason = check(event)

    if should_block and ip not in already_blocked:
        print(f"\n[MAIN] ALERT: {ip} → {reason}")
        blocked   = block(ip)
        verified  = is_blocked(ip) if blocked else False
        log_event(ip, reason, verified)
        already_blocked.add(ip)

if __name__ == "__main__":
    print("[MAIN] Dynamic Host Blocking System started.")
    print(f"[MAIN] Monitoring: {LOG_FILE}")
    tail_log(LOG_FILE, handle_event)