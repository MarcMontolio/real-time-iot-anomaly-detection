from fastapi import APIRouter

from app.core.config import settings
from app.api.v1.endpoints import health
from app.api.v1.endpoints import devices
from app.api.v1.endpoints import telemetry


router = APIRouter(
    prefix=settings.api_v1_prefix
)

router.include_router(health.router)
router.include_router(devices.router)
router.include_router(telemetry.router)