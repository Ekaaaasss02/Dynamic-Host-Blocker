# 🛡️ Dynamic Host Blocking System

A Python-based Intrusion Prevention System that automatically detects suspicious network activity, blocks malicious hosts using firewall rules, verifies the blocks, and logs all events — in real time.

---

## 📌 Table of Contents

- [About the Project](#about-the-project)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Setup & Installation](#setup--installation)
- [How to Run](#how-to-run)
- [Expected Output](#expected-output)
- [Detection Rules](#detection-rules)
- [Event Log](#event-log)
- [Important Notes](#important-notes)
- [Author](#author)

---

## 📖 About the Project

In real networks, attackers perform activities like:
- Repeated failed SSH login attempts (brute force)
- Scanning multiple ports to find vulnerabilities (port scanning)
- Flooding a server with excessive requests (HTTP flood)

Normally, a network administrator would have to manually detect and block these attackers. This project automates that entire process.

The **Dynamic Host Blocking System** monitors traffic behavior, applies threshold-based detection, automatically installs firewall DROP rules using `iptables`, verifies the block is active, and maintains a complete audit trail in a SQLite database.

---

## ✅ Features

- 🔍 **Detect suspicious activity** — threshold-based detection per IP address
- 🚫 **Install blocking rules** — automatic `iptables` DROP rules for malicious IPs
- ✔️ **Verify blocking** — confirms firewall rule is active after each block
- 📋 **Log events** — full audit trail stored in SQLite with timestamps
- 🎮 **Traffic simulator** — generates realistic fake attack traffic for testing
- 🔐 **Whitelist support** — trusted IPs are never blocked
- 🔒 **Reserved port awareness** — only uses ports 1024–65535 (avoids OS-rejected reserved ports)

---

## 🏗️ System Architecture

```
Simulated Traffic
      │
      ▼
 Log Parser         ← watches log file in real time
      │
      ▼
Detection Engine    ← counts events per IP within time windows
      │
      ├──── Clean IP → no action
      │
      ▼ (suspicious)
   Blocker          ← runs: iptables -A INPUT -s <IP> -j DROP
      │
      ▼
  Verifier          ← confirms rule exists in iptables -L
      │
      ▼
 Event Logger       ← saves IP, reason, timestamp, verified → SQLite
```

---

## 📁 Project Structure

```
dynamic-host-blocker/
│
├── main.py                 ← Entry point, main detection loop
├── config.py               ← All thresholds, paths, and settings
├── traffic_simulator.py    ← Generates fake attack traffic for testing
├── log_parser.py           ← Reads and parses the log file in real time
├── detector.py             ← Detection engine with threshold logic
├── blocker.py              ← Applies and removes iptables firewall rules
├── verifier.py             ← Verifies that block rules are active
├── event_logger.py         ← Logs all events to SQLite database
├── simulated_traffic.log   ← Generated at runtime (auto-created)
├── events.db               ← SQLite event database (auto-created)
└── README.md
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python 3 | Core application logic |
| iptables | Linux firewall for blocking IPs |
| SQLite3 | Lightweight event log database |
| WSL2 / Ubuntu | Linux environment on Windows |

---

## ⚙️ Setup & Installation

### Prerequisites

- Ubuntu (or WSL2 on Windows)
- Python 3.x
- iptables (pre-installed on Ubuntu)
- sqlite3

### Install sqlite3

```bash
sudo apt update
sudo apt install sqlite3 -y
```

### Clone the Repository

```bash
git clone https://github.com/Ekaaaasss02/Dynamic-Host-Blocker.git
cd dynamic-host-blocker
```

---

## ▶️ How to Run

Open **3 separate terminal windows** and navigate to the project folder in each:

```bash
cd ~/path/to/dynamic-host-blocker
```

**Terminal 1 — Start the main blocker:**
```bash
sudo python3 main.py
```

**Terminal 2 — Start the traffic simulator:**
```bash
python3 traffic_simulator.py
```

**Terminal 3 — Watch the event log live:**
```bash
watch -n 2 'sqlite3 -column -header events.db "SELECT * FROM events;"'
```

**To verify firewall rules are installed (any terminal):**
```bash
sudo iptables -L INPUT -n
```

---

## 📊 Expected Output

**Terminal 2 — Simulator generating attacks:**
```
[SIM] Starting traffic simulation...
[SIM] Using only non-reserved ports (1024-65535)
[SIM] 2024-01-15 14:32:00 | 10.0.0.5  | ssh_fail   | port=2345
[SIM] 2024-01-15 14:32:01 | 10.0.0.66 | port_scan  | port=8080
[SIM] 2024-01-15 14:32:01 | 10.0.0.5  | ssh_fail   | port=5432
```

**Terminal 1 — System detecting and blocking:**
```
[MAIN] Dynamic Host Blocking System started.
[MAIN] Monitoring: simulated_traffic.log

[MAIN] ALERT: 10.0.0.5 → ssh_fail × 5 in 60s
[BLOCKER] Blocked 10.0.0.5
[VERIFIER] 10.0.0.5 rule status: CONFIRMED
[LOGGER] Logged → 2024-01-15 14:32:05 | 10.0.0.5 | ssh_fail × 5 in 60s | verified=1
```

**Terminal 3 — Event log database:**
```
id  timestamp            ip           reason                     verified
--  -------------------  -----------  -------------------------  --------
1   2024-01-15 14:32:05  10.0.0.5     ssh_fail × 5 in 60s        1
2   2024-01-15 14:32:18  10.0.0.66    port_scan × 10 in 10s      1
3   2024-01-15 14:32:44  172.16.0.99  http_flood × 100 in 60s    1
```

**Firewall rules (`sudo iptables -L INPUT -n`):**
```
Chain INPUT (policy ACCEPT)
target   prot opt source          destination
DROP     all  --  10.0.0.5        0.0.0.0/0
DROP     all  --  10.0.0.66       0.0.0.0/0
DROP     all  --  172.16.0.99     0.0.0.0/0
```

---

## 🔍 Detection Rules

| Attack Type | Threshold | Time Window |
|---|---|---|
| SSH brute force (`ssh_fail`) | 5 failed attempts | 60 seconds |
| Port scanning (`port_scan`) | 10 port hits | 10 seconds |
| HTTP flood (`http_flood`) | 100 requests | 60 seconds |

All thresholds are configurable in `config.py`.

---

## 🗃️ Event Log Schema

Events are stored in `events.db` (SQLite) with the following structure:

| Column | Type | Description |
|---|---|---|
| id | INTEGER | Auto-increment primary key |
| timestamp | TEXT | Date and time of the block |
| ip | TEXT | The blocked IP address |
| reason | TEXT | Why it was blocked |
| verified | INTEGER | 1 = block confirmed, 0 = failed |

---

## ⚠️ Important Notes

- `sudo` is required for `main.py` because iptables needs root privileges
- The system only blocks ports **1024 and above** — reserved ports (1–1023) are excluded because the OS rejects those connections before they reach the application, which would cause false positives in detection
- IPs in the `WHITELIST` inside `config.py` are never blocked
- The log file (`simulated_traffic.log`) and database (`events.db`) are auto-created on first run
- This project is built for **educational purposes** in a lab/test environment

---

## 👤 Author

**Bismun Singh**  
