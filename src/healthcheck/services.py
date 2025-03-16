import os

import psycopg2

from src.healthcheck.interfaces import HealthCheckResultDTO, IHealthCheckResult


def check_status():
    return "Everything is ok"


def database_is_health() -> IHealthCheckResult:
    DATABASE_URL = os.environ.get("DATABASE_URL")

    if not DATABASE_URL:
        return HealthCheckResultDTO(health=False, message="DATABASE_URL not set")
    try:
        conn = psycopg2.connect(DATABASE_URL)
        conn.close()
        return HealthCheckResultDTO(health=True, message="Database is healthy")
    except Exception as e:
        error_message = str(e)
        print(f"Database connection error: {error_message}")
        return HealthCheckResultDTO(health=False, message=error_message)

