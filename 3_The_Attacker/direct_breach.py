import requests
from colorama import init, Fore
import json

init(autoreset=True)

# 1. SETUP TARGET (MUST be the API, not the Dashboard HTML page)
TARGET_URL = "http://127.0.0.1:8000/api/v1/user/search"

print(Fore.YELLOW + f"⚔️  RUNNING TEST: [DATA BREACH] Target: {TARGET_URL}...")
print(Fore.YELLOW + "    Attempting to bypass WAF and inject SQL...")

try:
    # 2. THE ATTACK PAYLOAD
    # We send a SQL Injection query (' OR '1'='1)
    payload = {"query": "' OR '1'='1"}
    
    # We send it to the API
    r = requests.post(TARGET_URL, json=payload)
    
    # 3. CHECK RESULTS
    if r.status_code == 200:
        data = r.json()
        record_count = len(data) if isinstance(data, list) else 0
        
        print(Fore.RED + f"❌ [BREACH SUCCESSFUL] System Vulnerable!")
        print(Fore.RED + f"    Server returned {record_count} confidential records.")
        print(Fore.RED + f"    Status Code: {r.status_code}")
        
    elif r.status_code == 403:
        print(Fore.GREEN + f"✅ [TEST FAILED] WAF BLOCKED THE ATTACK.")
        print(Fore.GREEN + f"    Server said: {r.json().get('error')}")
        
    else:
        print(Fore.CYAN + f"⚠️  [UNKNOWN RESPONSE] Status: {r.status_code}")
        print(f"    Response: {r.text}")

except Exception as e:
    print(Fore.RED + f"Connection Failed: {e}")