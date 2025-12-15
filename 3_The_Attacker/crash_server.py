import requests
from colorama import init, Fore
import time

init(autoreset=True)

# 1. TARGET THE NEW API
TARGET_URL = "http://127.0.0.1:8000/api/v1/system/diagnostics"

print(Fore.RED + "☠️  HACKER TOOLKIT: SERVER KILLER")
print(Fore.RED + f"    Targeting: {TARGET_URL}")
print(Fore.RED + "    Sending Malicious Payload...")

try:
    # 2. THE CORRECT PAYLOAD (Must match app.py exactly)
    # The server only crashes if it sees "INIT_OVERLOAD_SEQUENCE"
    payload = {"command": "INIT_OVERLOAD_SEQUENCE"}
    
    # Send POST request
    r = requests.post(TARGET_URL, json=payload)
    
    # 3. CHECK RESPONSE
    if r.status_code == 200:
        print(Fore.GREEN + "💥 [SUCCESS] TARGET SYSTEM CRASHED!")
        print(Fore.GREEN + "    Server Health dropped to 0%.")
        print(Fore.GREEN + f"    Response Code: {r.status_code}")
    elif r.status_code == 403:
        print(Fore.YELLOW + "🛡️ [BLOCKED] WAF Stopped the Attack.")
    else:
        print(Fore.YELLOW + f"⚠️  [FAIL] Server Response: {r.json()}")

except Exception as e:
    print(f"Error: {e}")