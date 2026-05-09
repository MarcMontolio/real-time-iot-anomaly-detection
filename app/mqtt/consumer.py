import asyncio

import paho.mqtt.client as mqtt

from app.db.session import AsyncSessionLocal
from app.mqtt.ingestion import ingest_mqtt_telemetry_message


BROKER = "127.0.0.1"
PORT = 1883
TOPIC = "iot/devices/+/telemetry"


async def handle_message(topic: str, payload: str) -> None:
    async with AsyncSessionLocal() as session:
        await ingest_mqtt_telemetry_message(
            session,
            topic,
            payload,
        )
        

def on_connect(
    client: mqtt.Client,
    userdata: object | None,
    flags: dict[str, int],
    rc: int
) -> None:
    print(f"Connected with result code {rc}")
    
    client.subscribe(TOPIC)
    
    print(f"Subscribed to {TOPIC}")
    

def on_message(
    client: mqtt.Client,
    userdata: object | None,
    msg: mqtt.MQTTMessage
) -> None:
    topic = msg.topic
    
    payload = msg.payload.decode()
    
    print(f"Received message on {topic}")
    
    try:
        asyncio.run(handle_message(topic, payload))
    except ValueError as error:
        print(f"Failed to process MQTT message: {error}")
    

def start_consumer() -> None:
    client = mqtt.Client()
    
    client.on_connect = on_connect
    client.on_message = on_message
    
    client.connect(BROKER, PORT, 60)
    
    client.loop_forever()
