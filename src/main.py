import os

from dotenv import load_dotenv
from fastapi import FastAPI

from src.config.logger import AppLog as log
from src.healthcheck.routes import router as healthcheck_router
from src.customer.routes import router as customer_router

PYTHON_ENV = os.getenv("PYTHON_ENV", "development")
PORT = os.getenv("PORT", 8000)

match PYTHON_ENV:
    case "development":
        load_dotenv(".env")
    case "test":
        load_dotenv(".env-test")
    case _:
        log.debug("Not loading .env file")


app = FastAPI()


app.include_router(healthcheck_router)
app.include_router(customer_router)


#TODO: Changes to use lifespan https://fastapi.tiangolo.com/advanced/events/#lifespan
@app.on_event("startup")
async def startup_event():
    log.info(f"🚀 Starting up Whishlist Service in {PYTHON_ENV} mode at port {PORT}...")
