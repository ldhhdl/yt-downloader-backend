import functools

import boto3

from yt_downloader_backend.config import get_settings


def _get_aws_client(service_name: str) -> boto3.client:
    settings = get_settings()
    return boto3.client(
        service_name,
        region_name=settings.aws_region,
        aws_access_key_id=settings.aws_access_key_id.get_secret_value(),
        aws_secret_access_key=settings.aws_secret_access_key.get_secret_value(),
    )


@functools.lru_cache
def get_sqs_client() -> boto3.client:
    return _get_aws_client("sqs")


@functools.lru_cache
def get_s3_client() -> boto3.client:
    return _get_aws_client("s3")


@functools.lru_cache
def get_dynamodb_client() -> boto3.client:
    return _get_aws_client("dynamodb")


__all__ = ["get_sqs_client", "get_s3_client", "get_dynamodb_client"]
