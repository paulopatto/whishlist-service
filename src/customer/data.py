import uuid
from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID

from fastapi import Depends
from pydantic import BaseModel, EmailStr
from sqlmodel import Field, Relationship, Session, SQLModel, select

from src.config.database import get_session
from src.config.logger import AppLog as log


class CustomerDTO(BaseModel):
    id: Optional[UUID | None] = None
    name: str
    email: EmailStr


class CustomerModel(SQLModel, table=True):
    __tablename__ = "customers"

    id: int | None = Field(default=None, primary_key=True)
    external_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: str = Field(nullable=False)
    email: EmailStr = Field(nullable=False, unique=True)

    created_at: datetime = Field(nullable=False, default=datetime.now(timezone.utc))
    # TODO: Trying auto update w/ kwargs
    # READ:
    # - https://github.com/fastapi/sqlmodel/issues/252
    # - https://medium.com/@jtgraham38/how-to-make-auto-updating-timestamp-fields-in-sqlmodel-03c1d674fa99
    updated_at: datetime = Field(
        nullable=False,
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)},
    )
    favorite_products: List["FavoriteProductModel"] = Relationship( # noqa: F821
        back_populates="customer"
    )


class CustomerRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_customer(self, data: CustomerDTO) -> CustomerModel:
        try:
            customer: CustomerModel = CustomerModel(name=data.name, email=data.email)
            self.session.add(customer)
            self.session.commit()
            self.session.refresh(customer)
            return customer
        except Exception as e:
            error_message = str(e)
            log.error(
                f"Error during creation customer due {error_message}",
                e.__traceback__
            )
            raise e


    #TODO: Ver se vale a pena e facilita a vida usar o DTO em vez do model
    def get_customer(self, identifier: UUID | str) -> CustomerModel:
        try:
            if isinstance(identifier, UUID):
                query = select(
                    CustomerModel
                ).where(
                    CustomerModel.external_id == identifier
                )
            else:
                query = select(
                    CustomerModel
                ).where(
                    CustomerModel.email == identifier
                )

            result = self.session.exec(query)
            customer = result.one_or_none()
        except Exception as e:
            error_message = str(e)
            log.error(
                f"Error during retrieve customer due {error_message}",
                exc_info=True
            )
            raise e

        if not customer:
            raise ValueError("Customer not found")
        return customer

    def update(self, data: CustomerDTO) -> CustomerModel:
        try:
            query = select(
                CustomerModel
            ).where(
                CustomerModel.external_id == data.id
            )
            result = self.session.exec(query)
            customer: CustomerModel = result.one_or_none()
            if not customer:
                raise ValueError(f"Customer with ID {data.id} not found")

            customer.name = data.name
            self.session.add(customer)
            self.session.commit()
            self.session.refresh(customer)
            return customer
        except Exception as e:
            error_message = str(e)
            log.error(
                f"Error during udapte customer due {error_message}",
                e.__traceback__)
            raise e

    def delete(self, external_id: UUID) -> None:
        statement = select(
            CustomerModel
        ).where(
            CustomerModel.external_id == external_id
        )
        result = self.session.exec(statement)
        customer = result.one_or_none()

        if not customer:
            raise ValueError(f"Customer with ID {external_id} not found")
        try:
            self.session.delete(customer)
            self.session.commit()
        except Exception as e:
            error_message = str(e)
            log.error(
                f"Error during delete customer due {error_message}",
                exc_info=True
            )
            raise e

def get_customer_repository(
    session: Session = Depends(get_session)
) -> CustomerRepository:
    return CustomerRepository(session)
