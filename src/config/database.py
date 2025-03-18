import os
from src.config.envs import load_envs
from src.config.logger import AppLog as log
from typing import Annotated
from fastapi import Depends
from sqlmodel import SQLModel, Session, create_engine

from src.customer.data import CustomerModel

load_envs()
MEMORY_DATABASE_URL = "sqlite:///:memory:"
DATABASE_URL = os.getenv("DATABASE_URL", MEMORY_DATABASE_URL)

# FIXME: Remover isso para ir para produçao
engine = create_engine(DATABASE_URL, echo=True)


def database_setup():
    log.info("=== Setup database")
    log.info(f"ENV={os.getenv("PYTHON_ENV")}")
    CustomerModel()
    SQLModel.metadata.create_all(engine)
    log.info("=== Setup database done.")


def get_session():
    with Session(engine) as session:
        yield session


SessionType = Annotated[Session, Depends(get_session)]

