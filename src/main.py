from fastapi import FastAPI
from src.healthcheck.routes import router as healthcheck_router


app = FastAPI()


app.include_router(healthcheck_router)
