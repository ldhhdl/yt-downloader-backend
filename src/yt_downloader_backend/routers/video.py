from typing import Annotated
from urllib.parse import parse_qs, urlparse

import botocore
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse

from yt_downloader_backend import clients
from yt_downloader_backend.api_models import DownloadVideoRequest, VideoItem
from yt_downloader_backend.config import Settings, get_settings


def get_router() -> APIRouter:
    router = APIRouter()

    @router.post("/video", status_code=status.HTTP_201_CREATED)
    async def download_video(
        request: DownloadVideoRequest,
        settings: Annotated[Settings, Depends(get_settings)],
    ) -> None:
        video_code = parse_qs(urlparse(request.url).query).get("v", [""])[0]
        if not video_code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid URL"
            )

        dynamodb_client = clients.get_dynamodb_client()
        response = dynamodb_client.query(
            TableName=settings.table_name,
            KeyConditionExpression="video_code = :video_code",
            ExpressionAttributeValues={":video_code": {"S": video_code}},
        )
        if response["Items"]:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Video already exists"
            )

        sqs_client = clients.get_sqs_client()
        sqs_client.send_message(
            QueueUrl=settings.queue_url,
            MessageBody=request.url,
        )

    @router.get("/video")
    async def list_videos(
        settings: Annotated[Settings, Depends(get_settings)],
    ) -> list[VideoItem]:
        dynamodb_client = clients.get_dynamodb_client()
        response = dynamodb_client.scan(TableName=settings.table_name)
        return [
            VideoItem(
                video_code=item["video_code"]["S"],
                video_hash=item["video_hash"]["S"],
                name=item["name"]["S"],
            )
            for item in response["Items"]
        ]

    @router.get("/video/{video_hash}")
    async def get_video(
        video_hash: str, settings: Annotated[Settings, Depends(get_settings)]
    ) -> StreamingResponse:
        s3_client = clients.get_s3_client()
        try:
            response = s3_client.get_object(
                Bucket=settings.bucket_name,
                Key=video_hash,
            )
        except botocore.errorfactory.NoSuchKey:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Video not found"
            )

        return StreamingResponse(response["Body"], media_type="video/mp4")

    return router
