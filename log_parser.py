# log_parser.py — reads the log file and returns structured events

import time

def parse_line(line):
    """Parse one log line → dict or None."""
    try:
        parts = [p.strip() for p in line.strip().split("|")]
        return {
            "timestamp": parts[0],
            "ip":        parts[1],
            "event":     parts[2],
            "detail":    parts[3] if len(parts) > 3 else ""
        }
    except Exception:
        return None

def tail_log(log_file, callback):
    """Continuously watch a log file and call callback(event) per new line."""
    print(f"[PARSER] Watching {log_file}")
    with open(log_file, "a"):   # create if missing
        pass
    with open(log_file, "r") as f:
        f.seek(0, 2)            # jump to end
        while True:
            line = f.readline()
            if line:
                event = parse_line(line)
                if event:
                    callback(event)
            else:
                time.sleep(0.5)