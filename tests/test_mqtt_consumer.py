import asyncio
import json
from unittest import mock

import paho.mqtt.client as mqtt
import pytest

from app.mqtt.consumer import (
    MQTTContext,
    on_message,
    process_message_queue,
)


@pytest.mark.asyncio
async def test_on_message_processes_consecutive_messages() -> None:
    loop = asyncio.get_running_loop()
    queue: asyncio.Queue[tuple[str, str]] = asyncio.Queue()
    context = MQTTContext(queue=queue, loop=loop)

    processed_messages: list[tuple[str, str]] = []

    message_processed = asyncio.Event()

    async def fake_handle_message(topic: str, payload: str) -> None:
        assert asyncio.get_running_loop() is loop

        processed_messages.append((topic, payload))

        if len(processed_messages) == 15:
            message_processed.set()

    with mock.patch("app.mqtt.consumer.handle_message", new=fake_handle_message):
        worker_task = asyncio.create_task(process_message_queue(queue))

        temperatures = [
            21.5,
            22.0,
            22.4,
            23.1,
            23.5,
            24.0,
            24.3,
            24.8,
            25.2,
            25.7,
            26.1,
            26.8,
            27.3,
            120.0,
            130.0,
        ]

        try:
            for temperature in temperatures:
                msg = mock.Mock(spec=mqtt.MQTTMessage)
                msg.topic = "iot/devices/sensor-001/telemetry"
                msg.payload = json.dumps(
                    {
                        "metric_name": "temperature",
                        "metric_value": temperature,
                    }
                ).encode("utf-8")

                await asyncio.to_thread(
                    on_message,
                    mock.Mock(spec=mqtt.Client),
                    context,
                    msg,
                )

            await asyncio.wait_for(
                message_processed.wait(),
                timeout=5,
            )

            await queue.join()

        finally:
            worker_task.cancel()

            try:
                await worker_task
            except asyncio.CancelledError:
                pass

            assert len(processed_messages) == 15

            assert all(
                topic == "iot/devices/sensor-001/telemetry"
                for topic, _ in processed_messages
            )

            received_temperatures = [
                json.loads(payload)["metric_value"] for _, payload in processed_messages
            ]

            assert sorted(received_temperatures) == sorted(temperatures)
