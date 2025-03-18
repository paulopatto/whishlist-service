from fastapi import APIRouter

from src.config.database import SessionType
from src.customer.data import CustomerDTO as Customer
from src.customer.services import create_customer

router = APIRouter(prefix="/api/customer")


@router.post("/", status_code=201, description="Creates new customers")
async def create(customer: Customer, session: SessionType) -> Customer:
    service_response: Customer = await create_customer(customer, session)
    return service_response

