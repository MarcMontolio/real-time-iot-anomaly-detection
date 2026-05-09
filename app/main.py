from fastapi import FastAPI

from app.api.v1.router import router as api_router
from app.core.config import settings


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    description="Real-time IoT detection system using FastAPI, MQTT, Redis, PostgreSQL and machine learning."
)

app.include_router(api_router)