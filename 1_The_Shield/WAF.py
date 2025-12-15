from flask import Flask, request, jsonify
import requests
import json
import os
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# --- CONFIGURATION ---
ORIGIN_URL = "http://127.0.0.1:5000"
BLOCKLIST_FILE = "geo_blocklist.json"
SIGNATURE_FILE = "attack_signatures.txt"

# --- DATABASE CONFIGURATION ---
DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'abcd1234',  # <--- 🔴 PUT YOUR ACTUAL PASSWORD HERE
    'database': 'cyber_hackathon'
}

# --- LOAD ASSETS ---
def load_signatures():
    if not os.path.exists(SIGNATURE_FILE): return []
    with open(SIGNATURE_FILE, "r") as f:
        return [line.strip().lower() for line in f if line.strip()]

def load_blocklist():
    if not os.path.exists(BLOCKLIST_FILE): return []
    with open(BLOCKLIST_FILE, "r") as f:
        return json.load(f)

ATTACK_SIGNATURES = load_signatures()
GEO_BLOCKLIST = load_blocklist()

# --- HELPER: LOG THREAT TO MARIADB ---
def log_threat_to_db(title, description, ip_address, country):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # SQL Query matching your 'incidents' table structure
        sql = """
            INSERT INTO incidents 
            (title, description, status, risk_score, ip_address, country, system_id, incident_type_id, reported_at) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        # Data to insert
        val = (
            title,              # title
            description,        # description
            "open",             # status (matches your DB logs)
            80,                 # risk_score (High risk, even if blocked)
            ip_address,         # ip_address
            country,            # country
            1,                  # system_id (matches your DB logs)
            1,                  # incident_type_id (1 seems to be for blocked/access attempts)
            datetime.now()      # reported_at
        )
        
        cursor.execute(sql, val)
        conn.commit()
        cursor.close()
        conn.close()
        print(f"📝 Incident logged to MariaDB: {title}")
        
    except mysql.connector.Error as err:
        print(f"⚠️ DATABASE ERROR: {err}")
    except Exception as e:
        print(f"⚠️ LOGGING ERROR: {e}")

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(path):
    print(f"🛡️  WAF received request for: /{path}")
    
    client_ip = request.remote_addr
    
    # --- LAYER 1: SIGNATURE DETECTION ---
    if request.args:
        query_str = str(request.args).lower()
        for sig in ATTACK_SIGNATURES:
            if sig in query_str:
                print(f"🚫 BLOCKING ATTACK: Signature detected -> {sig}")
                
                # ✅ LOG TO DATABASE
                log_threat_to_db(
                    title=f"🛡️ BLOCKED: Malicious Signature",
                    description=f"WAF blocked query containing signature: {sig}",
                    ip_address=client_ip,
                    country="Unknown"
                )
                
                return jsonify({"error": f"WAF BLOCKED: Malicious Signature ({sig})"}), 403

    # --- LAYER 2: GEO-BLOCKING ---
    country = request.headers.get('X-Country', 'Unknown')
    if country in GEO_BLOCKLIST:
        print(f"🚫 BLOCKING ORIGIN: {country} is in blocklist.")
        
        # ✅ LOG TO DATABASE
        log_threat_to_db(
            title=f"🛡️ BLOCKED: Geo-Restricted Access",
            description=f"WAF blocked connection from restricted country: {country}",
            ip_address=client_ip,
            country=country
        )
        
        return jsonify({"error": f"WAF BLOCKED: Access denied from {country}"}), 403

    # --- LAYER 3: FORWARD TO VAULT ---
    try:
        forward_headers = {key: value for (key, value) in request.headers if key != 'Host'}
        forward_headers['X-AEGIS-Key'] = "TopSecret-Handshake-2025"

        resp = requests.request(
            method=request.method,
            url=f"{ORIGIN_URL}/{path}",
            headers=forward_headers,
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False,
            params=request.args
        )
        return (resp.content, resp.status_code, resp.headers.items())
        
    except requests.exceptions.ConnectionError:
        return jsonify({"error": "The Vault is OFFLINE"}), 503

if __name__ == '__main__':
    print(f"🛡️  AEGIS SHIELD ACTIVE (Port 8000)")
    print(f"   - Connected to DB: {DB_CONFIG['database']}")
    app.run(port=8000, debug=True)