from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.telemetry_event import TelemetryEvent

from app.repositories.device_repository import get_device_by_id
from app.repositories.telemetry_repository import (
    create_telemetry_event,
    get_all_telemetry_events,
    get_telemetry_events_by_device_id,
    get_telemetry_events_by_device_id_and_metric_name,
)

from app.schemas.telemetry_event import TelemetryEventCreate

from app.services.anomaly_detection import detect_anomaly

from app.websockets.connection_manager import manager

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
        historical_events = await get_telemetry_events_by_device_id_and_metric_name(
        db=db,
        device_id=telemetry_event_data.device_id,
        metric_name=telemetry_event_data.metric_name,
        limit=50,
        offset=0,
        )
        
        historical_values = [event.metric_value for event in historical_events]
        
        if len(historical_values) >= 3:
            is_anomaly, anomaly_score = detect_anomaly(
                value=telemetry_event_data.metric_value,
                historical_values=historical_values,
            )
        else:
            is_anomaly = False
            anomaly_score = 0.0
        
        telemetry_event = await create_telemetry_event(db, telemetry_event_data)
        
        telemetry_event.is_anomaly = is_anomaly
        telemetry_event.anomaly_score = anomaly_score
        
        await db.commit()
        await db.refresh(telemetry_event)
        
        await manager.broadcast(
            {
                "id": telemetry_event.id,
                "device_id": telemetry_event.device_id,
                "metric_name": telemetry_event.metric_name,
                "metric_value": telemetry_event.metric_value,
                "timestamp": telemetry_event.timestamp.isoformat(),
                "is_anomaly": telemetry_event.is_anomaly,
                "anomaly_score": telemetry_event.anomaly_score,  
            }
        )
        
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
