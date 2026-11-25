import time
from datetime import UTC, datetime, timedelta

import requests

API_URL = "http://127.0.0.1:8000/api/v1/telemetry"
DEVICE_ID = 1

values = [
    40.0,
    41.0,
    42.0,
    41.5,
    42.2,
    40.8,
    43.0,
    41.7,
    42.1,
    120.0,
    41.9,
    42.4,
    39.8,
    130.0,
    41.2,
]

base_time = datetime.now(UTC)

for index, value in enumerate(values):
    payload = {
        "device_id": DEVICE_ID,
        "metric_name": "temperature",
        "metric_value": value,
        "timestamp": (base_time + timedelta(seconds=index)).isoformat(),
    }

    response = requests.post(API_URL, json=payload, timeout=5)
    response.raise_for_status()

    print(f"Published temperature={value}")

    time.sleep(0.5)