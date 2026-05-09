import paho.mqtt.publish as publish

publish.single(
    topic="iot/devices/sensor-001/telemetry",
    payload="""
    {
        "metric_name": "temperature",
        "metric_value": 42.5,
        "timestamp": "2026-05-09T12:00:00Z"
    }
    """,
    hostname="127.0.0.1",
    port=1883,
)

print("Message published")