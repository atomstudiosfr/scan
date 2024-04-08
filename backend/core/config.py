import os

from alembic.config import Config
from pydantic_settings import BaseSettings

path_alembic_ini = os.path.realpath(os.path.join(__file__, "..", "..", "alembic.ini"))
ALEMBIC_CONFIG = Config(path_alembic_ini)
ALEMBIC_CONFIG.set_main_option(
    "script_location",
    os.path.realpath(os.path.join(__file__, "..", "..", "migrations")),
)


class Settings(BaseSettings):
    PROJECT_NAME: str = 'My API'
    SECRET_KEY: str = "your-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ASYNC_SQLALCHEMY_DATABASE_URI: str = 'postgresql+psycopg://postgres:postgres@localhost:5432/postgres'


SETTINGS = Settings()
