from pydantic import BaseModel


class VideoItem(BaseModel):
    video_hash: str
    video_code: str
    name: str
