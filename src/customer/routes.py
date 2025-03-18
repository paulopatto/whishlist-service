from fastapi import APIRouter
from fastapi.exceptions import HTTPException

from src.config.database import SessionType
from src.config.logger import AppLog as log
from src.customer.data import CustomerDTO as Customer
from src.customer.services import create_customer

router = APIRouter(prefix="/api/customer")


@router.post("/", status_code=201, description="Creates new customers")
async def create(customer: Customer, session: SessionType) -> Customer:
    try:
        service_response: Customer = await create_customer(customer, session)
        return service_response
    except Exception as e:
        log.error(f"Erro: {e}")
        raise HTTPException(
            status_code=422,
            detail="Erro during create user",
        )

