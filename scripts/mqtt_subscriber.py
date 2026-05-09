import paho.mqtt.client as mqtt


BROKER = "127.0.0.1"
PORT = 1883
TOPIC = "iot/devices/+/telemetry"


def on_connect(
    client: mqtt.Client,
    userdata,
    flags,
    rc,
) -> None:
    print(f"Connected with result code {rc}")

    client.subscribe(TOPIC)

    print(f"Subscribed to {TOPIC}")


def on_message(
    client: mqtt.Client,
    userdata: object,
    msg: mqtt.MQTTMessage,
) -> None:
    payload = msg.payload.decode()

    print(f"[{msg.topic}] {payload}")


client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

print("Connecting to broker...")
client.connect(BROKER, PORT, 60)
print("Connected call returned, waiting for messages...")

print("Starting MQTT loop...")
client.loop_forever()
print("This should never print")