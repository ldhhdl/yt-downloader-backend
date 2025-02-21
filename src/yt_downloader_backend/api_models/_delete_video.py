from pydantic import BaseModel


class DeleteVideoRequest(BaseModel):
    url: str
