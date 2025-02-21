from pydantic import BaseModel


class DownloadVideoRequest(BaseModel):
    url: str
