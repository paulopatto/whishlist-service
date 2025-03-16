from fastapi import APIRouter, HTTPException

from src.healthcheck.interfaces import IHealthCheckResult

from .services import check_status, database_is_health

router = APIRouter()


@router.get("/api/healthcheck", description="Check the health of the API")
async def healthcheck():
    status = check_status()
    return { "status": "ok", "details": status }


@router.get(
    "/api/healthcheck/database",
    description="Check the health of database connection"
)
async def check_database_connection():
    status: IHealthCheckResult = database_is_health()
    if not status.health:
        raise HTTPException(status_code=503, detail=status.message)
    return { "status": "ok", "details": status }

