from pydantic import BaseModel
from typing import Optional

class Video(BaseModel):
    id: str
    title: str
    description: Optional[str]
    published_at: Optional[str]
    channel_id: str
    playlist_id: Optional[str]
