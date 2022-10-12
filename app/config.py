from pydantic import BaseSettings
from fastapi_jwt_auth import AuthJWT


class Settings(BaseSettings):
    database_host: str
    database_name: str
    database_username: str
    database_password: str
    authjwt_secret_key: str
    authjwt_token_location: set = {"cookies"}
    authjwt_cookie_secure: bool
    authjwt_cookie_csrf_protect: bool
    authjwt_cookie_domain: str
    authjwt_cookie_samesite: str
    authjwt_cookie_max_age: int

    class Config:
        env_file = ".env"


settings = Settings()


@AuthJWT.load_config
def get_config():
    return settings
