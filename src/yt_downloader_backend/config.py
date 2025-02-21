import functools

from pydantic import Secret
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    bucket_name: str = "video-downloads"
    queue_url: str = "blah"
    table_name: str = "video-downloads"
    aws_region: str = "us-east-1"
    aws_access_key_id: Secret[str] = "AKIA4IM3HDCO5O2KLTXS"
    aws_secret_access_key: Secret[str] = "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"


@functools.lru_cache
def get_settings() -> Settings:
    return Settings()
