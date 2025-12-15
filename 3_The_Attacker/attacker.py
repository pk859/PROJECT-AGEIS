import requests
import time
import random

# ATTACKING THE SHIELD (Port 8000), NOT THE VAULT (Port 5000)
API_URL = "http://127.0.0.1:8000/incidents"

scenarios = [
    {"title": "SQL Injection Attempt", "system_id": 1, "incident_type_id": 3, "description": "User tried ' OR 1=1"},
    {"title": "Valid Login", "system_id": 2, "incident_type_id": 1, "description": "User logged in successfully"}
]

print("⚔️  ATTACKER SIMULATION STARTED (Targeting WAF Port 8000)...")

while True:
    data = random.choice(scenarios)
    # Fake IP generation
    data["ip_address"] = f"192.168.1.{random.randint(1,255)}"
    
    try:
        resp = requests.post(API_URL, json=data)
        
        if resp.status_code == 201:
            print(f"✅ [ALLOWED] {data['title']} passed through WAF.")
        elif resp.status_code == 403:
            print(f"🛡️ [BLOCKED] {data['title']} stopped by WAF.")
        else:
            print(f"⚠️  [STATUS {resp.status_code}] Unexpected response.")
            
    except Exception as e:
        print(f"❌ Connection Error: {e}")
    
    time.sleep(2)