from typing import Dict, List
from models import Playlist, PlaylistMetadata, Video  
from datetime import datetime


class YouTubeTransformer:
    """
    segment 분할 및 기타 변환
    """
    def transform(self, raw_data: Dict[str, Dict]) -> List[Playlist]:
        playlists: List[Playlist] = []

        for title, content in raw_data.items():
            meta_raw = content.get("metadata", {})
            videos_raw = content.get("videos", [])

            metadata = PlaylistMetadata(
                playlistId=meta_raw["playlistId"],
                title=meta_raw["title"],
                description=meta_raw.get("description", ""),
                publishedAt=datetime.fromisoformat(meta_raw["publishedAt"].replace("Z", "+00:00"))
            )

            videos = [
                Video(
                    videoId=vid["videoId"],
                    title=vid["title"],
                    description=vid.get("description", ""),
                    publishedAt=datetime.fromisoformat(vid["publishedAt"].replace("Z", "+00:00")),
                    thumbnailUrl=vid.get("thumbnailUrl")
                )
                for vid in videos_raw
            ]

            playlists.append(Playlist(metadata=metadata, videos=videos))

        return playlists
