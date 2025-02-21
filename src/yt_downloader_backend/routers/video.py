from fastapi import APIRouter

from yt_downloader_backend.api_models import DownloadVideoRequest


def get_router() -> APIRouter:
    router = APIRouter()

    @router.post("/video")
    async def download_video(request: DownloadVideoRequest) -> None:
        raise NotImplementedError("finish this")

    @router.get("/video")
    async def list_videos() -> None:
        raise NotImplementedError("finish this")

    @router.get("/video/{video_id}")
    async def get_video(video_id: str) -> None:
        raise NotImplementedError("finish this")

    return router
