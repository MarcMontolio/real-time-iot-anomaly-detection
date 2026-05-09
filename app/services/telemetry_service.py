from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.telemetry_event import TelemetryEvent

from app.repositories.device_repository import get_device_by_id
from app.repositories.telemetry_repository import (
    create_telemetry_event,
    get_all_telemetry_events,
    get_telemetry_events_by_device_id,
)

from app.schemas.telemetry_event import TelemetryEventCreate


async def create_telemetry_event_service(
    db: AsyncSession,
    telemetry_event_data: TelemetryEventCreate,
) -> TelemetryEvent:
    existing_device = await get_device_by_id(db, telemetry_event_data.device_id)
    
    if existing_device is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device with this ID does not exist",
        )
        
    try:
        telemetry_event = await create_telemetry_event(db, telemetry_event_data)
        
        telemetry_event.is_anomaly = telemetry_event_data.metric_value > 90
        telemetry_event.anomaly_score = telemetry_event_data.metric_value / 100
        
        await db.commit()
        await db.refresh(telemetry_event)
        
        return telemetry_event
    except Exception:
        await db.rollback()
        raise
    

async def get_all_telemetry_events_service(
    db: AsyncSession,
    limit: int,
    offset: int,
) -> list[TelemetryEvent]:
    return await get_all_telemetry_events(db, limit, offset)


async def get_telemetry_events_by_device_id_service(
    db: AsyncSession,
    device_id: int,
    limit: int,
    offset: int,
) -> list[TelemetryEvent]:
    return await get_telemetry_events_by_device_id(db, device_id, limit, offset)
