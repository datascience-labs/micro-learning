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
    summary: Optional[str] = None
    subtitles: Optional[str]
    description: Optional[str]
    publishedAt: datetime
    thumbnailUrl: Optional[str]

    def print_summary(self):
        """
        세그먼트가 있는 경우 세그먼트 정보의 요약을 출력하고,
        세그먼트가 없는 경우 비디오 정보의 요약을 출력합니다.
        """
        if self.segments:
            print("세그먼트 요약:")
            for segment in self.segments:
                print(f"- 세그먼트 제목: {segment.title}")
                print(f"  요약: {segment.summary}")
                print(f"  시작 시간: {segment.start_time}, 종료 시간: {segment.end_time}")
        else:
            print("비디오 요약:")
            print(f"- 비디오 제목: {self.title}")
            print(f"  요약: {self.summary}")
