from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.device import Device
from app.schemas.device import DeviceCreate


async def get_device_by_device_id(
    db: AsyncSession,
    device_id: str,
) -> Device | None:
    statement = select(Device).where(Device.device_id == device_id)
    result = await db.execute(statement)
    return result.scalar_one_or_none()


async def create_device(
    db: AsyncSession,
    device_data: DeviceCreate,
) -> Device:
    device = Device(
        device_id=device_data.device_id,
        name=device_data.name,
        device_type=device_data.device_type,
        location=device_data.location,
    )

    db.add(device)
    await db.flush()

    return device


async def get_all_devices(
    db: AsyncSession
) -> list[Device]:
    statement = select(Device)
    result = await db.execute(statement)
    return list(result.scalars().all())