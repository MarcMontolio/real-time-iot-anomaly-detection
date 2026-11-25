import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import router as api_router
from app.core.config import settings
from app.mqtt.consumer import (
    process_message_queue,
    start_consumer_background,
)
from app.websockets.routes import router as websocket_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    loop = asyncio.get_running_loop()
    queue: asyncio.Queue[tuple[str, str]] = asyncio.Queue()

    mqtt_client = start_consumer_background(loop, queue)
    worker_task = asyncio.create_task(process_message_queue(queue))

    app.state.mqtt_client = mqtt_client
    app.state.mqtt_queue = queue

    try:
        yield
    finally:
        mqtt_client.disconnect()
        mqtt_client.loop_stop()

        await queue.join()

        worker_task.cancel()
        try:
            await worker_task
        except asyncio.CancelledError:
            pass


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    description=(
        "Real-time IoT detection system using FastAPI, MQTT, "
        "Redis, PostgreSQL and machine learning."
    ),
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_router)
app.include_router(websocket_router)
