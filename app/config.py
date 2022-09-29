from lib2to3.pytree import Base
from pydantic import BaseSettings


class Settings(BaseSettings):
    database_host: str
    database_name: str
    database_username: str
    database_password: str

    class Config:
        env_file = ".env"


settings = Settings()
