from fastapi.testclient import TestClient
from fastapi import status

from app.main import app


client = TestClient(app)


def test_health_check_returns_ok() -> None:
    response = client.get("/api/v1/health")
    assert response.status_code == status.HTTP_200_OK, "Health endpoint did not return 200"
    assert response.json() == {"status": "ok"}, "Unexpected response payload from /api/v1/health"