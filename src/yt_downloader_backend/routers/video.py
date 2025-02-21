from typing import Annotated

from fastapi import APIRouter, Depends, status

def get_router() -> APIRouter:
    router = APIRouter()

    @router.post('/video')
    async def download_video(request: DownloadVideoRequest) -> None:
        raise NotImplementedError('finish this')

    return router
