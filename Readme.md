# Project AEGIS - Adaptive Enterprise Guard & Intelligent Shield

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python) ![Flask](https://img.shields.io/badge/Flask-2.0-black?logo=flask) ![MariaDB](https://img.shields.io/badge/MariaDB-10.6%2B-blue?logo=mariadb) ![Security](https://img.shields.io/badge/Security-RASP%20%2B%20WAF-green) ![JavaScript](https://img.shields.io/badge/JavaScript-ES6%2B-yellow?logo=javascript)

A next-generation "Purple Team" cybersecurity simulation demonstrating the limitations of perimeter firewalls and the power of Runtime Application Self-Protection (RASP) with active deception technology.

---

## Live Demo
> "The firewall is just the first line of defense. The real battle happens inside."

**Accessing The Vault Mainframe...**
**Credentials Verified.**

Watch the AEGIS protocol in action: detecting anomalies, neutralizing threats in memory, and deploying active deception.

https://github.com/user-attachments/assets/8909933a-ccab-4bcd-b53d-71db839195eb




---

## Introduction

In traditional cybersecurity, organizations rely heavily on "Perimeter Defense" (Firewalls/WAFs) to keep attackers out. But what happens when the firewall fails, or the threat is already inside? **Project AEGIS** was built to answer this question.

This project simulates a realistic banking infrastructure ("The Vault") where a sophisticated attacker bypasses the outer Web Application Firewall (WAF) using direct-access techniques. However, instead of succeeding, the attacker is neutralized by an internal **Runtime Application Self-Protection (RASP)** system. The system doesn't just block the attack it deploys a **Honeypot**, feeding the attacker fake credentials to deceive them while logging their forensic data.

---

## Key Features

This project demonstrates a full "Cyber Kill Chain" simulation with advanced defensive countermeasures:

* ** Custom Web Application Firewall (WAF):** A Python-based perimeter shield running on Port 8000. It uses signature-based detection to identify and block common SQL Injection (`OR 1=1`) and Remote Code Execution payloads before they reach the application.

* ** Runtime Application Self-Protection (RASP):** The core innovation of AEGIS. Unlike a firewall, this internal protection system hooks into the application's memory. It detects malicious logic *during execution*, offering protection even if the firewall is completely bypassed.

* ** Active Deception (Honeypot):** Instead of simply blocking a detected intruder, the system serves them plausible but fake data (e.g., `sys_admin` credentials). This wastes the attacker's time and tricks them into revealing their techniques without compromising real data.

* ** Automated "Smart Breach" Protocol:** A custom Red Team script (`smart_breach.py`) that intelligently probes the network. It attempts to attack the Firewall first, and upon failure, automatically shifts tactics to exploit open backdoors (Port 5000).

* ** Live Command Dashboard:** A real-time web interface that visualizes the battle. It displays system health, attack geolocation, and flashes alerts when the RASP system intercepts a threat.

---

##  Technology Stack

| Category | Technology |
| :--- | :--- |
| **Backend** | Python, Flask, Requests, Colorama |
| **Frontend** | HTML5, CSS3 (Rajdhani Theme), JavaScript Fetch API |
| **Database** | MariaDB / MySQL (Dual tables: Real vs. Honeypot) |
| **Tooling** | Git, Python `venv`, Decorator Design Pattern |

---

##  System Architecture

The application follows a "Defense-in-Depth" workflow with two distinct attack paths:

**Scenario A: The Frontal Assault (Blocked)**
`Attacker Script` → `Port 8000 (WAF)` → `Signature Match` → 🔴 **403 FORBIDDEN**

**Scenario B: The Bypass & Trap (Deception)**
`Attacker Script` → `Port 5000 (Direct Access)` → `Application Logic` → `RASP Hook (@rasp_shield)` → 🟢 **Fake Data Returned (Honeypot)**

---

##  Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites
* Python 3.x
* MariaDB Server or MySQL Server
* Git

### Installation & Setup

1.  **Clone the repository:**
    ```sh
    git clone [https://github.com/pk859/Project-AEGIS.git](https://github.com/pk859/Project-AEGIS.git)
    cd Project-AEGIS
    ```

2.  **Set up the Python backend:**
    ```sh
    # Create and activate a virtual environment
    python -m venv venv
    .\venv\Scripts\activate  # On Windows
    # source venv/bin/activate # On macOS/Linux

    # Install required packages
    pip install -r requirements.txt
    ```

3.  **Set up the database:**
    * Connect to your MariaDB/MySQL server.
    * Update `database_config.py` with your credentials.
    * Run the setup script to create the real and fake users:
    ```sh
    python setup_users.py
    ```

4.  **Run the Simulation:**
    * **Terminal 1 (The Vault):** Start the App & RASP.
        ```sh
        cd 2_The_Vault
        python app.py
        ```
    * **Terminal 2 (The Shield):** Start the Firewall.
        ```sh
        cd 1_The_Shield
        python WAF.py
        ```
    * **Terminal 3 (The Attacker):** Run the Breach Protocol.
        ```sh
        cd 3_The_Attacker
        python smart_breach.py
        ```

---

##  Future Scope

This project provides a strong foundation for a commercial-grade security tool. Future enhancements could include:
* **AI Anomaly Detection:** Implement Machine Learning to detect attacks based on behavioral patterns rather than static signatures.
* **Adaptive Immunity:** Create a feedback loop where the RASP system automatically updates the Firewall's blocklist after detecting a new threat.
* **Automated Forensics:** Generate PDF incident reports containing the attacker's IP, timestamp, and used payload for legal evidence.

---
⚠️ CLASSIFIED FOOTNOTE
This project demonstrates the shift from "Fortress Security" to "Zero Trust Architecture." By assuming the network is already compromised, AEGIS proves that Resilience > Prevention.
