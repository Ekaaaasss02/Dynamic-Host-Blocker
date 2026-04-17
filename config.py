LOG_FILE = "simulated_traffic.log"
DB_FILE  = "events.db"

THRESHOLDS = {
    "ssh_fail":   {"count": 5,   "window": 60},
    "port_scan":  {"count": 10,  "window": 10},
    "http_flood": {"count": 100, "window": 60},
}

WHITELIST = ["127.0.0.1", "192.168.1.1"]
