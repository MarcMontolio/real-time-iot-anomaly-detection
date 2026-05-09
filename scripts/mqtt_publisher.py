import json
import time

import paho.mqtt.client as mqtt


BROKER = "127.0.0.1"
PORT = 1883
TOPIC = "iot/devices/sensor-001/telemetry"

payload = {
    "metric_name": "temperature",
    "metric_value": 42.5,
    "timestamp": "2026-05-09T12:00:00Z",
}

client = mqtt.Client()

client.connect(BROKER, PORT, 60)
client.loop_start()

time.sleep(1)

result = client.publish(TOPIC, json.dumps(payload))
result.wait_for_publish()

print("Message published")

client.loop_stop()
client.disconnect()