from fastapi import APIRouter, HTTPException

from src.customer.data import CustomerDTO as Customer
from src.customer.services import create_customer

router = APIRouter()

@router.post(
    "/api/customer",
    status_code = 201,
    description="Creates new customers"
)
async def create(customer: Customer):
    service_response = create_customer(customer)
    return service_response

