import os
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

from src.config.envs import load_envs
from src.config.logger import AppLog as log
from src.customer.data import CustomerModel

MEMORY_DATABASE_URL = "sqlite:///:memory:"
load_envs()
DATABASE_URL = os.getenv("DATABASE_URL")

# FIXME: Remover isso para ir para produçao
engine = create_engine(DATABASE_URL, echo=True)


def database_setup():
    log.info("=== Setup database")
    log.info(f"ENV={os.getenv("PYTHON_ENV")}")
    log.info(f"Registered tables: {SQLModel.metadata.tables.keys()}")
    SQLModel.metadata.create_all(engine)
    log.info("=== Setup database done.")


def get_session():
    with Session(engine) as session:
        yield session


SessionType = Annotated[Session, Depends(get_session)]

list(map(lambda m: m.__table__, [CustomerModel]))
