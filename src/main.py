import os

from fastapi import FastAPI
from src.config.envs import load_envs, PYTHON_ENV
from src.config.logger import AppLog as log
from src.healthcheck.routes import router as healthcheck_router
from src.customer.routes import router as customer_router

load_envs()

PORT = os.getenv("PORT", 8000)

app = FastAPI()


app.include_router(healthcheck_router)
app.include_router(customer_router)


# TODO: Changes to use lifespan https://fastapi.tiangolo.com/advanced/events/#lifespan
@app.on_event("startup")
async def startup_event():
    log.info(f"🚀 Starting up Whishlist Service in {PYTHON_ENV} mode at port {PORT}...")

