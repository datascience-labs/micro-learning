import polars as pl
from models import Channel

class YouTubeLoader:
    def __init__(self):
        pass

    def to_csv(self, transformed_data: list, filename: str):
        import csv
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=transformed_data[0].keys())
            writer.writeheader()
            writer.writerows(transformed_data)

    def to_json(self, transformed_data: list, filename: str):
        import json
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(transformed_data, f, ensure_ascii=False, indent=2)

    def flatten_channel_to_df(self, channel: Channel) -> pl.DataFrame:
        """
        Channel 객체를 Polars DataFrame으로 변환
        각 행 = 하나의 비디오 (채널/재생목록/비디오 정보 포함)
        """
        rows = []
        for playlist in channel.playlists:
            for video in playlist.videos:
                rows.append({
                    "channel_id": channel.id,
                    "channel_title": channel.title,
                    "channel_description": channel.description,
                    "channel_published_at": channel.published_at,
                    "channel_custom_url": channel.custom_url,
                    "channel_country": channel.country,
                    "channel_language": channel.language,
                    "channel_view_count": channel.view_count,
                    "channel_subscriber_count": channel.subscriber_count,
                    "channel_video_count": channel.video_count,
                    "playlist_id": playlist.metadata.playlistId,
                    "playlist_title": playlist.metadata.title,
                    "playlist_description": playlist.metadata.description,
                    "playlist_published_at": playlist.metadata.publishedAt,
                    "video_id": video.id,
                    "video_title": video.title,
                    "video_description": video.description,
                    "video_published_at": video.publishedAt,
                    "video_thumbnail_url": video.thumbnailUrl
                })

        return pl.DataFrame(rows)
    
    
    def save_channel_to_csv(self, channel: Channel, filepath: str):
        df = self.flatten_channel_to_df(channel)
        df.write_csv(filepath)
        print(f"✅ CSV 저장 완료: {filepath}")