import os
from typing import List
from uuid import UUID

import requests
from requests.exceptions import RequestException
from sqlalchemy.exc import IntegrityError

from src.config.logger import AppLog as log
from src.favorites.data import FavoriteProductRepository, ProductDTO


async def get_favorites(
    customer_id: UUID,
    repository: FavoriteProductRepository
) -> List[ProductDTO]:
    favorite_products = repository.get_customer_list(customer_id)
    products: List[ProductDTO] = [
        ProductDTO(
            product_id=favorite_product.id,
            title=favorite_product.title,
            price=favorite_product.price,
            image_url=favorite_product.image_url,
            reviews_score=favorite_product.review_score,
        )
        for favorite_product in favorite_products
    ]
    return products


async def add_favorite(
    customer_id: UUID,
    product_id: int,
    repository: FavoriteProductRepository
) -> ProductDTO:
    try:
        product: ProductDTO = await _fetch_product_from_product_api(product_id)
        repository.add_favorite(customer_id, product)
        return product
    except IntegrityError as e:
        log.error(f"Error during add favorite due {str(e)}", exc_info=True)
        raise ValueError("Product is already in the favorite list")
    except Exception as e:
        log.error(f"Error during add favorite due {str(e)}")
        raise e


async def _fetch_product_from_product_api(product_id: int) -> ProductDTO:
    PRODUCT_API_ENDPOINT = os.getenv("PRODUCT_API_URL")

    if not PRODUCT_API_ENDPOINT:
        raise ValueError("PRODUCT_API_URL environment variable is not set")
    try:
        log.info("Fetching product from product-api")
        response = requests.get(f'{PRODUCT_API_ENDPOINT}/api/product/{product_id}')
        #import pdb; pdb.set_trace()
        if response.status_code != 200:
            raise RequestException("No successful response from product-api")
    except RequestException as e:
        error_message = f"Error during fetch product from product-api due {str(e)}"
        log.error(error_message, exc_info=True)
        raise ValueError(error_message)

    product_data = response.json()
    product = ProductDTO(
        id=product_data.get("id"),
        title=product_data.get("title"),
        price=product_data.get("price"),
        image_url=product_data.get("image"),
        reviews_score=product_data.get("reviewScore"),
    )
    return product
