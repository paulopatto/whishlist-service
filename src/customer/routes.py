from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from src.auth.middlewares import validate_token
from src.config.logger import AppLog as log
from src.customer.data import CustomerDTO as Customer
from src.customer.data import CustomerRepository, get_customer_repository
from src.customer.services import (
    create_customer,
    delete_customer,
    fetch_customer,
    update_customer,
)

router = APIRouter(
    prefix="/api/customer",
    dependencies=[Depends(validate_token)]
)


@router.post(
    "/",
    status_code=201,
    description="Creates new customers",
    response_model=Customer,
    tags=["Customer"],
)
async def create(
    customer: Customer,
    repository: CustomerRepository = Depends(get_customer_repository)
) -> Customer:
    try:
        service_response: Customer = await create_customer(
            customer, repository=repository
        )
        return service_response
    except Exception as e:
        log.error(f"Erro: {e}")
        raise HTTPException(
            status_code=409,
            detail="Erro during create user",
        )


@router.delete(
    "/{external_id}",
    status_code=204,
    description="Deletes a customer by ID",
    tags=["Customer"],
)
async def delete(
    external_id: UUID, repository: CustomerRepository = Depends(get_customer_repository)
) -> None:
    try:
        await delete_customer(external_id, repository)
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
    tags=["Customer"],
)
async def update(
    external_id: UUID,
    customer: Customer,
    repository: CustomerRepository = Depends(get_customer_repository),
) -> Customer:
    try:
        customer.id = external_id  # Ensure the ID matches the path parameter
        service_response: Customer = await update_customer(customer, repository)
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
    "/{identifier}",
    status_code=200,
    description="Retrieves a customer by ID or email",
    response_model=Customer,
    tags=["Customer"],
)
async def get(
    identifier: str, repository: CustomerRepository = Depends(get_customer_repository)
) -> Customer:
    try:
        sanitized_identifier = sanitize_identifier(identifier)
        service_response: Customer = await fetch_customer(
            sanitized_identifier, repository=repository
        )
        return service_response
    except ValueError as e:
        log.error(f"Erro: {e}")
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )
    except Exception as e:
        log.error(f"Erro: {e}")
        error_message = str(e)
        raise HTTPException(
            status_code=500,
            detail=f"Erro during get user due {error_message}",
        )


def sanitize_identifier(identifier: str) -> UUID | str:
    try:
        return UUID(identifier)
    except ValueError:
        return identifier

