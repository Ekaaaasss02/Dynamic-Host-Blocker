# detector.py — counts events per IP, triggers on threshold breach

import time
from collections import defaultdict
from config import THRESHOLDS, WHITELIST

# ip → event_type → list of timestamps
_tracker = defaultdict(lambda: defaultdict(list))

def _clean_old(timestamps, window):
    now = time.time()
    return [t for t in timestamps if now - t < window]

def check(event):
    """Returns (should_block: bool, reason: str)."""
    ip         = event["ip"]
    event_type = event["event"]

    if ip in WHITELIST:
        return False, ""

    if event_type not in THRESHOLDS:
        return False, ""

    cfg = THRESHOLDS[event_type]
    ts_list = _tracker[ip][event_type]
    ts_list = _clean_old(ts_list, cfg["window"])
    ts_list.append(time.time())
    _tracker[ip][event_type] = ts_list

    if len(ts_list) >= cfg["count"]:
        reason = f"{event_type} × {len(ts_list)} in {cfg['window']}s"
        return True, reason

    return False, ""