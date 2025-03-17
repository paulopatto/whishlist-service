import os
from dotenv import load_dotenv
from fastapi import FastAPI
from src.config.logger import AppLog as log

from src.healthcheck.routes import router as healthcheck_router

PYTHON_ENV = os.getenv("PYTHON_ENV", "development")
ENVS_TO_LOAD_DOTENV = ["development", "test"]
PORT = os.getenv("PORT", 8000)

if PYTHON_ENV in ENVS_TO_LOAD_DOTENV:
    load_dotenv()
    log.info(f"Loading environment variables from .env file for {PYTHON_ENV} environment")

app = FastAPI()


app.include_router(healthcheck_router)


#TODO: Changes to use lifespan https://fastapi.tiangolo.com/advanced/events/#lifespan
@app.on_event("startup")
async def startup_event():
    log.info(f"🚀 Starting up Whishlist Service in {PYTHON_ENV} mode at port {PORT}...")
