import pytest
from fastapi import HTTPException
from pytest_mock import MockerFixture

from yt_downloader_backend.routers import video

TABLE_NAME = "table_name"
VIDEO_CODE = "abc123"

pytestmark = pytest.mark.unit


def test_get_video_code() -> None:
    url = "https://www.youtube.com/watch?v=abc123"
    assert video._get_video_code(url) == "abc123"


def test_get_video_code_invalid_url() -> None:
    url = "https://www.youtube.com/watch"
    with pytest.raises(HTTPException):
        video._get_video_code(url)


def test_check_already_exists(mocker: MockerFixture) -> None:
    dynamodb_client = mocker.patch("yt_downloader_backend.clients.get_dynamodb_client")
    dynamodb_client.return_value.query.return_value = {
        "Items": [{"video_code": {"S": VIDEO_CODE}}]
    }
    assert video._check_already_exists(TABLE_NAME, VIDEO_CODE)


def test_check_already_not_exists(mocker: MockerFixture) -> None:
    dynamodb_client = mocker.patch("yt_downloader_backend.clients.get_dynamodb_client")
    dynamodb_client.return_value.query.return_value = {"Items": []}
    assert not video._check_already_exists(TABLE_NAME, VIDEO_CODE)
