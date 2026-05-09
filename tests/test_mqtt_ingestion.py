import pytest

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status
from fastapi.testclient import TestClient

from app.mqtt.ingestion import ingest_mqtt_telemetry_message


async def test_ingest_mqtt_telemetry_message_creates_event(client: TestClient, db_session: AsyncSession) -> None:
    payload = {
        "device_id": "sensor-001",
        "name": "Temperature Sensor",
        "device_type": "temperature",
        "location": "server-room",
    }
    
    device_response = client.post("/api/v1/devices", json=payload)
    
    device_data = device_response.json()
    
    assert device_response.status_code == status.HTTP_201_CREATED
    
    topic = "iot/devices/sensor-001/telemetry"
    
    mqtt_payload = """
    {
        "metric_name": "temperature",
        "metric_value": 42.5,
        "timestamp": "2026-05-09T12:00:00Z"
    }
    """
    
    await ingest_mqtt_telemetry_message(db_session, topic, mqtt_payload)
    
    response = client.get(f"/api/v1/devices/{device_data['id']}/telemetry")
    
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    
    assert len(data) == 1    
    assert data[0]["metric_name"] == "temperature"
    assert data[0]["metric_value"] == 42.5
    assert data[0]["device_id"] == device_data["id"]
    

async def test_ingest_mqtt_telemetry_message_unknown_device_raises_error(db_session: AsyncSession) -> None:
    topic = "iot/devices/sensor-999/telemetry"
    
    mqtt_payload = """
    {
        "metric_name": "temperature",
        "metric_value": 42.5,
        "timestamp": "2026-05-09T12:00:00Z"
    }
    """
    
    with pytest.raises(ValueError, match="Device sensor-999 not found"):
        await ingest_mqtt_telemetry_message(db_session, topic, mqtt_payload)
        
        
async def test_ingest_mqtt_telemetry_message_invalid_metric_value_raises_error(client: TestClient, db_session: AsyncSession) -> None:
    payload = {
        "device_id": "sensor-001",
        "name": "Temperature Sensor",
        "device_type": "temperature",
        "location": "server-room",
    }
    
    device_response = client.post("/api/v1/devices", json=payload)
    
    assert device_response.status_code == status.HTTP_201_CREATED
    
    topic = "iot/devices/sensor-001/telemetry"
    
    mqtt_payload = """
    {
        "metric_name": "temperature",
        "metric_value": "not-a-number",
        "timestamp": "2026-05-09T12:00:00Z"
    }
    """
    
    with pytest.raises(ValueError, match="must be numeric"):
        await ingest_mqtt_telemetry_message(db_session, topic, mqtt_payload)