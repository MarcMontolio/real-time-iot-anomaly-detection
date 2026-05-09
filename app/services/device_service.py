from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.device import Device
from app.repositories.device_repository import create_device, get_device_by_device_id, get_all_devices
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
    

async def get_all_devices_service(
    db: AsyncSession
) -> list[Device]:
    device_list = await get_all_devices(db)
    return device_list
    
    
async def get_device_by_device_id_service(
    db: AsyncSession,
    device_id: str
) -> Device:
    device = await get_device_by_device_id(db, device_id)
    
    if device is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found"
        )
    
    return device