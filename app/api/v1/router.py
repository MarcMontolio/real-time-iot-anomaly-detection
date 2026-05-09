from fastapi import APIRouter

from app.core.config import settings
from app.api.v1.endpoints import health


router = APIRouter(
    prefix=settings.api_v1_prefix
)

router.include_router(health.router)