import os
from dotenv import load_dotenv
from src.config.logger import AppLog as log


def load_envs(env=os.getenv("PYTHON_ENV", "development")):
    match env:
        case "development":
            log.info(f"⛏️ Loading envs for {env} from .env")
            load_dotenv(".env")
        case "test":
            log.info(f"⛏️ Loading envs for {env} from .env-test")
            load_dotenv(".env-test")
        case _:
            log.debug("Not loading .env file")

