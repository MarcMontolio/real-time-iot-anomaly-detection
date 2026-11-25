from fastapi import status
from fastapi.testclient import TestClient


def create_test_device(client: TestClient, device_id: str = "sensor-001") -> dict[str, object]:
    payload: dict[str, str] = {
        "device_id": device_id,
        "name": "Temperature Sensor",
        "device_type": "temperature",
        "location": "server-room",
    }

    response = client.post("/api/v1/devices", json=payload)

    assert response.status_code == status.HTTP_201_CREATED

    return response.json()


def test_post_telemetry_events_returns_ok(client: TestClient) -> None:
    device_data = create_test_device(client)
    
    telemetry_payload: dict[str, object] = {
        "device_id": device_data["id"],
        "metric_name": "temperature",
        "metric_value": 42.5,
        "timestamp": "2026-05-09T12:00:00Z",
    }
        
    telemetry_response = client.post("/api/v1/telemetry", json=telemetry_payload)
    
    assert telemetry_response.status_code == status.HTTP_201_CREATED
    
    data = telemetry_response.json()
    
    assert data["device_id"] == device_data["id"]
    assert data["metric_name"] == "temperature"
    assert data["is_anomaly"] is False
    

def test_post_telemetry_event_with_unknown_device_returns_404(client: TestClient) -> None:
    telemetry_payload: dict[str, object] = {
        "device_id": 999,
        "metric_name": "temperature",
        "metric_value": 42.5,
        "timestamp": "2026-05-09T12:00:00Z",
    }

    response = client.post("/api/v1/telemetry", json=telemetry_payload)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Device with this ID does not exist"
    
    
    
def test_is_anomaly_returns_true(client: TestClient) -> None:
    device_data = create_test_device(client)

    normal_payloads = [
        {
            "device_id": device_data["id"],
            "metric_name": "temperature",
            "metric_value": 40.0,
            "timestamp": "2026-05-09T12:00:00Z",
        },
        {
            "device_id": device_data["id"],
            "metric_name": "temperature",
            "metric_value": 41.0,
            "timestamp": "2026-05-09T12:01:00Z",
        },
        {
            "device_id": device_data["id"],
            "metric_name": "temperature",
            "metric_value": 42.0,
            "timestamp": "2026-05-09T12:02:00Z",
        },
    ]

    for payload in normal_payloads:
        response = client.post("/api/v1/telemetry", json=payload)

        assert response.status_code == status.HTTP_201_CREATED

    anomaly_payload: dict[str, object] = {
        "device_id": device_data["id"],
        "metric_name": "temperature",
        "metric_value": 95.5,
        "timestamp": "2026-05-09T12:05:00Z",
    }

    response = client.post("/api/v1/telemetry", json=anomaly_payload)

    assert response.status_code == status.HTTP_201_CREATED

    data: dict[str, object] = response.json()

    assert data["is_anomaly"] is True
    assert isinstance(data["anomaly_score"], float)
    assert data["anomaly_score"] > 3.0
    
    
def test_get_all_telemetry_events_returns_list(client: TestClient) -> None:
    device_data = create_test_device(client)
    
    telemetry_payload: dict[str, object] = {
        "device_id": device_data["id"],
        "metric_name": "temperature",
        "metric_value": 42.5,
        "timestamp": "2026-05-09T12:00:00Z",
    }
    
    response = client.post("/api/v1/telemetry", json=telemetry_payload)
    
    response = client.get("/api/v1/telemetry")
    
    assert response.status_code == status.HTTP_200_OK
    
    data: list[dict[str,object]] = response.json()
    
    assert isinstance(data, list)
    
    
def test_get_device_telemetry_events_filter_by_device(client: TestClient) -> None:
    device1 = create_test_device(client)
    
    device2 = create_test_device(client, device_id="sensor-002")
    
    telemetry_payload: dict[str, object] = {
        "device_id": device1["id"],
        "metric_name": "temperature",
        "metric_value": 42.5,
        "timestamp": "2026-05-09T12:00:00Z",
    }
    
    response = client.post("/api/v1/telemetry", json=telemetry_payload)
    
    telemetry_payload: dict[str, object] = {
        "device_id": device2["id"],
        "metric_name": "humidity",
        "metric_value": 80,
        "timestamp": "2026-05-09T12:00:00Z",
    }
    
    response = client.post("/api/v1/telemetry", json=telemetry_payload)
    
    response = client.get(f"/api/v1/devices/{device2['id']}/telemetry")
    
    assert response.status_code == status.HTTP_200_OK
    
    data: list[dict[str, object]] = response.json()
    
    assert len(data) == 1
    assert data[0]["metric_name"] == "humidity"
    assert data[0]["device_id"] == device2["id"]
    
    
def test_get_all_telemetry_events_limit_validation_returns_422(client: TestClient) -> None:
    device_data = create_test_device(client)
    
    telemetry_payload: dict[str, object] = {
        "device_id": device_data["id"],
        "metric_name": "humidity",
        "metric_value": 80,
        "timestamp": "2026-05-09T12:00:00Z",
    }
    
    response = client.post("/api/v1/telemetry", json=telemetry_payload)
    
    response = client.get("/api/v1/telemetry?limit=1000")
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    

def test_get_device_telemetry_event_limit_validation_returns_422(client: TestClient) -> None:
    device_data = create_test_device(client)
    
    telemetry_payload: dict[str, object] = {
        "device_id": device_data["id"],
        "metric_name": "humidity",
        "metric_value": 80,
        "timestamp": "2026-05-09T12:00:00Z",
    }
    
    response = client.post("/api/v1/telemetry", json=telemetry_payload)
    
    response = client.get(
    f"/api/v1/devices/{device_data['id']}/telemetry?limit=1000"
    )
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_telemetry_event_with_insufficient_history_is_not_anomaly(client: TestClient) -> None:
    device_data = create_test_device(client)
    
    telemetry_payload: dict[str, object] = {
        "device_id": device_data["id"],
        "metric_name": "humidity",
        "metric_value": 150,
        "timestamp": "2026-05-09T12:00:00Z",
    }
    
    response = client.post("/api/v1/telemetry", json=telemetry_payload)
    
    assert response.status_code == status.HTTP_201_CREATED
    
    response = client.get(
        f"/api/v1/devices/{device_data['id']}/telemetry"
    )
    
    data = response.json()
    
    assert data[0]["is_anomaly"] is False
    assert data[0]["anomaly_score"] == 0.0