import click
import uvicorn

from src.config.envs import load_envs
from src.config.tables import database_setup

load_envs()


@click.group()
def cli():
    pass


@cli.command()
def start_server():
    """
    Start server in dev mode.
    """
    uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=True)


@cli.command()
def create_tables():
    """
    Create database tables.
    """
    database_setup()


if __name__ == "__main__":
    cli()

