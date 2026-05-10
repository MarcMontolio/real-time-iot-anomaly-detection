from fastapi import FastAPI

from app.api.v1.router import router as api_router
from app.core.config import settings

from app.websockets.routes import router as websocket_router

from app.mqtt.consumer import start_consumer_background


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    description="Real-time IoT detection system using FastAPI, MQTT, Redis, PostgreSQL and machine learning."
)

@app.on_event("startup")
async def start_mqtt_consumer() -> None:
    start_consumer_background()

app.include_router(api_router)
app.include_router(websocket_router)