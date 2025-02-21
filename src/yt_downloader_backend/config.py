import functools

from pydantic import Secret
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    bucket_name: str
    queue_url: str
    table_name: str
    aws_region: str
    aws_access_key_id: Secret[str]
    aws_secret_access_key: Secret[str]


@functools.lru_cache
def get_settings() -> Settings:
    return Settings()
