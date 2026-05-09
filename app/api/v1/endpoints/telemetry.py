from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.telemetry_event import TelemetryEventCreate, TelemetryEventRead
from app.services.telemetry_service import get_all_telemetry_events_service, create_telemetry_event_service
from app.api.deps import get_db
from app.models.telemetry_event import TelemetryEvent

router = APIRouter(tags=["telemetry"])

@router.post(
    "/telemetry",
    response_model=TelemetryEventRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_new_telemetry_event(
    telemetry_event_data: TelemetryEventCreate,
    db: AsyncSession = Depends(get_db)
) -> TelemetryEvent:
    return await create_telemetry_event_service(db, telemetry_event_data)


@router.get(
    "/telemetry",
    response_model=list[TelemetryEventRead]
)
async def get_telemetry_events(
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    db: AsyncSession = Depends(get_db),
) -> list[TelemetryEvent]:
    return await get_all_telemetry_events_service(db, limit, offset)