from dataclasses import asdict
from typing import List

from fastapi import APIRouter, HTTPException

from src.healthcheck.interfaces import IHealthCheckResult

from .services import database_is_health, server_is_health

router = APIRouter(prefix="/api/healthcheck")


@router.get("/", description="Check the health of the API")
async def healthcheck():
    webserver: IHealthCheckResult = server_is_health()
    database: IHealthCheckResult = database_is_health()

    checks: List[IHealthCheckResult] = [webserver, database]

    if any(not check.health for check in checks):
        json_checks = [asdict(check) for check in checks]
        raise HTTPException(status_code=503, detail=json_checks)

    return {"status": "Everything is ok", "details": checks}

