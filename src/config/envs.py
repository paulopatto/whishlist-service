import os
from dotenv import load_dotenv

PYTHON_ENV = os.getenv("PYTHON_ENV", "development")


def load_envs():
    match PYTHON_ENV:
        case "development":
            load_dotenv(".env")
        case "test":
            load_dotenv(".env-test")
        case _:
            log.debug("Not loading .env file")

