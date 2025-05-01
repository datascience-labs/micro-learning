from googleapiclient.discovery import build
from models import Channel, Playlist, PlaylistMetadata, Video
from datetime import datetime

class YouTubeExtractor:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.youtube = build('youtube', 'v3', developerKey=api_key)

    def get_playlists(self, channel_id: str) -> list:
        """
        채널 ID로부터 해당 채널의 모든 재생목록을 반환
        """
        playlists = []
        next_page_token = None

        while True:
            request = self.youtube.playlists().list(
                part='snippet',
                channelId=channel_id,
                maxResults=50,
                pageToken=next_page_token
            )
            response = request.execute()

            for item in response['items']:
                playlists.append({
                    "playlistId": item['id'],
                    "title": item['snippet']['title'],
                    "description": item['snippet'].get('description', ''),
                    "publishedAt": item['snippet']['publishedAt']
                })

            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break

        return playlists
    
    def get_channel_metadata(self, channel_id: str) -> dict:
        """
        채널 ID로부터 채널의 상세 메타데이터를 반환
        """
        request = self.youtube.channels().list(
            part="snippet,statistics",
            id=channel_id
        )
        response = request.execute()
        if not response["items"]:
            raise ValueError(f"Channel ID {channel_id} not found.")

        item = response["items"][0]
        snippet = item["snippet"]
        stats = item["statistics"]

        return {
            "id": item["id"],
            "title": snippet.get("title"),
            "description": snippet.get("description", ""),
            "publishedAt": snippet.get("publishedAt"),
            "customUrl": snippet.get("customUrl", None),
            "thumbnailUrl": snippet.get("thumbnails", {}).get("high", {}).get("url", None),
            "country": snippet.get("country", None),
            "language": snippet.get("defaultLanguage", None),
            "viewCount": int(stats.get("viewCount", 0)),
            "subscriberCount": int(stats.get("subscriberCount", 0)),
            "videoCount": int(stats.get("videoCount", 0))
        }


    def get_videos(self, playlist_id: str) -> list:
        """
        재생목록 ID로부터 해당 재생목록의 모든 비디오 정보를 반환
        """
        videos = []
        next_page_token = None

        while True:
            request = self.youtube.playlistItems().list(
                part='snippet',
                playlistId=playlist_id,
                maxResults=50,
                pageToken=next_page_token
            )
            response = request.execute()

            for item in response['items']:
                snippet = item['snippet']
                if snippet.get("resourceId", {}).get("videoId"):
                    videos.append({
                        "videoId": snippet["resourceId"]["videoId"],
                        "title": snippet["title"],
                        "description": snippet.get("description", ""),
                        "publishedAt": snippet["publishedAt"],
                        "thumbnailUrl": snippet.get("thumbnails", {}).get("high", {}).get("url")
                    })

            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break

        return videos

    def extract_all(self, channel_id: str) -> Channel:
        """
        채널 ID로부터 Channel 객체 전체 반환
        (채널 정보 + 재생목록 + 재생목록 내 비디오 포함)
        """
        # 채널 메타데이터 수집
        meta_raw = self.get_channel_metadata(channel_id)

        # 재생목록 수집
        playlists_raw = self.get_playlists(channel_id)
        playlist_objects = []

        for playlist in playlists_raw:
            playlist_id = playlist["playlistId"]
            videos_raw = self.get_videos(playlist_id)

            videos = [
                Video(
                    id=vid["videoId"],
                    title=vid["title"],
                    subtitles=None,
                    summary=None,
                    description=vid.get("description", ""),
                    publishedAt=datetime.fromisoformat(vid["publishedAt"].replace("Z", "+00:00")),
                    thumbnailUrl=vid.get("thumbnailUrl")
                )
                for vid in videos_raw
            ]

            playlist_obj = Playlist(
                metadata=PlaylistMetadata(
                    playlistId=playlist["playlistId"],
                    title=playlist["title"],
                    description=playlist.get("description", ""),
                    publishedAt=datetime.fromisoformat(playlist["publishedAt"].replace("Z", "+00:00"))
                ),
                videos=videos
            )
            playlist_objects.append(playlist_obj)

        # Channel 객체 생성
        channel = Channel(
            id=meta_raw["id"],
            title=meta_raw["title"],
            description=meta_raw.get("description", ""),
            published_at=datetime.fromisoformat(meta_raw["publishedAt"].replace("Z", "+00:00")) if meta_raw.get("publishedAt") else None,
            custom_url=meta_raw.get("customUrl"),
            thumbnail_url=meta_raw.get("thumbnailUrl"),
            country=meta_raw.get("country"),
            language=meta_raw.get("language"),
            view_count=meta_raw.get("viewCount"),
            subscriber_count=meta_raw.get("subscriberCount"),
            video_count=meta_raw.get("videoCount"),
            playlists=playlist_objects
        )

        return channel