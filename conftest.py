from fastapi.testclient import TestClient
from pytest import fixture
from sqlmodel import SQLModel, Session, create_engine

from src.main import app

DATABASE_URL = "sqlite:///:memory:"

@fixture
def test_client():
    with TestClient(app) as client:
        yield client


@fixture(scope = "session")
def engine():
    engine = create_engine(DATABASE_URL)
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)

@fixture
def db_session(engine):
    with Session(engine) as session:
        yield session
