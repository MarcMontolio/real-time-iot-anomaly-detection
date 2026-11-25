import asyncio
from concurrent.futures import Future
from dataclasses import dataclass

import paho.mqtt.client as mqtt

from app.db.session import AsyncSessionLocal
from app.mqtt.ingestion import ingest_mqtt_telemetry_message

BROKER = "127.0.0.1"
PORT = 1883
TOPIC = "iot/devices/+/telemetry"


@dataclass(slots=True)
class MQTTContext:
    loop: asyncio.AbstractEventLoop
    queue: asyncio.Queue[tuple[str, str]]


async def handle_message(topic: str, payload: str) -> None:
    async with AsyncSessionLocal() as session:
        await ingest_mqtt_telemetry_message(session, topic, payload)


async def process_message_queue(
    queue: asyncio.Queue[tuple[str, str]],
) -> None:
    while True:
        topic, payload = await queue.get()

        try:
            await handle_message(topic, payload)
        except Exception as error:  # noqa: BLE001
            print(f"Failed to process MQTT message: {error}")
        finally:
            queue.task_done()


def on_connect(
    client: mqtt.Client,
    userdata: object | None,
    flags: dict[str, int],
    rc: int,
) -> None:
    print(f"Connected with result code {rc}")
    if rc == 0:
        client.subscribe(TOPIC)
        print(f"Subscribed to {TOPIC}")


def _log_message_result(future: Future[None]) -> None:
    try:
        future.result()
    except Exception as error:  # noqa: BLE001
        print(f"Failed to enqueue MQTT message: {error}")


def on_message(
    client: mqtt.Client,
    userdata: object | None,
    msg: mqtt.MQTTMessage,
) -> None:
    if not isinstance(userdata, MQTTContext):
        print("MQTT message received without an active application context")
        return

    topic = msg.topic
    payload = msg.payload.decode()

    print(f"Received message on {topic}")

    future = asyncio.run_coroutine_threadsafe(
        userdata.queue.put((topic, payload)),
        userdata.loop,
    )
    future.add_done_callback(_log_message_result)


def start_consumer_background(
    loop: asyncio.AbstractEventLoop,
    queue: asyncio.Queue[tuple[str, str]],
) -> mqtt.Client:
    context = MQTTContext(loop=loop, queue=queue)
    client = mqtt.Client(userdata=context)

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(BROKER, PORT, 60)
    client.loop_start()

    return client
