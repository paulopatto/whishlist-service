from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends

from src.favorites.data import FavoriteProductRepository, ProductDTO, get_favorite_repository
from src.favorites.services import get_favorites

router = APIRouter(prefix="/api/customer/{customer_id}/list")



@router.get(
    "/",
    description="Get the clustomer's product list with pagination",
    tags=["ProductList"]
)
async def get_customer_product_list(
    customer_id: UUID,
    page: int = 1,
    per_page: int = 10,
    repository: FavoriteProductRepository = Depends(get_favorite_repository)
) -> List[ProductDTO]:
    products: List[ProductDTO] = await get_favorites(customer_id, repository)
    return products
