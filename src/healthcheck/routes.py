from fastapi import APIRouter

from .services import check_status

router = APIRouter()


@router.get("/api/healthcheck", description="Check the health of the API")
async def healthcheck():
    status = check_status()
    return {"status": "ok", "details": status}
