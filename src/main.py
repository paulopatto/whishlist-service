import os

from fastapi import FastAPI

from src.auth.middlewares import BearerTokenMiddleware
from src.config.envs import load_envs
from src.config.logger import AppLog as log
from src.config.tables import database_setup, rebuild_models
from src.customer.routes import router as customer_router
from src.healthcheck.routes import router as healthcheck_router
from src.favorites.routes import router as favorites_router

load_envs()

PORT = os.getenv("API_PORT", 8000)
PY_ENV = os.getenv("PYTHON_ENV", "dev")
app = FastAPI()

app.include_router(healthcheck_router)
app.include_router(customer_router)
app.include_router(favorites_router)
app.add_middleware(BearerTokenMiddleware)


database_setup() # Runs "pseudo" migrations XD
rebuild_models()


# TODO: Changes to use lifespan
# https://fastapi.tiangolo.com/advanced/events/#lifespan
@app.on_event("startup")
async def startup_event():
    log.info(f"🚀 Starting up whishlist  in {PY_ENV} mode at port {PORT}...")

