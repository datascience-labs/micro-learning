from typing import Dict, List
from models import Playlist, PlaylistMetadata, Video  
from datetime import datetime
from controllers.video_segmentation_controller import segment_video_by_description
from models.channel import Channel
import re
import logging

class YouTubeTransformer:
    def transform_channel_videos(self, channel: Channel):
        """
        채널 객체 내 비디오를 분석하여 세그먼트를 생성하고 태그를 추가합니다.

        Args:
            channel (Channel): 분석할 채널 객체

        Returns:
            Channel: 세그먼트가 추가된 채널 객체
        """
        for playlist in channel.playlists:
            for video in playlist.videos:
                try:
                    # 비디오 설명에서 세그먼트 분리
                    segments = segment_video_by_description(video.id, video.description)

                    if segments:
                        logging.info(f"생성된 세그먼트: {len(segments)}개")

                    # 태그 추출 및 추가
                    tag_pattern = r"#(\w+)"
                    tags = re.findall(tag_pattern, video.description)

                    if tags:
                        logging.info(f"추출된 태그: {tags}")

                    # 비디오 객체에 세그먼트 추가
                    video.segments = segments
                    video.tags = tags
                except ValueError as e:
                    print(f"⚠️ {video.title}에서 세그먼트를 생성할 수 없습니다: {e}")

        return channel

    def extract_subtitles(self, video_id: str) -> str:
        """
        비디오 ID를 사용하여 자막을 추출합니다.

        Args:
            video_id (str): 비디오 ID

        Returns:
            str: 추출된 자막 텍스트
        """
        # TODO: 자막 추출 로직 구현 (YouTube API 또는 외부 라이브러리 활용)
        return "추출된 자막 텍스트"

    def generate_summary(self, text: str) -> str:
        """
        주어진 텍스트를 요약합니다.

        Args:
            text (str): 요약할 텍스트

        Returns:
            str: 요약된 텍스트
        """
        # TODO: 요약 생성 로직 구현 (예: OpenAI API 또는 Hugging Face 모델 활용)
        return "요약된 텍스트"

    def generate_title(self, text: str) -> str:
        """
        주어진 텍스트를 기반으로 제목을 생성합니다.

        Args:
            text (str): 제목을 생성할 텍스트

        Returns:
            str: 생성된 제목
        """
        # TODO: 제목 생성 로직 구현 (예: OpenAI API 또는 Hugging Face 모델 활용)
        return "생성된 제목"
