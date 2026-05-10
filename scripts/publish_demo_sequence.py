import json
import time
from datetime import UTC, datetime, timedelta

import paho.mqtt.publish as publish


TOPIC = "iot/devices/sensor-001/telemetry"
HOSTNAME = "127.0.0.1"
PORT = 1883

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
        "metric_name": "temperature",
        "metric_value": value,
        "timestamp": (base_time + timedelta(seconds=index)).isoformat(),
    }

    publish.single(
        topic=TOPIC,
        payload=json.dumps(payload),
        hostname=HOSTNAME,
        port=PORT,
    )

    print(f"Published temperature={value}")

    time.sleep(1.5)