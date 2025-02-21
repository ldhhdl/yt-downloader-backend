import pytest
from fastapi import HTTPException

from yt_downloader_backend.routers import video

TABLE_NAME = "table_name"
VIDEO_CODE = "abc123"


@pytest.mark.unit
def test_get_video_code() -> None:
    url = "https://www.youtube.com/watch?v=abc123"
    assert video._get_video_code(url) == "abc123"


@pytest.mark.unit
def test_get_video_code_invalid_url() -> None:
    url = "https://www.youtube.com/watch"
    with pytest.raises(HTTPException):
        video._get_video_code(url)


@pytest.mark.unit
def test_check_already_exists(mocker) -> None:
    dynamodb_client = mocker.patch("yt_downloader_backend.clients.get_dynamodb_client")
    dynamodb_client.return_value.query.return_value = {
        "Items": [{"video_code": {"S": VIDEO_CODE}}]
    }
    assert video._check_already_exists(TABLE_NAME, VIDEO_CODE)


@pytest.mark.unit
def test_check_already_not_exists(mocker) -> None:
    dynamodb_client = mocker.patch("yt_downloader_backend.clients.get_dynamodb_client")
    dynamodb_client.return_value.query.return_value = {"Items": []}
    assert not video._check_already_exists(TABLE_NAME, VIDEO_CODE)
