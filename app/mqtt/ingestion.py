from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.mqtt.parser import extract_device_id_from_topic, parse_telemetry_payload
from app.repositories.device_repository import get_device_by_device_id
from app.schemas.telemetry_event import TelemetryEventCreate
from app.services.telemetry_service import create_telemetry_event_service

# from app.models.telemetry_event import TelemetryEvent


async def ingest_mqtt_telemetry_message(
    db: AsyncSession,
    topic: str,
    payload: str,
) -> None:
    device_external_id = extract_device_id_from_topic(topic)
    
    telemetry_payload: dict[str, object] = parse_telemetry_payload(payload)
    
    device = await get_device_by_device_id(db, device_external_id)
    
    if device is None:
        raise ValueError(f"Device {device_external_id} not found")
    
    metric_name = telemetry_payload["metric_name"]
    if not isinstance(metric_name, str):
        raise ValueError("metric_name must be a string")
    
    metric_value = telemetry_payload["metric_value"]
    if not isinstance(metric_value, (int, float)):
        raise ValueError("metric_value must be numeric")
    metric_value = float(metric_value)
    
    timestamp = telemetry_payload["timestamp"]
    if not isinstance(timestamp, str):
        raise ValueError("timestamp must be a string")
    timestamp = timestamp.replace("Z", "+00:00")
    timestamp = datetime.fromisoformat(timestamp)
    
    telemetry_event_data = TelemetryEventCreate(device_id=device.id, metric_name=metric_name, metric_value=metric_value, timestamp=timestamp)
    
    await create_telemetry_event_service(db, telemetry_event_data)
    
    