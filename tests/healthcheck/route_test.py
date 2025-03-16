from pytest import fixture
from fastapi.testclient import TestClient
from src.main import app


@fixture
def test_client():
    with TestClient(app) as client:
        yield client


def describe_healthcheck_route():
    def test_get_healthcheck_path(test_client):
        response = test_client.get("/api/healthcheck")

        body = response.json()

        assert response.status_code == 200
        assert body["status"] == "ok"

