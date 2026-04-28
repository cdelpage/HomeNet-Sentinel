import requests
from datetime import datetime, timezone

url = "http://127.0.0.1:8000/scan"
payload = {
    "sensor_id": "sensor_01",
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "scans": [
        {
            "bssid": "00:11:22:33:44:55",
            "ssid": "MyWiFiNetwork",
            "rssi": -55,
            "channel": 6,
            "encryption_type": "WPA2"
        }
    ]
}

response = requests.post(url, json=payload)
print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")
