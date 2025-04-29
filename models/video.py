from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from models.video_segment import VideoSegment

class Video(BaseModel):
    """
    Represents a YouTube video with metadata and optional details.

    Attributes:
        id (str): The unique identifier for the video.
        title (str): The title of the video.
        tags (Optional[list[str]]): A list of tags associated with the video.
        segments (Optional[list[VideoSegment]]): A list of video segments, each containing detailed information.
        subtitles (Optional[str]): The full subtitles of the video as a single string.
        description (Optional[str]): The description of the video.
        publishedAt (datetime): The publication date and time of the video.
        thumbnailUrl (Optional[str]): The URL of the video's thumbnail image.
    """
    id: str
    title: str
    tags: Optional[list[str]] = None
    segments: Optional[list[VideoSegment]] = None
    subtitles: Optional[str]
    description: Optional[str]
    publishedAt: datetime
    thumbnailUrl: Optional[str]
