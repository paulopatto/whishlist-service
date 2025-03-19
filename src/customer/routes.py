from fastapi import APIRouter
from fastapi.exceptions import HTTPException

from src.config.database import SessionType
from src.config.logger import AppLog as log
from src.customer.data import CustomerDTO as Customer
from src.customer.services import create_customer

router = APIRouter(prefix="/api/customer")


@router.post(
    "/", status_code=201,
    description="Creates new customers",
    response_model=Customer,
    tags=["Customer"]
)
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

from fastapi import APIRouter, HTTPException
from uuid import UUID

from src.config.database import SessionType
from src.config.logger import AppLog as log
from src.customer.data import CustomerDTO as Customer
from src.customer.services import create_customer, delete_customer, update_customer, get_customer

router = APIRouter(prefix="/api/customer")


@router.post(
    "/", status_code=201,
    description="Creates new customers",
    response_model=Customer,
    tags=["Customer"]
)
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


@router.delete(
    "/{external_id}",
    status_code=204,
    description="Deletes a customer by ID",
    tags=["Customer"]
)
async def delete(external_id: UUID, session: SessionType):
    try:
        await delete_customer(external_id, session)
    except ValueError as e:
        log.error(f"Erro: {e}")
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )
    except Exception as e:
        log.error(f"Erro: {e}")
        raise HTTPException(
            status_code=500,
            detail="Erro during delete user",
        )


@router.patch(
    "/{external_id}",
    status_code=200,
    description="Updates a customer by ID",
    response_model=Customer,
    tags=["Customer"]
)
async def update(external_id: UUID, customer: Customer, session: SessionType) -> Customer:
    try:
        customer.id = external_id  # Ensure the ID matches the path parameter
        service_response: Customer = await update_customer(customer, session)
        return service_response
    except ValueError as e:
        log.error(f"Erro: {e}")
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )
    except Exception as e:
        log.error(f"Erro: {e}")
        raise HTTPException(
            status_code=500,
            detail="Erro during update user",
        )


@router.get(
    "/{external_id}",
    status_code=200,
    description="Retrieves a customer by ID",
    response_model=Customer,
    tags=["Customer"]
)
async def get(external_id: UUID, session: SessionType) -> Customer:
    try:
        service_response: Customer = await get_customer(external_id, session)
        return service_response
    except ValueError as e:
        log.error(f"Erro: {e}")
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )
    except Exception as e:
        log.error(f"Erro: {e}")
        raise HTTPException(
            status_code=500,
            detail="Erro during get user",
        )
