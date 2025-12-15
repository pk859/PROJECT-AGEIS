from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import mariadb
import sys
import requests
import pandas as pd
from database_config import db_config
from rasp_guard import rasp_shield

# --- CONFIGURATION ---
app = Flask(__name__, template_folder='templates', static_folder='Frontend', static_url_path='/Frontend')
CORS(app)

# The "Shield" Secret Key
WAF_SECRET = "TopSecret-Handshake-2025"

# Global Health State (100 = Healthy, 50 = Data Leaking, 0 = System Crash)
SERVER_HEALTH = 100

# --- DB CONNECTION ---
def get_db_connection():
    try:
        conn = mariadb.connect(**db_config)
        return conn
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB: {e}")
        return None

# --- HELPER: INCIDENT LOGGER ---
# This ensures every event appears on your Tracker Console
def log_incident(title, description, risk, incident_type, client_ip):
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            country = "Unknown" 
            # Simple Geo-IP (Optional, keeps it fast)
            try:
                # You can uncomment this if you have internet access for real countries
                # geo = requests.get(f'http://ip-api.com/json/{client_ip}?fields=country', timeout=1).json()
                # country = geo.get('country', 'Unknown')
                pass
            except: pass

            sql = """INSERT INTO incidents (title, description, system_id, incident_type_id, risk_score, ip_address, country)
                     VALUES (?, ?, ?, ?, ?, ?, ?)"""
            cursor.execute(sql, (title, description, 1, incident_type, risk, client_ip, country))
            conn.commit()
            conn.close()
    except Exception as e:
        print(f"Logging Error: {e}")

# ======================================================
# 🚀 ROUTE 1: LOGIN PAGE (Root)
# ======================================================
@app.route('/')
def login_page():
    # >>> ADD THESE 2 LINES <<<
    global SERVER_HEALTH
    SERVER_HEALTH = 100  # Reset health to 100% whenever we visit login
    
    return render_template('login.html')
# ======================================================
# 🚀 ROUTE 2: DASHBOARD (Protected View)
# ======================================================
@app.route('/dashboard')
def company_portal():
    return render_template('company_portal.html')

# ======================================================
# 🚀 ROUTE 3: LOGIN API (THE TRAP)
# ======================================================
@app.route('/api/login', methods=['POST'])
def handle_login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    client_ip = request.remote_addr
    
    # 1. REAL LOGIN
    if username == "prateek" and password == "root":
        return jsonify({"status": "success", "redirect": "/dashboard"}), 200
    
    # 2. HONEYPOT TRAP (Catching the attacker using fake creds)
    elif username == "sys_admin" and password == "super_secret_password_123":
        # Log this capture to the database!
        log_incident(
            "🪤 HONEYPOT TRIGGERED", 
            f"Attacker caught using fake credentials! IP: {client_ip}", 
            100, 3, client_ip
        )
        return jsonify({"error": "ACCOUNT LOCKED: SUSPICIOUS ACTIVITY DETECTED"}), 401
        
    # 3. STANDARD FAILURE
    else:
        return jsonify({"error": "INVALID CREDENTIALS"}), 401
    

# ======================================================
# 🚀 ROUTE 4: SYSTEM HEALTH CHECK (For Dashboard JS)
# ======================================================
@app.route('/health')
def health_check():
    return jsonify({"health": SERVER_HEALTH})

# ======================================================
# 🛑 VULNERABILITY 1: DATA BREACH (SQL INJECTION)
# Target URL: http://127.0.0.1:5000/api/v1/user/search
# ======================================================
@app.route('/api/v1/user/search', methods=['POST'])
@rasp_shield
def user_search():
    global SERVER_HEALTH
    data = request.json
    search_term = data.get('query', '')
    client_ip = request.remote_addr

    # 1. WAF CHECK (The Shield)
    auth_header = request.headers.get('X-AEGIS-Key')
    
    # If WAF Key is present, we filter attacks
    if auth_header == WAF_SECRET:
        if "'" in search_term or "OR" in search_term:
            # LOG BLOCKED ATTEMPT
            log_incident("🛡️ WAF: SQL Injection Blocked", f"Blocked query: {search_term}", 60, 2, client_ip)
            return jsonify({"error": "Illegal characters detected. Access Denied."}), 403

    # 2. VULNERABLE PATH (WAF Bypassed)
    conn = get_db_connection()
    if not conn: return jsonify({"error": "DB Offline"}), 500
    cursor = conn.cursor()
    
    try:
        # RAW F-STRING SQL INJECTION
        unsafe_sql = f"SELECT * FROM incidents WHERE title LIKE '%{search_term}%'"
        print(f"⚠️  EXECUTING UNSAFE SQL: {unsafe_sql}")
        
        cursor.execute(unsafe_sql)
        results = cursor.fetchall()
        
        # LOG SUCCESSFUL BREACH (Regardless of result count)
        print("⚠️  DATA BREACH SUCCESSFUL")
        SERVER_HEALTH = 50 
        log_incident(
            "⚠️ CRITICAL: DATA BREACH", 
            f"Attacker executed SQL Injection: {search_term}", 
            95, 
            3, 
            client_ip
        )

        conn.close()
        return jsonify(results), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ======================================================
# 🛑 VULNERABILITY 2: SERVER CRASH (LOGIC BOMB)
# Target URL: http://127.0.0.1:5000/api/v1/system/diagnostics
# ======================================================
@app.route('/api/v1/system/diagnostics', methods=['POST'])
@rasp_shield
def system_diagnostics():
    global SERVER_HEALTH
    client_ip = request.remote_addr
    
    # 1. WAF CHECK
    auth_header = request.headers.get('X-AEGIS-Key')
    
    if auth_header == WAF_SECRET:
        # LOG BLOCKED ATTEMPT
        log_incident("🛡️ WAF: Blocked RCE Attempt", "Malicious diagnostics command blocked.", 80, 2, client_ip)
        return jsonify({"status": "blocked", "message": "Malicious payload detected by AEGIS WAF."}), 403

    # 2. VULNERABLE PATH
    data = request.json
    command = data.get('command', '')

    if command == "INIT_OVERLOAD_SEQUENCE":
        print(f"⚠️ CRITICAL: LOGIC BOMB DETECTED from {client_ip}")
        SERVER_HEALTH = 0
        
        # LOG SUCCESSFUL CRASH
        log_incident("⚠️ CRITICAL: SYSTEM FAILURE", "Remote Code Execution (RCE) Successful. System Halted.", 100, 3, client_ip)
        
        return jsonify({"error": "CRITICAL_FAILURE", "code": "0xDEADBEEF"}), 200
    
    return jsonify({"status": "ignored"}), 400

# ======================================================
# 🚀 ROUTE 5: INCIDENT FEED (For Tracker Console)
# ======================================================
@app.route('/incidents', methods=['GET'])
def get_incidents():
    try:
        conn = get_db_connection()
        # Fetch data for the Tracker Table
        query = """
            SELECT i.id, i.title, i.status, i.risk_score, i.reported_at, 
                   s.name as system_name, it.name as incident_type,
                   i.ip_address, i.country
            FROM incidents i
            JOIN systems s ON i.system_id = s.id
            JOIN incident_types it ON i.incident_type_id = it.id
            ORDER BY i.reported_at DESC LIMIT 15;
        """
        df = pd.read_sql(query, conn)
        conn.close()
        df['reported_at'] = df['reported_at'].astype(str)
        df.fillna('N/A', inplace=True)
        return df.to_json(orient="records"), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("--------------------------------------------------")
    print("🔒 AEGIS SERVER ONLINE")
    print(f"👉 LOGIN:     http://127.0.0.1:5000/")
    print("--------------------------------------------------")
    app.run(port=5000, debug=True)