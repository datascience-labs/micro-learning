from models.playlist import Playlist
from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional
from datetime import datetime

class Channel(BaseModel):
    id: str
    title: str
    description: Optional[str] = ""
    published_at: Optional[datetime] = None

    # 
    custom_url: Optional[str] = None
    thumbnail_url: Optional[HttpUrl] = None
    country: Optional[str] = None
    language: Optional[str] = None
    view_count: Optional[int] = None
    subscriber_count: Optional[int] = None
    video_count: Optional[int] = None

    playlists: List[Playlist] = Field(default_factory=list)
