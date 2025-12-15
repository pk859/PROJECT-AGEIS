import sys
import datetime

def block_ip_address(ip_address):
    """
    Simulates blocking an IP by writing it to a blocklist file.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{ip_address} blocked on {timestamp}\n"

    # Write to a file in the parent directory so the Shield can see it (Optional)
    # For now, we write it locally to simulate the firewall action
    with open("firewall_blocklist.txt", "a") as f:
        f.write(log_entry)

    print(f"🔥 SOAR ACTION TRIGGERED: {ip_address} added to Firewall Blocklist.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        block_ip_address(sys.argv[1])