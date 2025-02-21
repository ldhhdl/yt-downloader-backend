from fastapi import APIRouter

from yt_downloader_backend.api_models import DownloadVideoRequest


def get_router() -> APIRouter:
    router = APIRouter()

    @router.post("/video")
    async def download_video(request: DownloadVideoRequest) -> None:
        raise NotImplementedError("finish this")

    return router
