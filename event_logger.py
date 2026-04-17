# event_logger.py — logs all block events to SQLite

import sqlite3, datetime
from config import DB_FILE

def _connect():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            ip        TEXT,
            reason    TEXT,
            verified  INTEGER
        )
    """)
    conn.commit()
    return conn

def log_event(ip, reason, verified):
    conn = _connect()
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn.execute(
        "INSERT INTO events (timestamp, ip, reason, verified) VALUES (?,?,?,?)",
        (ts, ip, reason, int(verified))
    )
    conn.commit()
    conn.close()
    print(f"[LOGGER] Logged → {ts} | {ip} | {reason} | verified={verified}")

def print_all():
    conn = _connect()
    rows = conn.execute("SELECT * FROM events ORDER BY id DESC").fetchall()
    conn.close()
    print("\n--- Event Log ---")
    for row in rows:
        print(row)