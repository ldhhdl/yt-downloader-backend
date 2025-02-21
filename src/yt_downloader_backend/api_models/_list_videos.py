from pydantic import BaseModel


class VideoItem(BaseModel):
    video_code: str  # The partition key in the DynamoDB table
    name: str  # The sort key in the DynamoDB table
    video_hash: str  # The hash of the video file in S3
