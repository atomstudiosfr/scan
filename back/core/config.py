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

    SCALEWAY_S3_REGION: str = 'nl-ams'
    SCALEWAY_S3_URL: str = 'https://s3.nl-ams.scw.cloud'
    SCALEWAY_S3_KEY_ID: str = 'SCWVEF6RREH8E7FA0G5B'
    SCALEWAY_S3_ACCESS_KEY: str = 'b0d1a483-368f-4b54-9847-73db7a6230da'


SETTINGS = Settings()
