

from datetime import datetime, timezone
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from fastapi import Depends
from pydantic import BaseModel
from sqlmodel import Field, Relationship, SQLModel, Session, UniqueConstraint, select

from src.config.database import get_session
from src.customer.data import CustomerModel


class ProductDTO(BaseModel):
    id: int | None = None
    title: str | None = None
    price: Decimal | None = None
    image_url: str | None = None
    reviews_score: float | None = None

class FavoriteProductModel(SQLModel, table=True):
    __tablename__ = "favorite_products"
    __table_args__ = (
        UniqueConstraint(
            "customer_id",
            "product_id",
            name="unique_favorite_product"
        ),
    )

    id: int | None = Field(default=None, primary_key=True)
    customer_id: int = Field(foreign_key="customers.id")
    product_id: str = Field(nullable=False)
    title: str = Field(nullable=False)
    price: Decimal = Field(nullable=False)
    image_url: str = Field(nullable=False)
    review_score: Optional[float] = Field(default=None)

    created_at: datetime = Field(nullable=False, default=datetime.now(timezone.utc))
    updated_at: datetime = Field(
        nullable=False,
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)},
    )
    customer: "CustomerModel" = Relationship(back_populates="favorite_products") # noqa: F821

class FavoriteProductRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_customer_list(self, customer_external_id: UUID) -> List[FavoriteProductModel]:
        query = select(
            FavoriteProductModel
        ).join(
            CustomerModel, #FIXME: Aqui deveria ser feita uma injeçao da classe CustomerModel,
                           # mas não foi feita pois nao decidi ua forma elegante sem referenciar
                           # CustomerModel diretamente.
                           # Essa é uma falha de design que deveria ser corrigida.
            FavoriteProductModel.customer_id == CustomerModel.id
        ).where(
            CustomerModel.external_id == customer_external_id
        )
        result = self.session.exec(query)
        return result.all()


def get_favorite_repository(session: Session = Depends(get_session)) -> FavoriteProductRepository:
    return FavoriteProductRepository(session)
