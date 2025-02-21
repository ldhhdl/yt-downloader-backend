from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from yt_downloader_backend.routers import video


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # TODO: Use lifespan to setup any necessary config
    yield


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.include_router(video.get_router(), tags=["videos"])
    return app
