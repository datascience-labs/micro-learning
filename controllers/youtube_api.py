import requests
from models.channel import Channel
from models.video import Video
from config.settings import YOUTUBE_API_KEY

YOUTUBE_API_BASE = "https://www.googleapis.com/youtube/v3"

def fetch_video_details(video_id: str) -> dict:
    """
    주어진 video_id로 YouTube Data API를 호출하여 비디오 정보 반환
    """
    url = f"{YOUTUBE_API_BASE}/videos"
    params = {
        "part": "snippet,contentDetails",
        "id": video_id,
        "key": YOUTUBE_API_KEY
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    items = response.json().get("items", [])
    if not items:
        raise ValueError("No video found with the given ID")
    return items[0]

def extract_video_info(video_item: dict) -> dict:
    """
    API 결과 중 필요한 필드만 정제하여 반환
    """
    snippet = video_item["snippet"]
    return {
        "channelId": snippet["channelId"],
        "channelTitle": snippet["channelTitle"],
        "channelDescription": "",
        "channelPublishedAt": "",
        "videoId": video_item["id"],
        "videoTitle": snippet["title"],
        "videoDescription": snippet["description"],
        "videoPublishedAt": snippet["publishedAt"],
        "playlistId": snippet.get("playlistId", None)
    }


def fetch_and_parse_youtube_data(api_response):
    channel = Channel(
        id=api_response['channelId'],
        title=api_response['channelTitle'],
        description=api_response.get('channelDescription'),
        published_at=api_response.get('channelPublishedAt')
    )
    video = Video(
        id=api_response['videoId'],
        title=api_response['videoTitle'],
        description=api_response.get('videoDescription'),
        published_at=api_response.get('videoPublishedAt'),
        channel_id=channel.id,
        playlist_id=api_response.get('playlistId')
    )
    return channel, video
