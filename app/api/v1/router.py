from fastapi import APIRouter

from app.api.v1.endpoints import devices, health, telemetry
from app.core.config import settings

router = APIRouter(
    prefix=settings.api_v1_prefix
)

router.include_router(health.router)
router.include_router(devices.router)
router.include_router(telemetry.router)