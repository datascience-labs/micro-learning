from pydantic import BaseModel
from typing import List, Optional

class VideoSegment(BaseModel):
    id: str
    video_id: str
    title: str
    start_time: float
    end_time: float
    tags: List[str]
    keywords: List[str]
    subtitles: Optional[str]
    summary: str
    cognitive_level: str
    dok_level: str
