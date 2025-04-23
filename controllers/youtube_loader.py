import polars as pl
import pandas as pd
import csv
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
                if not 'segments' in video:
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
                else:
                    for segment in video.segments:
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
                            "video_thumbnail_url": video.thumbnailUrl,
                            "segment_id": segment.id,
                            "segment_title": segment.title,
                            "segment_start_time": segment.start_time,
                            "segment_end_time": segment.end_time,
                            "segment_tags": ",".join(segment.tags),
                            "segment_keywords": ",".join(segment.keywords),
                            "segment_summary": segment.summary,
                            "segment_cognitive_level": segment.cognitive_level,
                            "segment_dok_level": segment.dok_level
                        })

        return pl.DataFrame(rows)
    
    
    def save_channel_to_csv(self, channel: Channel, filepath: str):
        df = self.flatten_channel_to_df(channel)

        # # description의 줄바꿈 문제 해결
        # df = df.with_columns(
        #     # df["channel_description"].str.replace("\n", " "),
        #     # df["playlist_description"].str.replace("\n", " "),
        #     df["video_description"].str.replace("\n", " ")
        # )
        pandas_df = df.to_pandas()

        pandas_df.to_csv(filepath, index=False, encoding="utf-8-sig", quoting=csv.QUOTE_ALL)  # quoting=1은 csv.QUOTE_NONNUMERIC과 동일
        
        # df.write_csv(filepath, encoding="utf-8-sig")  # 한글 깨짐 방지를 위해 utf-8-sig 인코딩 사용
        print(f"✅ CSV 저장 완료: {filepath}")

    def save_channel_to_xlsx(self, channel: Channel, filepath: str):
        """
        Channel 객체를 Polars DataFrame으로 변환한 뒤 Excel 파일로 저장
        """

        # Polars DataFrame을 생성
        df = self.flatten_channel_to_df(channel)

        # Polars DataFrame을 Pandas DataFrame으로 변환
        pandas_df = df.to_pandas()

        # Pandas DataFrame을 Excel 파일로 저장
        pandas_df.to_excel(filepath, index=False, engine="openpyxl")
        print(f"✅ Excel 저장 완료: {filepath}")
