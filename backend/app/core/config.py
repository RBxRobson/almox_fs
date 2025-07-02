from pydantic_settings import BaseSettings
from typing import Literal

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: Literal["HS256", "RS256", "HS384", "HS512"]
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"

settings = Settings()
