import os

from sqlmodel import Session, create_engine
from sqlalchemy.sql import text

from src.healthcheck.interfaces import HealthCheckResultDTO, IHealthCheckResult


def server_is_health() -> IHealthCheckResult:
    return HealthCheckResultDTO(health=True, message="Webserver is healthy")


def database_is_health() -> IHealthCheckResult:
    DATABASE_URL = os.environ.get("DATABASE_URL")

    if not DATABASE_URL:
        return HealthCheckResultDTO(health=False, message="DATABASE_URL not set")
    try:
        engine = create_engine(DATABASE_URL)
        with Session(engine) as session:
            #DOC: https://stackoverflow.com/questions/54483184/sqlalchemy-warning-textual-column-expression-should-be-explicitly-declared
            session.exec(text("SELECT 1"))
        return HealthCheckResultDTO(health=True, message="Database is healthy")
    except Exception as e:
        error_message = str(e)
        print(f"Database connection error: {error_message}")
        return HealthCheckResultDTO(health=False, message=error_message)

