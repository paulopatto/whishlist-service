

from typing import List
from uuid import UUID

from src.favorites.data import FavoriteProductRepository, ProductDTO


async def get_favorites(customer_id: UUID, repository: FavoriteProductRepository) -> List[ProductDTO]:
    favorite_products = repository.get_customer_list(customer_id)
    products: List[ProductDTO] = [
        ProductDTO(
            id=favorite_product.id,
            title=favorite_product.title,
            price=favorite_product.price,
            image_url=favorite_product.image_url,
            reviews_score=favorite_product.review_score,
        )
        for favorite_product in favorite_products
    ]
    return products
