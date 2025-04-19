from models.video import Video
from pydantic import BaseModel
from typing import List
from datetime import datetime
from typing import Optional


class PlaylistMetadata(BaseModel):
    playlistId: str
    title: str
    description: Optional[str] = ""
    publishedAt: datetime

class Playlist(BaseModel):
    metadata: PlaylistMetadata
    videos: List[Video]
