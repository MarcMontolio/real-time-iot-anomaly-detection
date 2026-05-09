from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.telemetry_event import TelemetryEventRead
from app.schemas.device import DeviceCreate, DeviceRead

from app.services.telemetry_service import get_telemetry_events_by_device_id_service
from app.services.device_service import create_device_service, get_all_devices_service, get_device_by_device_id_service

from app.api.deps import get_db
from app.models.device import Device
from app.models.telemetry_event import TelemetryEvent


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


@router.get(
    "/devices",
    response_model=list[DeviceRead]
)
async def get_devices(
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    db: AsyncSession = Depends(get_db),
) -> list[Device]:
    return await get_all_devices_service(db, limit, offset)


@router.get(
    "/devices/{device_id}",
    response_model=DeviceRead,
)
async def get_device(
    device_id: str,
    db: AsyncSession = Depends(get_db)
) -> Device:
    return await get_device_by_device_id_service(db, device_id)


@router.get(
    "/devices/{device_id}/telemetry",
    response_model=list[TelemetryEventRead]
)
async def get_device_telemetry_events(
    device_id: int,
    limit: int = Query(default=100, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: AsyncSession = Depends(get_db),
) -> list[TelemetryEvent]:
    return await get_telemetry_events_by_device_id_service(
        db,
        device_id,
        limit,
        offset
    )