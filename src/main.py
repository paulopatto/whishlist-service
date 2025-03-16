import os
from fastapi import FastAPI
from src.healthcheck.routes import router as healthcheck_router
from dotenv import load_dotenv


PYTHON_ENV = os.getenv("PYTHON_ENV", "development")
ENVS_TO_LOAD_DOTENV = ["development", "test"]

if PYTHON_ENV in ENVS_TO_LOAD_DOTENV:
    load_dotenv()

app = FastAPI()


app.include_router(healthcheck_router)
