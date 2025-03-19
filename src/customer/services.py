from uuid import UUID

from sqlmodel import select
from src.config.database import SessionType
from src.config.logger import AppLog as log
from src.customer.data import CustomerDTO, CustomerModel

#TODO: Pensar em como remover essas duplicação de código
async def create_customer(data: CustomerDTO, session: SessionType) -> CustomerDTO:
    try:
        customer: CustomerModel = CustomerModel(name=data.name, email=data.email)

        with session:
            session.add(customer)
            session.commit()
            session.refresh(customer)
            data.id = customer.external_id

        return data
    except Exception as e:
        error_message = str(e)
        log.error(f"Error during creation customer due {error_message}")
        raise e

async def delete_customer(external_id: UUID, session: SessionType) -> None:
    try:
        with session:
            statement = select(CustomerModel).where(CustomerModel.external_id == external_id)
            result = session.exec(statement)
            customer = result.one_or_none()

            if not customer:
                raise ValueError(f"Customer with ID {external_id} not found")

            session.delete(customer)
            session.commit()
    except Exception as e:
        error_message = str(e)
        log.error(f"Error during deletion of customer {external_id} due {error_message}")
        raise e

async def update_customer(data: CustomerDTO, session: SessionType) -> CustomerDTO:
    try:
        with session:
            statement = select(CustomerModel).where(CustomerModel.external_id == data.id)
            result = session.exec(statement)
            customer = result.one_or_none()

            if not customer:
                raise ValueError(f"Customer with ID {data.id} not found")

            customer.name = data.name
            # Only update name, email remains the same
            # customer.email = data.email

            session.add(customer)
            session.commit()
            session.refresh(customer)

        return data
    except Exception as e:
        error_message = str(e)
        log.error(f"Error during update of customer {data.id} due {error_message}")
        raise e

async def get_customer(external_id: UUID, session: SessionType) -> CustomerDTO:
    try:
        with session:
            statement = select(CustomerModel).where(CustomerModel.external_id == external_id)
            result = session.exec(statement)
            customer = result.one_or_none()

            if not customer:
                raise ValueError(f"Customer with ID {external_id} not found")

            return CustomerDTO(
                id=customer.external_id,
                name=customer.name,
                email=customer.email
            )
    except Exception as e:
        error_message = str(e)
        log.error(f"Error during retrieval of customer {external_id} due {error_message}")
        raise e
