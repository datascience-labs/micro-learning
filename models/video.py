from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Video(BaseModel):
    id: str
    title: str
    description: Optional[str]
    publishedAt: datetime
    thumbnailUrl: Optional[str]
