import requests
from config.settings import YOUTUBE_API_KEY
from models.channel import Channel
from models.playlist import Playlist
from models.video import Video
from views.graph_view import GraphView
from datetime import datetime

class ChannelIngestionController:
    def __init__(self):
        self.graph = GraphView()

    def fetch_playlists_for_channel(self, channel_id: str) -> list[Playlist]:
        playlists = []
        url = "https://www.googleapis.com/youtube/v3/playlists"
        params = {
            "part": "snippet",
            "channelId": channel_id,
            "maxResults": 50,
            "key": YOUTUBE_API_KEY
        }
        response = requests.get(url, params=params)
        response.raise_for_status()

        for item in response.json().get("items", []):
            playlists.append(Playlist(
                id=item["id"],
                title=item["snippet"]["title"],
                description=item["snippet"].get("description", ""),
                channel_id=channel_id
            ))
        return playlists

    def fetch_videos_for_playlist(self, playlist_id: str) -> list[Video]:
        videos = []
        url = "https://www.googleapis.com/youtube/v3/playlistItems"
        params = {
            "part": "snippet",
            "playlistId": playlist_id,
            "maxResults": 50,
            "key": YOUTUBE_API_KEY
        }
        response = requests.get(url, params=params)
        response.raise_for_status()

        for item in response.json().get("items", []):
            snippet = item["snippet"]
            video_id = snippet["resourceId"]["videoId"]
            videos.append(Video(
                id=video_id,
                title=snippet["title"],
                description=snippet.get("description", ""),
                published_at=datetime.fromisoformat(snippet.get("publishedAt", "1970-01-01T00:00:00Z").replace("Z", "+00:00")) if snippet.get("publishedAt") else None,
                channel_id=snippet["channelId"],
                playlist_id=playlist_id
            ))
        return videos

    def store_channel_playlists_videos(self, channel_id: str, channel_title: str):
        # Step 1: 채널 노드 생성
        channel = Channel(id=channel_id, title=channel_title, description="", published_at=None)
        self.graph.insert_node(channel)

        # Step 2: 채널의 플레이리스트 수집 및 저장
        playlists = self.fetch_playlists_for_channel(channel_id)
        for pl in playlists:
            self.graph.insert_node(pl)
            self.graph.insert_relationship(channel.id, pl.id, "HAS_PLAYLIST", "Channel", "Playlist")

            # Step 3: 각 플레이리스트의 영상 수집 및 저장
            videos = self.fetch_videos_for_playlist(pl.id)
            for v in videos:
                self.graph.insert_node(v)
                self.graph.insert_relationship(pl.id, v.id, "HAS_VIDEO", "Playlist", "Video")

    def close(self):
        self.graph.close()
