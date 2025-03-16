from fastapi.testclient import TestClient
from pytest import fixture

from src.main import app


@fixture
def test_client():
    with TestClient(app) as client:
        yield client
