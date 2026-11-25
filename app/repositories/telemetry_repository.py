from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.telemetry_event import TelemetryEvent
from app.schemas.telemetry_event import TelemetryEventCreate


async def create_telemetry_event(
    db: AsyncSession, telemetry_event_data: TelemetryEventCreate
) -> TelemetryEvent:
    telemetry_event = TelemetryEvent(
        device_id=telemetry_event_data.device_id,
        metric_name=telemetry_event_data.metric_name,
        metric_value=telemetry_event_data.metric_value,
        timestamp=telemetry_event_data.timestamp,
    )

    db.add(telemetry_event)
    await db.flush()

    return telemetry_event


async def get_all_telemetry_events(
    db: AsyncSession, limit: int, offset: int
) -> list[TelemetryEvent]:
    statement = (
        select(TelemetryEvent)
        .order_by(TelemetryEvent.timestamp.desc(), TelemetryEvent.id.desc())
        .offset(offset)
        .limit(limit)
    )
    result = await db.execute(statement)
    return list(result.scalars().all())


async def get_telemetry_events_by_device_id(
    db: AsyncSession,
    device_id: int,
    limit: int,
    offset: int,
) -> list[TelemetryEvent]:
    statement = (
        select(TelemetryEvent)
        .where(TelemetryEvent.device_id == device_id)
        .order_by(TelemetryEvent.timestamp.desc())
        .offset(offset)
        .limit(limit)
    )
    result = await db.execute(statement)
    return list(result.scalars().all())


async def get_telemetry_events_by_device_id_and_metric_name(
    db: AsyncSession,
    device_id: int,
    limit: int,
    offset: int,
    metric_name: str,
    timestamp: datetime,
) -> list[TelemetryEvent]:
    statement = (
        select(TelemetryEvent)
        .where(
            TelemetryEvent.device_id == device_id,
            TelemetryEvent.metric_name == metric_name,
            TelemetryEvent.timestamp < timestamp,
            TelemetryEvent.is_anomaly.is_(False),
        )
        .order_by(TelemetryEvent.timestamp.desc())
        .limit(limit)
        .offset(offset)
    )
    result = await db.execute(statement)
    return list(result.scalars().all())
