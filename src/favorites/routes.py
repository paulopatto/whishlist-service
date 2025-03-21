from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from src.favorites.data import (
    FavoriteProductRepository,
    ProductDTO,
    get_favorite_repository,
)
from src.favorites.services import add_favorite, get_favorites

router = APIRouter(
    prefix="/api/customer/{customer_id}/favorites",
    dependencies=[Depends(validate_token)]
)



@router.get(
    "/",
    description="Get the clustomer's favorite list with pagination",
    tags=["Favorites"]
)
async def get_customer_product_list(
    customer_id: UUID,
    page: int = 1,
    per_page: int = 10,
    repository: FavoriteProductRepository = Depends(get_favorite_repository)
) -> List[ProductDTO]:
    products: List[ProductDTO] = await get_favorites(customer_id, repository)
    return products

@router.post(
    "/{product_id}",
    description="Add a product to the customer's favorite list",
    tags=["Favorites"]
)
async def add_product_to_customer_list(
    customer_id: UUID,
    product_id: int,
    repository: FavoriteProductRepository = Depends(get_favorite_repository)
) -> ProductDTO:
    try:
        product: ProductDTO = await add_favorite(customer_id, product_id, repository)
        return product
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")
