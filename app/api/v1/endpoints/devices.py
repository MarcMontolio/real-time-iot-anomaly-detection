from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.device import DeviceCreate, DeviceRead
from app.services.device_service import create_device_service
from app.api.deps import get_db
from app.models.device import Device

router = APIRouter(tags=["devices"])

@router.post(
    "/devices",
    response_model=DeviceRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_new_device(
    device_data: DeviceCreate,
    db: AsyncSession = Depends(get_db)
) -> Device:
    return await create_device_service(db, device_data)