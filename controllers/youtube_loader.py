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

    def flatten_channel_to_df(self, channel: Channel) -> tuple[pl.DataFrame, pl.DataFrame]:
        """
        Channel 객체를 Polars DataFrame으로 변환
        세그먼트가 있는 비디오와 없는 비디오를 각각 DataFrame으로 반환
        """
        rows_with_segments = []
        rows_without_segments = []

        for playlist in channel.playlists:
            for video in playlist.videos:
                if hasattr(video, 'segments') and video.segments:
                    for segment in video.segments:
                        rows_with_segments.append({
                            "channel_id": channel.id,
                            "channel_title": channel.title,
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
                else:
                    rows_without_segments.append({
                        "channel_id": channel.id,
                        "channel_title": channel.title,
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

        df_with_segments = pl.DataFrame(rows_with_segments)
        df_without_segments = pl.DataFrame(rows_without_segments)

        return df_with_segments, df_without_segments
    
    def save_channel_to_csv(self, channel: Channel, filepath: str):
        df_with_segments, df_without_segments = self.flatten_channel_to_df(channel)

        pandas_df_with_segments = df_with_segments.to_pandas()
        pandas_df_without_segments = df_without_segments.to_pandas()

        pandas_df_with_segments.to_csv(filepath.replace(".csv", "_with_segments.csv"), index=False, encoding="utf-8-sig", quoting=csv.QUOTE_ALL)
        pandas_df_without_segments.to_csv(filepath.replace(".csv", "_without_segments.csv"), index=False, encoding="utf-8-sig", quoting=csv.QUOTE_ALL)
        
        print(f"✅ CSV 저장 완료: {filepath}")

    def save_channel_to_xlsx(self, channel: Channel, filepath: str):
        """
        Channel 객체를 Polars DataFrame으로 변환한 뒤 Excel 파일로 저장
        """

        df_with_segments, df_without_segments = self.flatten_channel_to_df(channel)

        pandas_df_with_segments = df_with_segments.to_pandas()
        pandas_df_without_segments = df_without_segments.to_pandas()

        pandas_df_with_segments.to_excel(filepath.replace(".xlsx", "_with_segments.xlsx"), index=False, engine="openpyxl")
        pandas_df_without_segments.to_excel(filepath.replace(".xlsx", "_without_segments.xlsx"), index=False, engine="openpyxl")
        
        print(f"✅ Excel 저장 완료: {filepath}")
