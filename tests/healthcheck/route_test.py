from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def describe_healthcheck_route():
    def test_get_healthcheck_path():
        response = client.get("/api/healthcheck")

        body = response.json()

        assert response.status_code == 200
        assert body["status"] == "ok"

