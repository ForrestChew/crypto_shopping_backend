from pydantic import BaseSettings


class Settings(BaseSettings):
    database_host: str
    database_name: str
    database_username: str
    database_password: str
    jose_jwt_secret_key: str
    algorithm: str
    access_token_expire_minutes: str

    class Config:
        env_file = ".env"


settings = Settings()
