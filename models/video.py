from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from models.video_segment import VideoSegment

class Video(BaseModel):
    id: str
    title: str
    tags: Optional[list[str]] = None
    segments: Optional[list[VideoSegment]] = None
    description: Optional[str]
    publishedAt: datetime
    thumbnailUrl: Optional[str]
