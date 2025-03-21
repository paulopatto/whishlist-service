import os

from sqlmodel import Session, create_engine

from src.config.envs import load_envs

MEMORY_DATABASE_URL = "sqlite:///:memory:"
load_envs()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True)

def get_engine():
    return engine

def get_session():
    with Session(engine) as session:
        yield session

# SessionType = Annotated[Session, Depends(get_session)]
