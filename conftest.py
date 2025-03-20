from fastapi.testclient import TestClient
from pytest import fixture
from sqlmodel import Session, SQLModel, create_engine

from factories import CustomerFactory, InvalidUserFactory
from src.config.database import DATABASE_URL
from src.config.envs import load_envs
from src.config.tables import database_setup
from src.main import app

load_envs("test")

@fixture
def test_client():
    with TestClient(app) as client:
        yield client


@fixture(scope="session")
def engine():
    engine = create_engine(DATABASE_URL)
    # with Session(engine) as session:
    #     database_setup()
    #     yield session
    #
    # SQLModel.metadata.drop_all(engine)
    database_setup()
    yield engine
    engine.dispose()


@fixture(scope="function", autouse=True)
def clean_db(session):
    for table in reversed(SQLModel.metadata.sorted_tables):
        session.execute(table.delete())

    session.commit()


@fixture(scope="function")
def session(engine):
    with Session(engine) as session:
        database_setup()
        yield session

    session.close()


@fixture(scope="function")
def valid_customer():
    return CustomerFactory()

@fixture(scope="function")
def invalid_customer():
    return InvalidUserFactory()
