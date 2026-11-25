import argparse
import json
import threading
from datetime import UTC, datetime, timedelta

import paho.mqtt.client as mqtt

parser = argparse.ArgumentParser(description="Publish a demo MQTT telemetry sequence")

parser.add_argument(
    "--device-id",
    default="sensor-001",
    help="Target device ID (default: sensor-001)",
)

args = parser.parse_args()

TOPIC = f"iot/devices/{args.device_id}/telemetry"
HOSTNAME = "127.0.0.1"
PORT = 1883

VALUES = [
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

connected = threading.Event()


def on_connect(client, userdata, flags, reason_code, properties):
    print(f"MQTT connection: {reason_code}")
    if reason_code == 0:
        connected.set()


client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect

try:
    client.connect(HOSTNAME, PORT, 60)
    client.loop_start()

    if not connected.wait(timeout=5):
        raise RuntimeError("Could not connect to MQTT broker")

    base_time = datetime.now(UTC) - timedelta(seconds=len(VALUES) - 1)

    for index, value in enumerate(VALUES):
        payload = {
            "metric_name": "temperature",
            "metric_value": value,
            "timestamp": (base_time + timedelta(seconds=index)).isoformat(),
        }

        info = client.publish(
            TOPIC,
            json.dumps(payload),
            qos=1,
        )
        info.wait_for_publish(timeout=5)

        if not info.is_published():
            raise RuntimeError(f"Publish failed: temperature={value}")

        print(f"Published temperature={value}")

finally:
    client.disconnect()
    client.loop_stop()
