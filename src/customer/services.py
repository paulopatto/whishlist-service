from uuid import UUID

from fastapi import Depends

from src.config.logger import AppLog as log
from src.customer.data import (
    CustomerDTO,
    CustomerModel,
    CustomerRepository,
    get_customer_repository,
)


async def delete_customer(external_id: UUID, repository: CustomerRepository) -> None:
    try:
        repository.delete(external_id)
    except Exception as e:
        error_message = str(e)
        log.error(
            f"Error during deletion of customer {external_id} due {error_message}"
        )
        raise e

async def update_customer(
    data: CustomerDTO,
    repository: CustomerRepository
) -> CustomerDTO:
    try:
        #import pdb; pdb.set_trace()
        updated_customer = repository.update(data)
        return CustomerDTO(
            id=updated_customer.external_id,
            name=updated_customer.name,
            email=updated_customer.email,
        )
    except Exception as e:
        error_message = str(e)
        log.error(f"Error during update of customer {data.id} due {error_message}")
        raise e

async def fetch_customer(
    identifier: str | UUID,
    repository: CustomerRepository = Depends(get_customer_repository)
) -> CustomerDTO:
    """
    Fetch a customer by external_id (UUID) or email (str).
    """
    try:
        customer: CustomerModel = repository.get_customer(identifier)
        return CustomerDTO(
            id=customer.external_id,
            name=customer.name,
            email=customer.email,
        )
    except ValueError as e:
        log.error("Error during retrieval of customer due not found")
        raise e
    except Exception as e:
        error_message = str(e)
        log.error(
            f"Error during retrieval of customer due {error_message}"
        )
        raise e

async def create_customer(
    data: CustomerDTO,
    repository: CustomerRepository
) -> CustomerDTO:
    try:
        customer: CustomerModel = repository.create_customer(data)
        return CustomerDTO(
            id=customer.external_id,
            name=customer.name,
            email=customer.email,
        )
    except Exception as e:
        error_message = str(e)
        log.error(f"Error during creation customer due {error_message}")
        raise e
