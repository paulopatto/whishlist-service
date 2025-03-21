import os

from sqlmodel import SQLModel

from src.config.database import get_engine
from src.config.logger import AppLog as log
from src.customer.data import CustomerModel
from src.favorites.data import FavoriteProductModel


def database_setup():
    log.info("=== Setup database")
    log.info(f"ENV={os.getenv("PYTHON_ENV")}")
    log.info(f"Registered tables: {SQLModel.metadata.tables.keys()}")
    SQLModel.metadata.create_all(get_engine())
    log.info("=== Setup database done.")

def rebuild_models():
    log.info("=== Rebuilding database models")
    log.info(f"Registered tables: {SQLModel.metadata.tables.keys()}")
    models = [
        CustomerModel,
        FavoriteProductModel,
    ]

    [m.model_rebuild() for m in models]

    log.info("=== Rebuilding database models done.")
