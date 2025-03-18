from src.config.database import SessionType
from src.customer.data import CustomerDTO, CustomerModel


async def create_customer(data: CustomerDTO, session: SessionType) -> CustomerDTO:
    customer: CustomerModel = CustomerModel(name=data.name, email=data.email)

    with session:
        session.add(customer)
        session.commit()
        session.refresh(customer)
        data.id = customer.external_id

    return data

