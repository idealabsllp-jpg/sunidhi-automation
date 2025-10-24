import requests
import os
from datetime import datetime

# Get the health URL from environment variable
HEALTH_URL = os.environ.get("HEALTH_URL", "http://localhost:5000/health")

try:
    response = requests.get(HEALTH_URL, timeout=5)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if response.status_code == 200:
        print(f"[{timestamp}] ✅ Heartbeat successful - App is alive!")
    else:
        print(f"[{timestamp}] ⚠️ Heartbeat returned status {response.status_code}")
except Exception as e:
    print(f"❌ Heartbeat failed: {e}")
Add heartbeat keep-alive script
