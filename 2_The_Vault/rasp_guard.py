from functools import wraps
from flask import request, jsonify
from datetime import datetime
import mysql.connector

# Database Config (To log the RASP Alert to dashboard)
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'abcd1234',  # Check your password
    'database': 'cyber_hackathon'
}

def log_rasp_incident(client_ip):
    """Logs that RASP blocked an attack so Dashboard can show 'ACCESS DENIED'"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        sql = """INSERT INTO incidents 
                 (title, description, risk_score, ip_address, country, system_id, incident_type_id, reported_at) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        val = (
            "⚡ RASP ALERT: ATTACK BLOCKED", 
            "Deception Protocol Initiated. Fake credentials sent to attacker.", 
            0, # Score 0 means 'Secure' but we use it to trigger the UI alert
            client_ip, "Unknown", 1, 2, datetime.now()
        )
        cursor.execute(sql, val)
        conn.commit()
        conn.close()
    except:
        pass

def rasp_shield(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 1. INSPECT THE INPUT
        data = request.json or {}
        input_data = str(data).lower()
        
        # 2. DEFINE ATTACK PATTERNS (The "Bad Intent")
        sql_signatures = ["or '1'='1", "union select", "drop table", "sleep("]
        logic_signatures = ["init_overload_sequence"]

        # 3. DETECT & DECEIVE
        is_attack = any(sig in input_data for sig in sql_signatures)
        is_logic_bomb = any(sig in input_data for sig in logic_signatures)

        if is_attack or is_logic_bomb:
            client_ip = request.remote_addr
            print(f"⚡ RASP INTERCEPT: Malicious payload detected from {client_ip}")
            
            # A. Log the event so Dashboard knows to show "Access Denied"
            log_rasp_incident(client_ip)

            # B. THE DECEPTION (Return Fake Data instead of Blocking)
            # This makes the attacker think they succeeded!
            fake_response = [
                {"id": 901, "username": "sys_admin", "password": "super_secret_password_123"},
                {"id": 902, "username": "honeypot_user", "password": "password1"}
            ]
            return jsonify(fake_response), 200

        # 4. IF CLEAN, LET IT PASS
        return f(*args, **kwargs)
        
    return decorated_function