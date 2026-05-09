from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.device import Device
from app.repositories.device_repository import create_device, get_device_by_device_id
from app.schemas.device import DeviceCreate


async def create_device_service(
    db: AsyncSession,
    device_data: DeviceCreate,
) -> Device:
    existing_device = await get_device_by_device_id(db, device_data.device_id)

    if existing_device is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Device with this device_id already exists",
        )

    try:
        device = await create_device(db, device_data)
        await db.commit()
        await db.refresh(device)
        return device
    except Exception:
        await db.rollback()
        raise