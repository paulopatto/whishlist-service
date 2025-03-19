import uuid
from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, EmailStr
from sqlmodel import Field, SQLModel


class CustomerDTO(BaseModel):
    id: Optional[uuid.UUID | None] = None
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

