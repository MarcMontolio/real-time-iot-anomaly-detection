from fastapi import status
from fastapi.testclient import TestClient


def test_post_devices_returns_ok(client: TestClient) -> None:
    payload = {
        "device_id": "sensor-001",
        "name": "Temperature Sensor",
        "device_type": "temperature",
        "location": "server-room",
    }
    
    response = client.post("/api/v1/devices", json=payload)
    
    assert response.status_code == status.HTTP_201_CREATED
    
    data = response.json()
    
    assert data["device_id"] == "sensor-001"
    assert data["name"] == "Temperature Sensor"
    assert data["status"] == "active"


def test_post_duplicate_device(client: TestClient) -> None:
    payload = {
        "device_id": "sensor-001",
        "name": "Temperature Sensor",
        "device_type": "temperature",
        "location": "server-room",
    }
    
    response = client.post("/api/v1/devices", json=payload)
    response = client.post("/api/v1/devices", json=payload)
    
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()["detail"] == "Device with this device_id already exists"
    
    
def test_get_all_devices(client: TestClient) -> None:
    payload = {
        "device_id": "sensor-001",
        "name": "Temperature Sensor",
        "device_type": "temperature",
        "location": "server-room",
    }

    client.post("/api/v1/devices", json=payload)

    response = client.get("/api/v1/devices")

    assert response.status_code == status.HTTP_200_OK

    data: list[dict[str, object]] = response.json()

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["device_id"] == "sensor-001"
    
def test_get_device_by_id(client: TestClient) -> None:
    payload = {
        "device_id": "sensor-001",
        "name": "Temperature Sensor",
        "device_type": "temperature",
        "location": "server-room",
    }
    
    response = client.post("/api/v1/devices", json=payload)
    response = client.get("/api/v1/devices/sensor-001")
    
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    
    assert data["device_id"] == "sensor-001"
    
    
def test_get_device_non_existent(client: TestClient) -> None:
    response = client.get("/api/v1/devices/non-existent")
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    

def test_get_device_limit_works(client: TestClient) -> None:
    payload = {
        "device_id": "sensor-001",
        "name": "Temperature Sensor",
        "device_type": "temperature",
        "location": "server-room",
    }
    
    response = client.post("/api/v1/devices", json=payload)
    
    payload = {
        "device_id": "sensor-002",
        "name": "Temperature Sensor",
        "device_type": "temperature",
        "location": "server-room",
    }
    
    response = client.post("/api/v1/devices", json=payload)
    
    payload = {
        "device_id": "sensor-003",
        "name": "Temperature Sensor",
        "device_type": "temperature",
        "location": "server-room",
    }
    
    response = client.post("/api/v1/devices", json=payload)
    
    response = client.get("/api/v1/devices?limit=2&offset=0")
    
    data: list[dict[str, object]] = response.json()
    
    assert len(data) == 2
    

def test_get_device_offset_works(client: TestClient) -> None:
    payload = {
        "device_id": "sensor-001",
        "name": "Temperature Sensor",
        "device_type": "temperature",
        "location": "server-room",
    }
    
    response = client.post("/api/v1/devices", json=payload)
    
    payload = {
        "device_id": "sensor-002",
        "name": "Temperature Sensor",
        "device_type": "temperature",
        "location": "server-room",
    }
    
    response = client.post("/api/v1/devices", json=payload)
    
    payload = {
        "device_id": "sensor-003",
        "name": "Temperature Sensor",
        "device_type": "temperature",
        "location": "server-room",
    }
    
    response = client.post("/api/v1/devices", json=payload)
    
    response = client.get("/api/v1/devices?limit=2&offset=2")
    
    data: list[dict[str, object]] = response.json()
    
    assert len(data) == 1
    assert data[0]["device_id"] == "sensor-003"
    
    
def test_get_device_limit_limitation_returns_422 (client: TestClient) -> None:
    payload = {
            "device_id": "sensor-001",
            "name": "Temperature Sensor",
            "device_type": "temperature",
            "location": "server-room",
    }
        
    response = client.post("/api/v1/devices", json=payload)
    
    response = client.get("/api/v1/devices?limit=1000&offset=2")
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    