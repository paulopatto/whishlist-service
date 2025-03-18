from src.config.database import SessionType
from src.config.logger import AppLog as log
from src.customer.data import CustomerDTO, CustomerModel


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

